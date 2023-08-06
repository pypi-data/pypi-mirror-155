# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

__author__ = """Tobias Herp <tobias.herp@visaplan.com>"""

# Zope:
from Missing import Value as MissingValue
from Products.CMFCore.utils import getToolByName
from zope.interface import implementer

# Plone:
from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFPlone.interfaces import INonInstallable

# visaplan:
from visaplan.plone.tools.setup import step

# Local imports:
from pdfreactor.parsecfg.defaults import default_config_text
from pdfreactor.parsecfg.plone.interfaces import IPdfReactorConversionSettings

# ------------------------------------------------------- [ data ... [
PROJECTNAME = 'pdfreactor.parsecfg'
PROFILE_ID = PROJECTNAME + ':default'
LOGGER_LABEL = PROJECTNAME + ': setuphandlers'
# ------------------------------------------------------- ] ... data ]

# Logging / Debugging:
import logging

logger = logging.getLogger(LOGGER_LABEL)


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            PROJECTNAME + ':uninstall',
        ]


def post_install(context):
    """Post install script"""
    logger.info('Installation complete')

    # Do something at the end of the installation of this package.


@step
def register_settings(context, logger):
    registry = getToolByName(context, 'portal_registry')

    registry.registerInterface(IPdfReactorConversionSettings)
    logger.info('Registered interface %r', IPdfReactorConversionSettings)
    proxy = registry.forInterface(IPdfReactorConversionSettings)
    key = 'config_text'
    early_return = 0
    late_return = 1
    if early_return:
        return
    val = getattr(proxy, key, None)
    if val not in (None, MissingValue):
        logger.info('Found %(key)s = %(val)r', locals())
    elif late_return:
        logger.warn('No value yet for key %(key)s!', locals())
    else:
        val = default_config_text.strip()
        setattr(proxy, key, val)
        logger.info('Set %(key)s to %(val)r', locals())
