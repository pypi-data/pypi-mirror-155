# -*- coding: utf-8
"""
pdfreactor.parsecfg.parse: Configuration parser for PDFreactor client integrations

This module publishes the parsing functionality, based on the Python standard
tokenize module;  this includes two generators and three helper classes.

For the actual conversion to a config dictionary, see the convert module.
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

# Local imports:
from pdfreactor.parsecfg._statement import Statement, generate_statements
from pdfreactor.parsecfg._tokeninfo import TokenInfo
from pdfreactor.parsecfg._tokensgroup import TokensGroup, generate_token_groups

# from .oldmethods import map2
# from .oldsymbols import *


__all__ = [
    'generate_statements',	# ./_statement.py
    # helper functions:
    'generate_token_groups',	# ./_tokensgroup.py
    # helper classes:
    'TokenInfo',	# ./_tokeninfo.py
    'TokensGroup', 	# ./_tokensgroup.py
    'Statement',	# ./_statement.py
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
