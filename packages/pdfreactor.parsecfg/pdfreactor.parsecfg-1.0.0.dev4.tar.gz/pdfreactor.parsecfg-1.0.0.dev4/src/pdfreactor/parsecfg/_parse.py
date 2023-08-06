# -*- coding: utf-8
"""
pdfreactor.parsecfg._parse: Configuration parser for PDFreactor client integrations
"""

# Python compatibility:
from __future__ import absolute_import, print_function

from six.moves import range, zip
from six.moves import StringIO

# from six.moves import map, range

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

# Logging / Debugging:
from visaplan.tools.debug import pp

# from .oldmethods import map2
# from .oldsymbols import *

__all__ = [
    'make_parser',
    ]

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
    Create a `prefixed` function to prepend symbol names with a prefix:

    >>> f = make_prefixed('PDFreactor')
    >>> f('SomeKnownSymbol')
    'PDFreactor.SomeKnownSymbol'

    Some aliases to important Python builtins, however, are converted to their
    Python names and not prefixed:

    >>> f('on')
    'True'
    >>> f('no')
    'False'
    >>> f('null')
    'None'

    We accept integer numbers:

    >>> f('1')
    '1'

    ... but no floats etc.:

    >>> f('4.2')
    Traceback (most recent call last):
      ...
    ValueError: invalid literal for int() with base 10: '4.2'

    We can choose not to inject a prefix:

    >>> f2 = make_prefixed(None)
    >>> f2('SomeKnownSymbol')
    'SomeKnownSymbol'
    >>> f2('NIL')
    'None'
    >>> f2('1.23')
    Traceback (most recent call last):
      ...
    ValueError: invalid literal for int() with base 10: '1.23'
    """
    if not prefix:
        prefix = ''
    elif not prefix.endswith('.'):
        prefix += '.'
    def prefixed(token):
        if token[0] in '0123456789':
            int(token)
            return token
        ltoken = token.lower()
        if ltoken in SYMBOLS_MAP:
            return SYMBOLS_MAP[ltoken]
        else:
            return prefix + token
    return prefixed


def make_parser(**kwargs):
    """
    Create a parser for PDFreactor client configurations:

    >>> parse = make_parser()

    In the basic case, the parser will understand comment lines;
    it returns a 3-tuple (config, deletions, unused).
    If we don't have special 'control commands', and don't need to apply
    changes to existing configurations, we might be interested in the first
    part only:

    >>> def p0(txt):
    ...     return sorted(parse(txt)[0].items())
    >>> txt = '''# some comment
    ... config.outputFormat = {
    ...     type: OutputType.JPEG,
    ...     width: 640,
    ... }
    ... '''
    >>> parse(txt)
    >>> p0(txt) # doctest: +NORMALIZE_WHITESPACE
    [('type', 'OutputType.JPEG'),
     ('width': 640)]


    """
    pop = kwargs.pop
    prefix = pop('prefix', None)
    commands = pop('commands', None)
    if commands is None:
        commands = set([])
    elif isinstance(commands, str):
        commands = set(commands.split())

    if kwargs:
        invalid = list(kwargs.keys())
        many = bool(invalid[1:])
        raise TypeError('Unsupported option%s: %r%s' % (
                many and 's' or '',
                invalid[0],
                many and ' ...' or '',
                ))

    prefixed = make_prefixed(prefix)

    def parse(txt):
        """
        Return a 3-tuple:

        config -- a dict, as expected e.g. by the PDFreactor.convert method
        deletions -- keys which have been found to be obsolete during
                     processing; not implemented yet.
        unused -- control statements and (suspected) API methods which have not
                  been converted to config dict changes.
        """
        res = {}
        deletions = []
        unused = []
        for statement in gen_restricted_lines(txt, prefixed):
            if isinstance(statement, Assignment):
                key, val = supported_assignment(statement)
                if isinstance(val, dict):
                    dest = res.getdefault(key, {})
                    dest.update(val)
                else:
                    res[key] = val
            elif 0:  # no deletions implemented yet
                pass
            else:
                unused.append(statement)

        return res, deletions, unused

    return parse


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
    def key_and_value(self, skip):
        tokens = self.tokens
        if skip is not None:
            for toktup, chunk in zip(tokens, skip):
                if chunk is None:
                    continue  # accept anything
                elif toktup[1] != chunk:
                    raise ValueError('Expected %(chunk)r; found %(toktup)s!'
                            % locals())
            tokens = tokens[len(skip):]
        if not tokens:
            raise ValueError('Empty assignment: %(self)r' % locals())
        _name = []
        _isdic = None
        _done = 0
        _left_complete = 0
        _braces = []  # a stack of braces
        _thiskey = None
        _thisval = []
        _thedict = None

        for toktup in tokens:
            _typ, _val = toktup
            if _done:
                raise ValueError('Too much: %(toktup)s!' % locals())
            if _typ == OP:
                if not _name:
                    raise ValueError('No name yet!')
                elif _val == '=':
                    if _left_complete:
                        raise ValueError('Duplicate "="!')
                    _left_complete = 1
                elif _val == '{':
                    if not _left_complete:
                        raise ValueError('%(_val)r found but no = yet!'
                                % locals())
                    assert _left_complete
                    if _isdic is not None:
                        raise ValueError('Found %(_val)r,'
                                ' with _isdic == %(_isdic)r'
                                % locals())
                    _isdic = True
                    _thedict = {}
                elif _val == ';':
                    _done = 1
                else:
                    raise ValueError('%(toktup)r not supported yet' % locals())
            elif _left_complete:
                _thisval.append(_val)
            else:
                _name.append(_val)

        return (
            ''.join(_name),
            _thedict if   _isdic
                     else ''.join(_thisval))
# ------------------------ ] ... Statements, generiert von ApiFilter ]


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

def supported_assignment(stmt):
    """
    Take an Assignment (to some config key)
    and return a (key, value) tuple.

    >>> txt1 = 'config.disableLinks = True'
    >>> seq1 = list(gen_restricted_lines(txt1))
    >>> stmt1 = Assignment(seq1[0])
    >>> supported_statement(stmt1)
    ('disableLinks', True)
    """
    if stmt.name != 'config':
        raise ValueError('We support only assignments to config keys!'
                         " (%r != 'config')" % (
                         stmt.name,
                         ))
    pp(stmt.tokens)
    return stmt.key_and_value(skip=(None, '.'))


if __name__ == '__main__':
  if 1:
      txt1 = '''
      # don't forget that '.' OP:
      config.disableLinks = true
      '''
      stmts = list(gen_restricted_lines(txt1))
      stmt = stmts[0]
      print(stmt)
      kw = {'skip': (None, '.')}
      # Logging / Debugging:
      from pdb import set_trace
      set_trace()
      tup = stmt.key_and_value(**kw)
      print(tup)

      txt2 = '''
      # don't forget that '.' OP:
      config.outputFormat = {
          type: OutputType.JPEG,
      '''
  elif 0:
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

