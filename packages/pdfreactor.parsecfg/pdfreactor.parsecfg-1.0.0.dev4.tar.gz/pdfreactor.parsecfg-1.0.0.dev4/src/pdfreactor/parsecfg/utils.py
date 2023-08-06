# -*- coding: UTF-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=79
"""\
tools.pdf.utils: Utility-Modul für den PDF-Export (mit PDFReactor)
"""

# Python compatibility:
from __future__ import absolute_import, print_function

from six.moves import map, range
from six.moves import StringIO

__author__ = "Tobias Herp <tobias.herp@visaplan.com>"

# Standard library:
from string import letters
from token import ENDMARKER, NAME, NEWLINE, OP, STRING, tok_name
from tokenize import (
    COMMENT,
    DEDENT,
    INDENT,
    NL,
    TokenError,
    generate_tokens,
    untokenize,
    )

# visaplan:
from visaplan.tools.minifuncs import makeBool
from visaplan.tools.minifuncs import translate_dummy as _
from visaplan.tools.sequences import sequence_slide

__all__ = ('ApiFilter',
           'acceptable_method_name',
           # ... verwendet: 'API_WHITELIST',
           )
# Logging / Debugging:
from visaplan.tools.debug import pp


def gen_restricted_lines(txt, func=None):
    """
    Generiere "Zeilen" aus dem übergebenen Text:

    >>> txt = '''# ein Kommentar
    ... strict on
    ... setAddLinks(False) # noch ein Kommentar
    ... with_images off
    ... '''

    >>> prefixed = make_prefixed('A')

    >>> list(gen_restricted_lines(txt, prefixed))
    ... # doctest: +NORMALIZE_WHITESPACE
    [<ControlStatement 'strict on '>,
     <ApiCall 'A.setAddLinks (False )'>,
     <ControlStatement 'with_images off '>]

    Einstmals hartcodierte Aufrufe:

    >>> txt2 = '''
    ... setAddLinks(False)
    ... # Enable bookmarks in the PDF document
    ... setAddBookmarks(True)
    ... setCleanupTool(CLEANUP_NONE)
    ... setEncoding('UTF-8')
    ... setJavaScriptMode(JAVASCRIPT_MODE_ENABLED_NO_LAYOUT)
    ... '''
    >>> list(gen_restricted_lines(txt2, prefixed))
    ... # doctest: +NORMALIZE_WHITESPACE
    [<ApiCall 'A.setAddLinks (False )'>,
     <ApiCall 'A.setAddBookmarks (True )'>,
     <ApiCall 'A.setCleanupTool (A.CLEANUP_NONE )'>,
     <ApiCall "A.setEncoding ('UTF-8')">,
     <ApiCall 'A.setJavaScriptMode (A.JAVASCRIPT_MODE_ENABLED_NO_LAYOUT )'>]

    Es können mehrere Anweisungen pro Zeile notiert werden,
    durch Semikolon getrennt:

    >>> txt3 = '; ;setA();setB()'
    >>> list(gen_restricted_lines(txt3, prefixed))
    [<ApiCall 'A.setA ()'>, <ApiCall 'A.setB ()'>]

    Nun zu den Neuerungen zur Unterstützung der neuen PDFreactor-API.
    Als Ersatz für die veralteten API-Aufrufe
    -- die (vorerst?) noch unterstützt und automatisch konvertiert werden --
    unterstützen wir nun direkte Zuweisungen an die config-Variable, die
    der .convert-Methode übergeben wird:

    >>> txt4 = '''
    ... config.outputFormat = {
    ...     type: OutputType.JPEG,
    ...     width: 640,
    ... }
    ... '''
    >>> list(gen_restricted_lines(txt4))      # doctest: +NORMALIZE_WHITESPACE
    [<Assignment 'config .outputFormat
                ={type :OutputType .JPEG ,width :640 ,}'>]
    """
    if not txt:
        return
    buf = []
    alltokens = generate_tokens(StringIO(txt or '').readline)
    for toktup in alltokens:
        ttype, token, startpos, endpos, line = toktup
        if ttype in (NEWLINE, ENDMARKER, DEDENT):
            if buf:
                yield restrictedStatement(buf, func)
                del buf[:]
        elif ttype == OP and token == ';':
            if buf:
                yield restrictedStatement(buf, func)
                del buf[:]
        elif ttype in (NL, COMMENT):
            pass
        elif not buf and ttype in (INDENT,
                ):
            pass
        else:
            buf.append(toktup)
    if buf:
        yield restrictedStatement(buf, func)

COMMAND_TYPES = list(range(100, 103))
CT_CONTROL, CT_ASSIGNMENT, CT_API = COMMAND_TYPES
"""\
toc (h2, h3, h4) afterbegin of body
appendix afterbegin of "#appendix" (
  images grouped force,
  media grouped auto,
  tables grouped auto,
  literature sorted,
  standards sorted
)"""

CONTROL_COMMANDS = ('strict',
                    'toc',
                    'appendix',
                    'with_images',
                    )
SYMBOLS_MAP = {}
_tmp = [('True',  'on', 'yes'),
        ('False', 'off', 'no'),
        ('None',  'null', 'nothing', 'nil'),
        ]
for _tup in _tmp:
    first = _tup[0]
    for name in _tup:
        SYMBOLS_MAP[name.lower()] = first

def make_prefixed(prefix):
    """
    Erzeuge eine Funktion, die
    - die Symbole der SYMBOLS_MAP normalisiert, und
    - alle anderen Namen mit einem Präfix versieht
    """
    if not prefix.endswith('.'):
        prefix += '.'
    def prefixed(token):
        ltoken = token.lower()
        if ltoken in SYMBOLS_MAP:
            return SYMBOLS_MAP[ltoken]
        else:
            return prefix + token
    return prefixed

class ApiError(ValueError):
    """
    Fehler bei Verarbeitung der PDFreactor-API-Aufrufe
    """
class BogusLine(ApiError):
    """
    Grundlegend fehlerhafte Zeile
    """
class DisallowedMethod(ApiError):
    """
    Versuch, eine unzulässige Methode aufzurufen
    """

def restrictedStatement(seq, transform_func):
    """
    Erzeuge aus der übergebenen (vom tokenize-Modul erzeugten) Sequenz einen
    API-Aufruf (Klasse ApiCall) oder eine Kontrollanweisung (ControlStatement).

    Einige Symbole werden normalisiert;
    so bestehen z. B. gewisse Freiheiten bei der Angabe logischer Werte:

    >>> func = make_prefixed('A')
    >>> repr(restrictedStatement([(1, 'strict'), (1, 'on')], func))
    "<ControlStatement 'strict on '>"
    >>> restrictedStatement([(1, 'strict'), (1, 'off')], func)
    <ControlStatement 'strict off '>

    Alle anderen Symbole werden, wie auch die Namen der API-Methoden,
    durch das Präfix <prefix> ergänzt:

    >>> restrictedStatement([(1, 'setDings'), (OP, '('),
    ...     (1, 'ATTRNAME'), (OP, ')')], func)
    <ApiCall 'A.setDings (A.ATTRNAME )'>

    (tokenize.untokenize fügt leider nach jedem Namen und jeder Zahl
    sicherheitshalber ein Leerzeichen ein)
    """
    res = []
    main = None
    ltype = None # line type, "Zeilen"typ
    for prevtup, currtup, nexttup in sequence_slide(seq):
        ttype, token = currtup[:2]
        WTF = tok_name[ttype]
        # pp(WTF, token)
        if main is None:
            if ttype == NAME:
                # set_trace()
                nexttype = (None
                            if nexttup is None
                            else nexttup[0])
                if nexttype is OP and nexttup[1] != '(':
                    ltype = CT_ASSIGNMENT
                elif token in CONTROL_COMMANDS:
                    ltype = CT_CONTROL
                elif nexttype == NAME:
                    # we might get an exception during untokenization :-(
                    # ... but at least it's an exception.
                    # We insist in the '.' OP after 'config'!
                    res.append(currtup)
                    raise BogusLine(untokenize(res))
                else:
                    ltype = CT_API
                main = token
        res.append(currtup)
    if ltype == CT_ASSIGNMENT:
        return Assignment(res, transform_func)
    elif ltype == CT_API:
        return ApiCall(res, transform_func)
    elif ltype == CT_CONTROL:
        return ControlStatement(res)
    elif not res:
        return None
    elif ltype is None:
        pp({'ltype:': ltype,
            'main': main,
            'res': res,
            })
        for toktup in res:
            token_info(*toktup)
        raise BogusLine(untokenize(res))
    else:
        raise ProgrammingError
    return ' '.join(res)

API_WHITELIST = frozenset(['enableDebugMode',
                           ])
def acceptable_method_name(name):
    """
    Gehört der übergebene Name zu einer akzeptablen PDFreactor-API-Funktion?
    """
    if name in API_WHITELIST:
        return True
    if not name[3:]:
        return False
    if (name.startswith('set')
        or name.startswith('add')
        ):
        return True
    return False

def token_info(ttype, token, start, end, logiline):
    """
    Für Entwicklung/Debugging
    """
    print('%-20s %r (%r)' % ('%2d (%s):' % (ttype, tok_name[ttype]),
                             token, logiline))

# ------------------------ [ Statements, generiert von ApiFilter ... [
class Statement(object):
    """
    Ein von der ApiFilter-Umgebung verwendbares Statement
    """

    def __init__(self, tokens, transform=None):
        tokheads = []
        name = None
        args = []
        has_errors = 0
        for toktup in tokens:
            ttype, token = toktup[:2]
            if name is None:
                if ttype == NAME:
                    name = token
                elif ttype in (INDENT,):
                    continue
                else:
                    if not has_errors:
                        pp(('Hu?', {
                            'tokens:': tokens,
                            'toktup:': toktup[:2],
                            }))
                    token_info(*toktup)
                    print('%s: Name erwartet' % (toktup,))
                    has_errors += 1
            elif ttype not in (OP,
                               ):
                args.append(token)
            # weitere Informationen (toktup[2:]) verwerfen:
            tokheads.append((ttype, token))
        self.tokens = tokheads
        self.name = name
        self.args = args
        if transform is not None:
            self.transformed = True
            tokens2 = []
            for toktup in tokens:
                ttype, token = toktup[:2]
                if ttype == NAME:
                    token = transform(token)
                tokens2.append((ttype, token))

            self.tokens_transformed = tokens2
        else:
            self.transformed = False

    def __str__(self):
        if self.transformed:
            return untokenize(self.tokens_transformed)
        else:
            return untokenize(self.tokens)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, str(self))

    def tell(self):
        pp({'name': self.name,
            'args': self.args,
            'tokens': self.tokens,
            'tokens_pretty': resolve_tokens(self.tokens),
            })

class ControlStatement(Statement):
    """
    Zur Steuerung der API-Aufrufe
    """

class ApiCall(Statement):
    """
    API-Aufruf; Methoden- und sonstige Namen werden mit einem Präfix versehen
    """

class Assignment(Statement):
    """
    Assignment of a value to a config key

    To support the new PDFreactor API, which uses a config dictionary instead
    of the plethora of setter methods, we support statements like

      config.outputFormat = {
          type: OutputType.JPEG,
          width: 640,
      }

    which would be translated to something like

      dic = config.getdefault('outputFormat', {})
      dic.update({
          'type': PDFreactor.OutputType.JPEG,
          'width': 640,
          })

    """
# ------------------------ ] ... Statements, generiert von ApiFilter ]


# ------------------------------------------- [ Klasse ApiFilter ... [
class ApiFilter(object):
    """
    Erlaubt einen kontrollierten Zugriff auf eine API
    """

    def __init__(self,
                 config,
                 calls_before=None,
                 calls_default=None,
                 calls_after=None,
                 log=None,
                 msg=None,
                 check_methodname=None):
        """
        config -- the config dictionary to be given to the PDFreactor.convert
                  method; this is changed in-place.
        calls_before -- zu Beginn aufzurufende API-Aufrufe
                        (derzeit nicht verwendet)
        calls_default -- werden jeweils verwendet, sofern nicht dieselbe
                         Methode zuvor mit denselben *oder anderen* Argumenten
                         aufgerufen wurde
        calls_after -- abschließende API-Aufrufe; werden verwendet, sofern
                       nicht schon bei Abarbeitung der variablen Aufrufe
                       *identisch* erledigt (siehe __call__-Methode)
        symbols_map -- ein Dictionary, um z. B. Wahrheitswerte nach
                       Nicht-Python-Konventionen zu erkennen
        log -- eine Methode zum Loggen der Aufrufe
        msg -- der message-Adapter
        check_methodname -- eine Funktion, die API-Methodennamen daraufhin
                            prüft, ob ihre Verwendung erlaubt ist
        """
        self._config = config
        self.calls_before = calls_before
        self.calls_default = calls_default
        self.calls_after = calls_after
        self._log = log
        self._msg = msg
        self.check_methodname = check_methodname

    def log(self, *args, **kwargs):
        """
        Rufe die übergebene logger-Methode auf;
        ansonsten eine Notlösung
        """
        if self._log is not None:
            self._log(*args, **kwargs)
        else:
            print('#' * 79)
            print([(tup[0], repr(tup[1]))
                   for tup in kwargs.items()
                   ])
            print('#' * 79)
            print('(API)', ' '.join(map(repr, args)), \
                    ', '.join(['='.join((str(tup[0]), repr(tup[1]))
                                        )
                               for tup in kwargs.items()
                               ]))

    def msg(self, txt, type='info', mapping={}):
        """
        Rufe den Message-Adapter auf (wenn übergeben)
        """
        if self._msg is not None:
            self._msg(txt, type, mapping=mapping)

    def check_acceptable_name(self, name, **kwargs):
        """
        Der Name darf nur Buchstaben enthalten;
        außerdem sind einige Namen reserviert, um die korrekte Funktion
        sicherzustellen.

        """
        for ch in name:
            if not ch in letters:
                raise ValueError('Disallowed character %(ch)r'
                                 'in name %(name)r'
                                 % locals())
        if name in CONTROL_COMMANDS:
            raise ValueError('name %(name)r is reserved' % locals())
        if name in ('key', 'val', 'tup', 'prefix',
                    'statement', 'errors', 'found',
                    '_', 'translate', 'mogrify',
                    'text', 'errtext', 'ok', 'e',
                    'api_call',
                    # Zum Test dieser Funktionalität:
                    'verboten',
                    # Python-Standardfunktionen und -namen:
                    'str', 'isinstance',
                    'True', 'False', 'None', 'self',
                    ):
            raise ValueError('name %(name)r is reserved' % locals())

    def skip_this(self, stmt):
        """
        Gib True zurück, wenn sich Instanzen dieser ApiFilter-Klasse um das
        übergebene Statement prinzipiell nicht kümmern.
        """
        if isinstance(stmt, ControlStatement):
            return stmt.name != 'strict'
        elif isinstance(stmt, ApiCall):
            return stmt.name == 'setAddLinks'
        # was der Bauer nicht kennt ...:
        return True

    def _skip(self, stmt):
        if self.skip_this(stmt):
            self.log('%s: skipping %s' % (
                     self.__class__.__name__,
                     stmt))
            return True
        return False

    def _call_statement(self, stmt,
                        checkfunc=None):
        """
        Führe das übergebene Statement aus, sofern die bisherigen alle
        erfolgreich waren; andernfalls wird nur Versuch protokolliert, mit dem
        Vermerk 'Skip'.

        stmt -- ein Statement-Objekt
        checkfunc -- eine Funktion zur Prüfung, ob der übergebene Methodenname
                     zulässig ist. Wird nur beim Aufruf für die im Profil
                     konfigurierten, nicht für die hartcodierten Methoden
                     angegeben.

        Mit 'strict on' (Vorgabewert) ist der Versuch, eine unzulässige Methode
        aufzurufen, ein Fehler (und führt dazu, daß die weiteren nicht mehr
        ausgeführt werden).
        """
        if self._skip(stmt):
            return
        if isinstance(stmt, ApiCall):
            api_call = str(stmt)
            if not self._ctrl['ok']:
                errtext = _('Skipping %(api_call)r')
                self.log(errtext, locals())
                return
            if checkfunc is not None:
                if not checkfunc(stmt.name):
                    values = {'name': stmt.name,
                              }
                    self.msg('API method ${name} is disallowed', 'error', mapping=values)
                    self.log('API method %(name)r is disallowed', values)
                    if self._ctrl['strict']:
                        self._ctrl['ok'] = False
                        self.log('Remaining API calls will be skipped'
                                 '; PDF creation will be aborted')
                    return
            errtext = _('API call: %(api_call)s')
            self.log(errtext % locals())

            try:
                # erst das API-Objekt (den PDFreactor) lokal bekanntmachen:
                exec('%s=self._api_object' % self._api_name)
                # ... dann den Methodenaufruf:
                eval(api_call)
            except AttributeError as e:
                errtext = 'Unknown Attribute: %(e)r'
            except ValueError as e:
                errtext = 'Unknown Value: %(e)r'
            except NameError as e:
                errtext = 'Unknown Name: %(e)r'
            except Exception as e:
                e_name = e.__class__.__name__
                errtext = 'Unexpected Error (%(e_name)s): %(e)r'
            else:
                self.memorizeCall(stmt)
                return
            self.msg(_('API call ${api_call} failed'),
                     'error',
                     mapping=locals())
            self.log('E '+errtext, locals())
            self._ctrl['ok'] = False
            return
        elif isinstance(stmt, ControlStatement):
            if not self._ctrl['ok']:
                return
            # Bisher gibt es nur 'strict'.
            # Wenn es mehr werden, muß das evtl.
            # mal generischer gelöst werden:
            if stmt.name == 'strict':
                if stmt.args:
                    self._ctrl['strict'] = makeBool(stmt.args[0])
                else:
                    self._ctrl['strict'] = True
                self.log('i strict %s',
                         self._ctrl['strict'] and 'ON' or 'OFF')

    def memorizeCall(self, stmt):
        self._found.append((stmt.name, str(stmt)))

    def wasCalledBefore(self, stmt, exact):
        """
        Wurde das übergebene Statement zuvor schon aufgerufen?

        stmt -- das Statement
        exact -- Wahrheitswert
        """
        name = stmt.name
        filtered = [tup[1]
                    for tup in self._found
                    if tup[0] == name]
        if not exact:
            if filtered:
                self.log('Skipping %r: %r was called before',
                         str(stmt), name)
                return True
            else:
                return False
        else:
            s = str(stmt)
            if s in filtered:
                self.log('Skipping %r (was called before)',
                         s)
                return True
            elif filtered:
                self.log('Info: other calls of %r found',
                         name)
            return False

    def reset(self):
        self._found = []
        self._ctrl = {'strict': True,
                      'with_images': True,
                      'ok': True,
                      }

    def __call__(self, text,
                 **kwargs):
        """
        text -- zu interpretierender API-Text
        kwargs -- Es wird genau *ein* weiteres benanntes Argument erkannt;
                  dieses wird auch für das Präfix verwendet
        """
        if len(list(kwargs.keys())) != 1:
            raise ValueError('Expected exactly one named argument!'
                             ' (%s)' % kwargs)
        for tup in kwargs.items():
            key, val = tup
            self.check_acceptable_name(key)
            self._api_name = key
            self._api_object = val
            prefix = key + '.'
            break

        prefixed = make_prefixed(prefix)
        self.reset()

        checkfunc = self.check_methodname
        # text: Im Profil konfigurierte Aufrufe
        statements = list(gen_restricted_lines(text, prefixed))
        for statement in statements:
            self._call_statement(statement,
                                 checkfunc=checkfunc)
        # calls_default: Aufrufe von API-Methoden,
        # für die *keine* Aufrufe im Profil konfiguriert wurden
        for statement in gen_restricted_lines(self.calls_default, prefixed):
            if isinstance(statement, ControlStatement):
                # Kontrollanweisungen sind (vorerst?)
                # nur für konfigurierten Code gedacht:
                continue
            if not self.wasCalledBefore(statement, exact=False):
                self._call_statement(statement)
        # calls_after: Aufrufe von API-Methoden,
        #              die *exakt so* noch nicht erfolgt sind
        #              (aber nicht doppelt erfolgen sollen, wie z.B. das
        #              Hinzufügen von Skripten)
        for statement in gen_restricted_lines(self.calls_after, prefixed):
            if isinstance(statement, ControlStatement):
                # Kontrollanweisungen sind (vorerst?)
                # nur für konfigurierten Code gedacht:
                continue
            if not self.wasCalledBefore(statement, exact=True):
                self._call_statement(statement)

        return self._ctrl['ok']
# ------------------------------------------- ] ... Klasse ApiFilter ]


def fix(html, parser='lxml', from_encoding=None):
    """
    Gib eine geänderte und UTF-8-codierte Fassung des übergebenen HTML-Texts
    zurück.

    html -- der HTML-Text
    parser -- eine für BeautifulSoup 4 akzeptable Parser-Angabe
    from_encoding -- für den Fall, daß die automatische Erkennung versagt

    Literaturverweise werden geglättet und gesammelt:

    ><> uid = 'ccb9e2a26fc8ea71c567f0a39ddc4b85'
    ><> text = ('<html><body><p><a onclick="..." class="content-only" '
    ... 'href="./resolveuid/ccb9e2a26fc8ea71c567f0a39ddc4b85">[SteinD00]</a>')
    ><> fix(html)
    'DUMMY'
    """
    if from_encoding is not None:
        soup = BeautifulSoup(html, parser, from_encoding=from_encoding)
    else:
        soup = BeautifulSoup(html, parser)

    fix_literature(soup)
    return str(soup)


def fix_literature(soup):
    """
    Verarbeite Literaturlinks für die PDF-Ausgabe.

    soup -- das BeautifulSoup-Objekt, in-place geändert.
    """
    lit_list = []
    for a in soup.find_all('a', attrs={'class': 'content-only'}):
        text = a.get_text()
        if text.startswith('[') and text.endswith(']'):
            dic = {'text': text[1:-1],
                   }
            # TODO:
            # ... uid aus href extrahieren
            # ... onclick-Attribut entfernen
            # ... Änderungen (Element anhängen?), um Fußnoten zu erzeugen


"""<div class="attribute-text"><div class="clearfix layout-row columns-2"><div
class="layout-column first column-1"><p>Beim <strong>Abwasser</strong> handelt
es sich nach <a
onclick="window.open(this.href,'','resizable=yes,location=no,menubar=no,scrollbars=yes,status=no,toolbar=no,fullscreen=no,dependent=no,status,width=600,height=800');return
false;" href="./resolveuid/1749ea2e4c146dcfbf887e36dc14f357"
class="content-only BONK">[DINEN752g]</a> um ein Wasser, bestehend aus jeglicher Kombination von abgeleitetem Wasser aus Haushalten, Industrie- und Gewerbebetrieben, Oberflächenabfluss und unbeabsichtigtem Fremdwasserzufluss.</p></div> <div class="layout-column last column-2"><div style="text-align: left;">
 """

# ---------------------------------- [ Entwicklungsunterstützung ... [
def resolve_tokens(tokens):
    """
    Löse die numerischen Tokentypangaben auf.

    >>> tokens = [(1, 'toc'), (51, '('), (1, 'h1'), (51, ')')]
    >>> resolve_tokens(tokens)
    [('NAME', 'toc'), ('OP', '('), ('NAME', 'h1'), ('OP', ')')]
    """
    return [(tok_name[tup[0]], tup[1])
            for tup in tokens
            ]
# ---------------------------------- ] ... Entwicklungsunterstützung ]


if __name__ == '__main__':
  if 0:
      txt = '''
      strict on
      # don't forget that '.' OP:
      config.outputFormat = {
          type: OutputType.JPEG,
          width: 640,
      }
      '''
      # Standard library:
      from pprint import pprint

      # Logging / Debugging:
      from pdb import set_trace
      print(list(gen_restricted_lines(txt)))


      bogustxt = '''
      strict on
      # don't forget that '.' OP:
      config outputFormat = {
          type: OutputType.JPEG,
          width: 640,
      }
      '''
      print(list(gen_restricted_lines(bogustxt)))

      txt = '''
      strict on
      config.outputFormat = {
          type: OutputType.JPEG,
          width: 640,
      }
      '''
      set_trace() # b 104
      for tokens in gen_restricted_lines(txt):
          pprint(tokens)
          # pprint(resolve_tokens(tokens))

  else:
    # Standard library:
    import doctest
    doctest.testmod()
