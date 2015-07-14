from plone.restapi.interfaces import IAPIRequest
from plone.restapi.interfaces import IPUT
from plone.restapi.interfaces import IGET
from plone.restapi.interfaces import IPOST
from plone.restapi.interfaces import IDELETE
from plone.restapi.interfaces import IOPTIONS
from plone.restapi.interfaces import IPATCH
from zope.interface import alsoProvides


def mark_as_api_request(context, event):
    """Mark a request with Content-Type 'application/json' with the IAPIRequest
       interface.
    """
    if event.request.getHeader('Content-Type') == 'application/json':
        alsoProvides(event.request, IAPIRequest)
        if event.request.get('REQUEST_METHOD') == 'PUT':
            alsoProvides(event.request, IPUT)
        if event.request.get('REQUEST_METHOD') == 'DELETE':
            alsoProvides(event.request, IDELETE)
        if event.request.get('REQUEST_METHOD') == 'GET':
            alsoProvides(event.request, IGET)
        if event.request.get('REQUEST_METHOD') == 'POST':
            alsoProvides(event.request, IPOST)
        if event.request.get('REQUEST_METHOD') == 'OPTIONS':
            alsoProvides(event.request, IOPTIONS)
        if event.request.get('REQUEST_METHOD') == 'PATCH':
            alsoProvides(event.request, IPATCH)
