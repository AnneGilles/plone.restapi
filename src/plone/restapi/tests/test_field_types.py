# -*- coding: utf-8 -*-
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.fti import DexterityFTI
from plone.namedfile.field import NamedBlobFile as NamedBlobFileInterface
from plone.namedfile.file import NamedBlobFile
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.testing import PLONE_RESTAPI_INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName

import unittest2 as unittest
import zope.schema
import json


class IAllFieldTypes(IDexterityContent):

    field_type_namedblobfile = NamedBlobFileInterface(
        title=u"Please upload a file",
        required=False,
    )

    field_type_list = zope.schema.List(
        title=u"List",
        value_type=zope.schema.TextLine(),
        missing_value=[],
        default=[],
        required=False,
    )

    text = zope.schema.Text(
        title=u'Text',
        required=False,
    )

    textline = zope.schema.TextLine(
        title=u'TextLine',
        required=False,
    )


class TestFieldTypes(unittest.TestCase):

    layer = PLONE_RESTAPI_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        fti = DexterityFTI('AllFieldTypes')
        fti._updateProperty(
            'schema',
            'plone.restapi.tests.test_adapter_file.'
            'IFileDocument'
        )
        types_tool = getToolByName(self.portal, "portal_types")
        types_tool._setObject('AllFieldTypes', fti)
        self.portal.invokeFactory('AllFieldTypes', 'doc')

    def test_field_types_choice(self):
        pass

    def test_field_types_bytes(self):
        pass

    def test_field_types_ascii(self):
        pass

    def test_field_types_bytesline(self):
        pass

    def test_field_types_asciiline(self):
        pass

    def test_field_types_text(self):
        self.portal.doc.text = u'Lorem Ipsum'
        self.assertEqual(
            u'Lorem Ipsum',
            json.loads(ISerializeToJson(self.portal.doc)).get('text')
        )

    def test_field_types_textline(self):
        self.portal.doc.textline = u'Lorem Ipsum'
        self.assertEqual(
            u'Lorem Ipsum',
            json.loads(ISerializeToJson(self.portal.doc)).get('textline')
        )

    def test_field_types_bool(self):
        pass

    def test_field_types_int(self):
        pass

    def test_field_types_float(self):
        pass

    def test_field_types_tuple(self):
        pass

    def test_field_types_list(self):
        pass

    def test_field_types_set(self):
        pass

    def test_field_types_frozenset(self):
        pass

    def test_field_types_password(self):
        pass

    def test_field_types_dict(self):
        pass

    def test_field_types_datetime(self):
        pass

    def test_field_types_date(self):
        pass

    def test_field_types_timedelta(self):
        pass

    def test_field_types_sourcetext(self):
        pass

    def test_field_types_object(self):
        pass

    def test_field_types_uri(self):
        pass

    def test_field_types_id(self):
        pass

    def test_field_types_dottedname(self):
        pass

    def test_field_types_interfacefield(self):
        pass

    def test_field_types_decimal(self):
        pass

    def test_namedblobfile(self):
        pass

    def test_field_types_namedblobimage(self):
        pass

    def test_field_types_relation(self):
        pass

    def test_field_types_relationlist(self):
        pass

    def test_field_types_relationchoice(self):
        pass

    def test_field_types_richtext(self):
        pass
