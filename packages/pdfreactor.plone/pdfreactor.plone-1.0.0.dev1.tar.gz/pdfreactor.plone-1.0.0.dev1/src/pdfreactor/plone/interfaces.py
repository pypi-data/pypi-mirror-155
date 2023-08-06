"""
pdfreactor.plone.interfaces

For the IPdfReactorConversionSettings interface, see the pdfreactor.parsecfg package
"""

# Zope:
from zope import schema
from zope.interface import Interface

# Plone:
from plone.supermodel import model

from pdfreactor.defaults import default_connection as conn


# ------------------------ [ marker interfaces for browser views ... [
class IExporter(Interface):
    """
    For browser views to provide a PDF export of the given context
    """


class IAsynchronousExporter(Interface):
    """
    For browser views to provide an asynchronous PDF export of the given context

    This won't yield the PDF document directly but instead return some JSON
    data to access it once it is ready.
    """


class IGetPdfReactorConversionSettings(Interface):
    """
    Return a very basic, non-configurable config dict.
    """
    # We don't define a similar interface for the connection settings here
    # because we don't expect so much customization regarding this aspect;
    # it should be enough to  
# ------------------------ ] ... marker interfaces for browser views ]


class IPdfReactorConnectionSettings(model.Schema):
    """
    Configuration for the PDFreactor backend
    """
    service_url = schema.URI(
        title=u"URL of the PDFreactor service",
        default=conn['service_url'],
        description=(u'Adjust the address of your PDFreactor service here; '
            u'default value is %(service_url)r.'
            ) % conn)

    api_key = schema.ASCII(
        title=u"API key for the PDFreactor service",
        default=conn['api_key'],
        description=(u'Enter your API key here (some XML text "<license>...'
            u'</license>", containing a signature).'
            u'This is not strictly necessary, e.g. if the license is installed '
            u'on the server, or when evaluating.'
            ) % conn)
