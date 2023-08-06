"""
@@pdfreactor-config browser: very basic configuration
"""

from Products.Five.browser import BrowserView
from zope.interface import implements

from pdfreactor.plone.interfaces import IGetPdfReactorConversionSettings
from pdfreactor.defaults import default_config


class DefaultSettingsView(BrowserView):
    """
    Return a very basic `config` dict e.g. for PDFreactor.convert
    """
    
    implements(IGetPdfReactorConversionSettings)

    def __call__(self):
        return default_config.copy()
