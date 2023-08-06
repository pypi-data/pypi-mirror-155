# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

__author__ = """Tobias Herp <tobias.herp@visaplan.com>"""

from Products.CMFCore.utils import getToolByName
from zope.interface import implementer

# Plone:
from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFPlone.interfaces import INonInstallable

# visaplan:
from visaplan.plone.tools.setup import step, load_and_cook

from .plone.defaults import (
    default_connection as conn,
    default_config as config,
    )
from .plone.interfaces import IPdfReactorConnection, IPdfReactorSettings

# ------------------------------------------------------- [ data ... [
PROJECTNAME = 'pdfreactor-api'
PROFILE_ID = PROJECTNAME + ':default'
LOGGER_LABEL = PROJECTNAME + ': setuphandlers'
# ------------------------------------------------------- ] ... data ]

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

    registry.registerInterface(IPdfReactorConnection)
    logger.info('Registered interface %r', IPdfReactorConnection)
    proxy = registry.forInterface(IPdfReactorConnection)
    for key in default_connection.keys():
        if key in proxy:
            val = proxy[key]
            logger.info('Found %(key)s = %(val)r', locals())
        else:
            proxy[key] = val = None
            logger.info('Set %(key)s to %(val)r', locals())

    registry.registerInterface(IPdfReactorSettings)
    logger.info('Registered interface %r', IPdfReactorSettings)
    proxy = registry.forInterface(IPdfReactorSettings)
    for key, val in default_connection.items():
        if key in proxy:
            val = proxy[key]
            logger.info('Found %(key)s = %(val)r', locals())
        else:
            proxy[key] = val
            logger.info('Set %(key)s to %(val)r', locals())
