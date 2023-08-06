# -*- coding: utf-8
"""
pdfreactor.parsecfg.symbols: known symbols of the current API

Instead of inspecting the PDFreactor class at runtime, we put the data in some
convenient dict object(s).
"""

# Python compatibility:
from __future__ import absolute_import

__all__ = [
    'SYMBOL_STRINGS',
    # 'SYMBOL_TUPLES',  (removed)
    'SIMPLE_SYMBOLS',
    ]

# Standard library:
from inspect import isclass

from pdfreactor.api import PDFreactor

# we'll see which one we'll use ..
SYMBOL_STRINGS = {}


for clsname in dir(PDFreactor):
    subclass = getattr(PDFreactor, clsname)
    if isclass(subclass):
        for symname in dir(subclass):
            if symname.startswith('_'):
                continue
            symbol = getattr(subclass, symname)
            if callable(symbol):
                raise ValueError('found callable %(symbol)r in %(subclass)r!'
                                 % locals())
            tup = (clsname, symname)
            key = '.'.join(tup)
            SYMBOL_STRINGS[key] = symbol

SIMPLE_SYMBOLS = {}
for val, keys in [
        (True,  ('True',  'on', 'yes')),
        (False, ('False', 'off', 'no')),
        (None,  ('None',  'null', 'nothing', 'nil')),
        ]:
    for key in keys:
        SIMPLE_SYMBOLS[key.lower()] = val

if __name__ == '__main__':
    # Standard library:
    from pprint import pprint
    pprint(SYMBOL_STRINGS)
    # pprint(SIMPLE_SYMBOLS)
