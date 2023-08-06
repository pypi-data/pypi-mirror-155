"""
pdfreactor.parsecfg.defaults: default values
"""

# Python compatibility:
from __future__ import absolute_import

from pdfreactor.defaults import default_config as _cfg

default_config_text = """\
disableLinks = %(disableLinks)r
""" % _cfg
