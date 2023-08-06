# -*- coding: utf-8
"""
pdfreactor.parsecfg._statement: Statement class and generate_statements function

(helper class and generator for the .parse module)
"""

# Python compatibility:
from __future__ import absolute_import, print_function

from six import string_types as six_string_types
from six.moves import range, zip

__author__ = "Tobias Herp <tobias.herp@visaplan.com>"

# Standard library:
from collections import deque
# from tokenize import untokenize  (customize, perhaps?)
from tokenize import (
    COMMENT,
    ENDMARKER,
    INDENT,
    NAME,
    NEWLINE,
    NL,
    OP,
    STRING,
    TokenError,
    generate_tokens,
    tok_name,
    )

# visaplan:
from visaplan.tools.minifuncs import makeBool
from visaplan.tools.minifuncs import translate_dummy as _
from visaplan.tools.sequences import sequence_slide

# Local imports:
from pdfreactor.parsecfg._args import extract_input_specs
from pdfreactor.parsecfg._tokeninfo import TokenInfo
from pdfreactor.parsecfg._tokensgroup import TokensGroup, generate_token_groups

# from .oldmethods import map2
# from .oldsymbols import *


class Statement(list):
    """
    A class to represent a configuration statement which we'll interpret
    when using a textual configation to create (mainly) a config dictionary
    as expected e.g. by the PDFreactor.convert API method.

    For our logic, a Statement is just a list of TokensGroups
    (which may resemble e.g. a dotted name -- the main reason why we don't
    simply use tokens -- or an operator), which in turn are lists of TokenInfo
    objects.

    Given the following text:

    >>> txt = 'config.disableLinks = true'
    >>> groups = list(generate_token_groups(txt))
    >>> groups
    [<NAME config.disableLinks>, <OP '='>, <NAME true>, <ENDMARKER>]

    ... we can create the following statement (omitting that end marker):
    >>> stmt = Statement(groups[:-1])
    >>> stmt
    <Statement (config.disableLinks = true)>
    >>> stmt.is_assignment
    True
    >>> stmt.is_method_call
    False

    In the old (PDFreactor 7-) Python API, we had method calls:

    >>> txt = 'setAddLinks(true)'
    >>> groups = list(generate_token_groups(txt))
    >>> stmt = Statement(groups[:-1])
    >>> stmt
    <Statement (setAddLinks(true))>
    >>> stmt.is_assignment
    False
    >>> stmt.is_method_call
    True
    """

    def __repr__(self):
        return '<Statement (%(self)s)>' % locals()

    @property
    def is_assignment(self):
        if not self[1:]:
            return False
        grp2 = self[1]
        return grp2.ttype == OP and grp2.text == '='

    @property
    def is_method_call(self):
        if not self[1:]:
            return False
        name, op = self[:2]
        return name.ttype == NAME and op.ttype == OP and op.text == '('

    def __str__(self):
        liz = []
        ins, app = 0, 0
        for prev_tg, current_tg, next_tg in sequence_slide(self):
            current_ttype = current_tg.ttype
            current_text = current_tg.text
            if current_ttype == OP:
                if current_text == '=':
                    ins, app = (1, 1)
                elif current_text == ',':
                    if not next_tg.closes_brace:
                        ins, app = (0, 1)
                    elif next_tg.text == ')':
                        ins, app = (0, 0)
                    else:
                        continue
                elif current_tg.opens_brace:
                    ins, app = (0, 0)
                elif current_tg.closes_brace:
                    ins, app = (0, 0)
                else:
                    ins, app = (0, 1)
            elif (current_ttype == NAME
                  and next_tg is not None
                  and next_tg.ttype == NAME
                  ):
                ins, app = (0, 1)
            else:
                ins, app = (0, 0)
            if ins:
                liz.append(' ')
            liz.append(current_text)
            if app and next_tg is not None:
                liz.append(' ')
        return ''.join(liz)


def generate_statements(*args, **kwargs):
    """
    Parse an input text and generate statements.

    We use the generate_token_groups function internally;
    why not use the same input data for our doctests?

    >>> def lost(txt):
    ...     return list(generate_statements(txt))
    >>> txt = 'config.disableLinks = true'
    >>> stmts = lost(txt)
    >>> stmts
    [<Statement (config.disableLinks = true)>]
    >>> stmt = stmts[0]
    >>> stmt.is_assignment
    True

    At this stage, we are not picky about what we accept;
    we are prepared to accept old (PDFreactor v7-) API method names
    and proprietary control statements:

    >>> txt = '''# some comment
    ... strict on
    ... setAddLinks(False); # another comment
    ... with_images off
    ... '''
    >>> lost(txt)                             # doctest: +NORMALIZE_WHITESPACE
    [<Statement (strict on)>,
     <Statement (setAddLinks(False))>,
     <Statement (with_images off)>]

    >>> txt2 = '''
    ... setAddLinks(False)
    ... # Enable bookmarks in the PDF document
    ... setAddBookmarks(True)
    ... setCleanupTool(CLEANUP_NONE)
    ... setEncoding('UTF-8')
    ... setJavaScriptMode(JAVASCRIPT_MODE_ENABLED_NO_LAYOUT)
    ... '''
    >>> lost(txt2)
    ...                                       # doctest: +NORMALIZE_WHITESPACE
    [<Statement (setAddLinks(False))>,
     <Statement (setAddBookmarks(True))>,
     <Statement (setCleanupTool(CLEANUP_NONE))>,
     <Statement (setEncoding('UTF-8'))>,
     <Statement (setJavaScriptMode(JAVASCRIPT_MODE_ENABLED_NO_LAYOUT))>]

    Of course, the conversion to the respective new API config assignments is
    not done here, where we just do some educated parsing.

    We may put multiple statements in one line, separated by semicolons:

    >>> txt3 = '; ;setA();setB()'
    >>> lost(txt3)
    ...                                       # doctest: +NORMALIZE_WHITESPACE
    [<Statement (setA())>,
     <Statement (setB())>]

    Comments work as expected, of course:

    >>> txt3c = 'setA();#setB()'
    >>> lost(txt3c)
    ...                                       # doctest: +NORMALIZE_WHITESPACE
    [<Statement (setA())>]

    We mainly expect to see assignments for the current PDFreactor API
    which we support in convenient fashion.

    Instead of something like:

    >>> txt4py = '''
    ... config['outputFormat'] = {
    ...     'type': PDFreactor.OutputType.JPEG,
    ...     'width': 640,
    ...     }
    ... '''

    (which is what you'll get in the end,
    and which might be supported by a future release),
    you may specify:

    >>> txt4 = '''
    ... config.outputFormat = {
    ...     type: OutputType.JPEG,
    ...     width: 640,
    ... }
    ... '''
    >>> lost(txt4)                            # doctest: +NORMALIZE_WHITESPACE
    [<Statement (config.outputFormat = {type:  OutputType.JPEG,
                                        width: 640})>]

    or:
    >>> txt5 = '''
    ... config.outputFormat.type = OutputType.JPEG
    ... config.outputFormat.width = 640
    ... '''
    >>> lost(txt5)                            # doctest: +NORMALIZE_WHITESPACE
    [<Statement (config.outputFormat.type = OutputType.JPEG)>,
     <Statement (config.outputFormat.width = 640)>]

    We can parse the Python assignment, however:
    >>> stmts = lost(txt4py)
    >>> stmts                                 # doctest: +NORMALIZE_WHITESPACE
    [<Statement (config['outputFormat'] =
        {'type': PDFreactor.OutputType.JPEG,
         'width': 640})>]

    We just don't recognize it as an assigment yet:
    >>> stmts[0].is_assignment                # doctest: +NORMALIZE_WHITESPACE
    False

    Now for our example configuration for server-side creation of appendixes
    and tables of contents (not implemented here).
    This is what it could be configured:
    >>> lost(
    ... '''toc (".headline-level-2", ".headline-level-3",
    ... ".headline-level-4")
    ... appendix (
    ... #  glossary,  (commented out)
    ...   images,
    ...   formulas,
    ... )
    ... ''')                                  # doctest: +NORMALIZE_WHITESPACE
    [<Statement (toc(".headline-level-2",
                     ".headline-level-3",
                     ".headline-level-4"))>,
     <Statement (appendix(images,
                          formulas,))>]

    Remember, the actual processing is not part of this package;
    but you get an idea of what you could do.
    """
    input_specs = extract_input_specs(args, kwargs)
    token_groups = generate_token_groups(**input_specs)
    buf = []
    for prev_grp, grp, next_grp in sequence_slide(token_groups):
        if grp.is_terminator:
            if not buf:
                continue
            elif prev_grp.opens_brace:
                pass
            elif prev_grp.ttype == OP and prev_grp.text == ',':
                pass
            else:
                yield Statement(buf)
                buf = []
            continue
        buf.append(grp)
    assert not buf, "We get always a trailing terminator, right?!"


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
