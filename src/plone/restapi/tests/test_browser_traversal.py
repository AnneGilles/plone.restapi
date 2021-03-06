# -*- coding: utf-8 -*-
from plone.restapi.testing import PLONE_RESTAPI_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from plone.testing.z2 import Browser

from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import unittest

import json
import os
import requests
import transaction


class TestTraversal(unittest.TestCase):

    layer = PLONE_RESTAPI_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', id='document1')
        self.document = self.portal.document1
        self.document_url = self.document.absolute_url()
        self.portal.invokeFactory('Folder', id='folder1')
        self.folder = self.portal.folder1
        self.folder_url = self.folder.absolute_url()
        transaction.commit()
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_json_view_document_traversal(self):
        self.browser.open(self.document_url + '/@@json')
        self.assertTrue(json.loads(self.browser.contents))
        self.assertEqual(
            json.loads(self.browser.contents).get('@id'),
            self.document_url + '/@@json'
        )

    def test_json_view_folder_traversal(self):
        self.browser.open(self.folder_url + '/@@json')
        self.assertTrue(json.loads(self.browser.contents))
        self.assertEqual(
            json.loads(self.browser.contents).get('@id'),
            self.folder_url + '/@@json'
        )

    def test_json_view_site_root_traversal(self):
        self.browser.open(self.portal_url + '/@@json')
        self.assertTrue(json.loads(self.browser.contents))
        self.assertEqual(
            json.loads(self.browser.contents).get('@id'),
            self.portal_url + '/@@json'
        )

    def test_document_traversal(self):
        response = requests.get(
            self.document_url,
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get('content-type'),
            'application/json',
            'When sending a GET request with Accept: application/json ' +
            'the server should respond with sending back application/json.'
        )
        self.assertEqual(
            response.json()['@id'],
            self.document_url
        )

    def test_news_item_traversal(self):
        self.portal.invokeFactory('News Item', id='news1')
        image_file = os.path.join(os.path.dirname(__file__), u'image.png')
        self.portal.news1.image = NamedBlobImage(
            data=open(image_file, 'r').read(),
            contentType='image/png',
            filename=u'image.png'
        )
        self.portal.news1.image_caption = u'This is an image caption.'
        transaction.commit()
        response = requests.get(
            self.portal.news1.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get('content-type'),
            'application/json',
            'When sending a GET request with content-type: application/json ' +
            'the server should respond with sending back application/json.'
        )
        self.assertEqual(
            response.json()['@id'],
            self.portal.news1.absolute_url()
        )
        self.assertEqual(
            u'This is an image caption.',
            response.json()['image_caption']
        )
        self.assertEqual(
            u'http://localhost:55001/plone/news1/@@images/image',
            response.json()['image']
        )

    def test_folder_traversal(self):
        response = requests.get(
            self.folder_url,
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get('content-type'),
            'application/json',
            'When sending a GET request with content-type: application/json ' +
            'the server should respond with sending back application/json.'
        )
        self.assertEqual(
            response.json()['@id'],
            self.folder_url
        )

    def test_site_root_traversal(self):
        response = requests.get(
            self.portal_url,
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get('content-type'),
            'application/json',
            'When sending a GET request with content-type: application/json ' +
            'the server should respond with sending back application/json.'
        )
        self.assertEqual(
            response.json()['@id'],
            self.portal_url
        )

    def test_site_root_traversal_with_default_page(self):
        self.portal.invokeFactory('Document', id='front-page')
        self.portal.setDefaultPage('front-page')
        transaction.commit()
        response = requests.get(
            self.portal_url,
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get('content-type'),
            'application/json',
            'When sending a GET request with content-type: application/json ' +
            'the server should respond with sending back application/json.'
        )
        self.assertEqual(
            response.json()['@id'],
            self.portal_url
        )

    @unittest.skip('Not implemented yet.')
    def test_file_traversal(self):  # pragma: no cover
        self.portal.invokeFactory('File', id='file1')
        self.portal.file1.title = 'File'
        self.portal.file1.description = u'A file'
        pdf_file = os.path.join(
            os.path.dirname(__file__), u'file.pdf'
        )
        self.portal.file1.file = NamedBlobFile(
            data=open(pdf_file, 'r').read(),
            contentType='application/pdf',
            filename=u'file.pdf'
        )
        intids = getUtility(IIntIds)
        file_id = intids.getId(self.portal.file1)
        self.portal.file1.file = RelationValue(file_id)
        transaction.commit()
        response = requests.get(
            self.portal.file1.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get('content-type'),
            'application/json',
            'When sending a GET request with content-type: application/json ' +
            'the server should respond with sending back application/json.'
        )
        self.assertEqual(
            response.json()['@id'],
            self.portal.file1.absolute_url()
        )

    @unittest.skip('Not implemented yet.')
    def test_image_traversal(self):  # pragma: no cover
        self.portal.invokeFactory('Image', id='img1')
        self.portal.img1.title = 'Image'
        self.portal.img1.description = u'An image'
        image_file = os.path.join(os.path.dirname(__file__), u'image.png')
        self.portal.img1.image = NamedBlobImage(
            data=open(image_file, 'r').read(),
            contentType='image/png',
            filename=u'image.png'
        )
        transaction.commit()
        response = requests.get(
            self.portal.img1.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get('content-type'),
            'application/json',
            'When sending a GET request with content-type: application/json ' +
            'the server should respond with sending back application/json.'
        )
        self.assertEqual(
            response.json()['@id'],
            self.portal.img1.absolute_url()
        )
