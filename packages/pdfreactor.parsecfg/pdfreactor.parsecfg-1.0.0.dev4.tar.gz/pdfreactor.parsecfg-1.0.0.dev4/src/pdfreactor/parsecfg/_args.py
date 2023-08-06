# -*- coding: utf-8
"""
pdfreactor.parsecfg._args: Options evaluation

(helper functions for the .parse module)
"""

# Python compatibility:
from __future__ import absolute_import

from six import string_types as six_string_types

__author__ = "Tobias Herp <tobias.herp@visaplan.com>"


def extract_input_specs(args, kw):
    """
    Little options extraction helper; returns a dict.

    We expect a `text` or a `file` named option;
    if neither one is given, the first positional option is tried
    (which must be a string).

    >>> eis = extract_input_specs
    >>> eis([], {'text': 'some text'})
    {'text': 'some text'}
    >>> eis([], {'file': '<some file>'})
    {'file': '<some file>'}
    >>> eis([], {'text': 'some text',
    ...          'file': '<some file>'})
    Traceback (most recent call last):
      ...
    TypeError: Specified both a text and a file!
    >>> eis(('positional text',), {})
    {'text': 'positional text'}
    >>> eis((), {})
    Traceback (most recent call last):
      ...
    TypeError: Please specify a text or a file!

    >>> eis((42,), {})
    Traceback (most recent call last):
      ...
    TypeError: As positional input, we expect text; found <type 'int'>!

    If you specify a string instead of a list or tuple as a positional
    argument, you'll get:
    >>> eis('abc', {})
    Traceback (most recent call last):
      ...
    TypeError: Superfluous unnamed option(s)! ['b', 'c']
    >>> eis(['abc'], 'other crap')
    Traceback (most recent call last):
      ...
    TypeError: dict expected; got <type 'str'>!

    """
    res = {}
    if not isinstance(kw, dict):
        raise TypeError('dict expected; got %s!'
                        % (type(kw),
                           ))
    pop = kw.pop
    val = pop('text', None)
    if val is not None:
        res['text'] = val
    val = pop('file', None)
    if val is not None:
        if res:
            raise TypeError('Specified both a text and a file!')
        res['file'] = val
    if res:
        if args:
            raise TypeError('Unsupported unnamed option(s)!')
        return res
    if not args:
        raise TypeError('Please specify a text or a file!')
    elif isinstance(args, tuple):
        args = list(args)
    if not isinstance(args, list):
        args = list(args)
    val = args.pop(0)
    if isinstance(val, six_string_types):
        res['text'] = val
    else:
        raise TypeError('As positional input, we expect text; found %s!' % (
                        type(val),
                        ))
    if args:
        raise TypeError('Superfluous unnamed option(s)! %r'
                        % (args[:3],
                        ))
    return res


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
