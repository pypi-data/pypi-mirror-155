"""
@@pdfreactor-config: parsed global settings
"""

# Python compatibility:
from __future__ import absolute_import

# Setup tools:
import pkg_resources

try:
    pkg_resources.get_distribution('pdfreactor.plone')
except pkg_resources.DistributionNotFound:
    HAVE_PDFREACTORPLONE = 0
else:
    HAVE_PDFREACTORPLONE = 1

# Zope:
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.interface import implements

from pdfreactor.api import PDFreactor

# Local imports:
from pdfreactor.parsecfg.plone.interfaces import (
    IGetSettings,
    IPdfReactorConversionSettings,
    )

if HAVE_PDFREACTORPLONE:
    from pdfreactor.plone.config import DefaultSettingsView as BaseSettingsView
else:
    from Products.Five.browser import BrowserView as BaseSettingsView

# Local imports:
from ..convert import parse_configuration


class SettingsView(BaseSettingsView):

    implements(IGetSettings)  # usually IGetPdfReactorConversionSettings from
                              # pdfreactor.plone.interfaces

    def __call__(self):
        """
        Get the PDFreactor config(uration) settings as configured in the Plone
        registry.  You might want to inject contextual configuration changes as
        well.
        """
        context = aq_inner(self.context)
        registry = getToolByName(context, 'portal_registry')
        dic = registry.forInterface(IPdfReactorConversionSettings)
        config_text = dic.config_text
        config = parse_configuration(config_text)
        return config
