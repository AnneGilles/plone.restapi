# -*- coding: utf-8 -*-
from zope.interface import Interface


class IAPIRequest(Interface):
    """Marker for API requests.
    """


class ISerializeToJson(Interface):
    """Adapter to serialize a Dexterity object into a JSON object.
    """

class IPut(Interface):
    """Put method
    """

class IDelete(Interface):
    """Delete method
    """