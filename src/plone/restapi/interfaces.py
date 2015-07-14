# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IPloneRestapiLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IAPIRequest(Interface):
    """Marker for API requests.
    """


class ISerializeToJson(Interface):
    """Adapter to serialize a Dexterity object into a JSON object.
    """


class IGET(Interface):
    """ Get method
    """


class IPOST(Interface):
    """ Post method
    """


class IPUT(Interface):
    """ Put method
    """


class IDELETE(Interface):
    """ Delete method
    """


class IOPTIONS(Interface):
    """ Options method
    """


class IPATCH(Interface):
    """ Patch method
    """
