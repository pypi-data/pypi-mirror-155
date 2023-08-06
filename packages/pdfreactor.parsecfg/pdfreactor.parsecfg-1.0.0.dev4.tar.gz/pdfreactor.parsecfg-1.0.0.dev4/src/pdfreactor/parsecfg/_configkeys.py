# -*- coding: utf-8
"""
pdfreactor.parsecfg._configkeys: info about PDFreactor config keys

vim:
%s;^\(\s\+\)\('[^',]\+'\):;\1(\2,):;
"""

_factories = {
        ('disableLinks',): bool,
        ('outputFormat',): dict,
        ('outputFormat', 'type'): str,
        ('outputFormat', 'width'): int,
        ('outputFormat', 'height'): int,
        }
