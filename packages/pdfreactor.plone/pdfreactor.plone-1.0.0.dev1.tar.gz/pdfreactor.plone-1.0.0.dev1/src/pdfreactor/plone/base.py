"""
@@as.pdf browser: simple PDF export
"""

from urllib import urlencode

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.interface import implements

from pdfreactor.api import PDFreactor

from pdfreactor.plone.interfaces import IExporter
from pdfreactor.plone.interfaces import IPdfReactorConnectionSettings


class Exporter(BrowserView):

    implements(IExporter)

    def __init__(self, context, request):
        """
        Create the browser view, using the configured connection settings
        """
        super(Exporter, self).__init__(context, request)
        self.reactor = self.make_reactor(context)

    def make_reactor(self, context):
        """
        Create the PDFreactor object which we'll use for our conversions
        """
        registry = getToolByName(context, 'portal_registry')
        proxy = registry.forInterface(IPdfReactorConnectionSettings)
        url = proxy.service_url or None
        reactor = PDFreactor(url)
        key = proxy.api_key or None
        if key is not None:
            reactor.apiKey = key
        return reactor

    def conversionSettings(self):
        """
        Create the config dictionary, as expected e.g. by the PDFrector.convert
        method.

        There are two options to customize this:

        - Inherit from this class and override the conversionSettings method
        - Override the 'pdfreactor-config' browser.
        """
        context = aq_inner(self.context)
        view = getMultiAdapter((context, self.request),
                               name='pdfreactor-config')
        return view()

    def connectionSettings(self):
        """
        Return a {'headers': ..., 'cookies': ...} dict

        E.g. to create PDF documents from restricted contents,
        we need to provide cookies.

        For the basic backend configuration, see the make_reactor method.
        """
        request = self.request
        cookies = request.cookies
        return {
            'cookies': cookies,
            }

    def conversion_url(self):
        """
        Return the URL to be fed to the PDFreactor service
        """
        return self.context.absolute_url()

    def __call__(self):
        """
        Send a request to the configured PDFreactor service, and return the PDF

        This is a simple sulution for small exports which the user and her/his
        web browser is willing to wait for.
        For cases where browser timeouts are likely to occur, you should use
        asynchronous conversion.
        """
        pdfReactor = self.reactor
        config = self.conversionSettings()
        config.update({
            'document': self.conversion_url(),
            })
        conn = self.connectionSettings()
        kw = {
            'config': config,
            'connectionSettings': conn,
            }
        result = pdfReactor.convertAsBinary(**kw)
        setHeader = self.request.response.setHeader
        setHeader("Content-type", "application/pdf")
        title = self.context.Title
        if callable(title):
            title = title()
        fname = title.strip()+'.pdf'
        setHeader('Content-Disposition', 'attachment; filename="%s"' % fname)
        return result
