"""
pdfreactor.parsecfg: Configuration parser for PDFreactor client integrations
"""

# Python compatibility:
from __future__ import absolute_import, print_function

# from ._parse import make_parser, ControlStatement, ApiCall

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
