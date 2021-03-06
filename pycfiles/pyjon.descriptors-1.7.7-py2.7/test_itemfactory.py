# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyjon/descriptors/tests/test_itemfactory.py
# Compiled at: 2015-01-20 06:40:20
from six import next
import unittest
from pyjon.descriptors.readers import ItemFactory
from pyjon.descriptors.readers import CSVReader
from pyjon.descriptors.readers import InputDialect
from pyjon.descriptors.casters import Caster
from pyjon.descriptors.tests.test_utils import basetestdir
from pyjon.descriptors.tests.test_utils import open_file
from xml.etree import cElementTree as ET
import datetime, csv

class TestItemFactory(unittest.TestCase):

    def test_invalid_schema_missingname(self):
        schema_filename = '%s/DESC_TEST_invalid_missingname.xml' % basetestdir
        schemaroot = ET.parse(schema_filename)
        caster = Caster()
        self.assertRaises(KeyError, ItemFactory, schemaroot, 'utf-8', caster)

    def test_invalid_schema_missingmandatory(self):
        schema_filename = '%s/DESC_TEST_invalid_missingmandatory.xml' % basetestdir
        schemaroot = ET.parse(schema_filename)
        caster = Caster()
        self.assertRaises(KeyError, ItemFactory, schemaroot, 'utf-8', caster)

    def test_invalid_prerenderer(self):
        schema_filename = '%s/DESC_TEST_invalid_prerender.xml' % basetestdir
        schemaroot = ET.parse(schema_filename)
        caster = Caster()
        self.assertRaises(ValueError, ItemFactory, schemaroot, 'utf-8', caster)

    def test_prerenderer_eval(self):
        """the prerenderer with type eval should have access to the raw_value
        and should be able to modify it so that the item factory processes only
        the prerendered value instead of the raw data
        """
        schema_filename = '%s/DESC_TEST_prerender_eval.xml' % basetestdir
        sourcefilename = '%s/csv_date_prerenderer_test.csv' % basetestdir
        source = open_file(sourcefilename, 'r')
        schemaroot = ET.parse(schema_filename)
        encoding = 'utf-8'
        reader_shell = CSVReader(encoding, schemaroot)
        caster = Caster()
        factory = ItemFactory(schemaroot, encoding, caster)
        dialect = InputDialect(reader_shell.separator)
        csv_reader = csv.reader(source, dialect)
        header = next(csv_reader)
        del header
        row = next(csv_reader)
        item = factory.create_item(row, record_num=1)
        self.assertEquals(item.Field1, 'C000301')
        self.assertEquals(item.Field2, datetime.date(2008, 5, 22))
        row = next(csv_reader)
        item = factory.create_item(row, record_num=2)
        self.assertEquals(item.Field1, '611380')
        self.assertEquals(item.Field2, datetime.date(2008, 5, 21))
        row = next(csv_reader)
        item = factory.create_item(row, record_num=3)
        self.assertEquals(item.Field1, '611380')
        self.assertEquals(item.Field2, datetime.date(2008, 5, 5))
        source.close()

    def test_prerenderer_eval_implicit(self):
        """the prerenderer with no type will be of type eval
        """
        schema_filename = '%s/DESC_TEST_prerender_eval_implicit.xml' % basetestdir
        sourcefilename = '%s/csv_date_prerenderer_test.csv' % basetestdir
        source = open_file(sourcefilename, 'r')
        schemaroot = ET.parse(schema_filename)
        encoding = 'utf-8'
        reader_shell = CSVReader(encoding, schemaroot)
        caster = Caster()
        factory = ItemFactory(schemaroot, encoding, caster)
        dialect = InputDialect(reader_shell.separator)
        csv_reader = csv.reader(source, dialect)
        header = next(csv_reader)
        del header
        row = next(csv_reader)
        item = factory.create_item(row, record_num=1)
        self.assertEquals(item.Field1, 'C000301')
        self.assertEquals(item.Field2, datetime.date(2008, 5, 22))
        row = next(csv_reader)
        item = factory.create_item(row, record_num=2)
        self.assertEquals(item.Field1, '611380')
        self.assertEquals(item.Field2, datetime.date(2008, 5, 21))
        row = next(csv_reader)
        item = factory.create_item(row, record_num=3)
        self.assertEquals(item.Field1, '611380')
        self.assertEquals(item.Field2, datetime.date(2008, 5, 5))
        source.close()

    def test_prerenderer_eval_raises(self):
        """the prerenderer with type eval raise a ValueError if the evaluation
        goes south
        """
        schema_filename = '%s/DESC_TEST_prerender_eval_invalid.xml' % basetestdir
        sourcefilename = '%s/csv_date_prerenderer_test.csv' % basetestdir
        source = open_file(sourcefilename, 'r')
        schemaroot = ET.parse(schema_filename)
        encoding = 'utf-8'
        reader_shell = CSVReader(encoding, schemaroot)
        caster = Caster()
        factory = ItemFactory(schemaroot, encoding, caster)
        dialect = InputDialect(reader_shell.separator)
        csv_reader = csv.reader(source, dialect)
        header = next(csv_reader)
        del header
        row = next(csv_reader)
        self.assertRaises(ValueError, factory.create_item, row, record_num=1)
        source.close()

    def test_prerenderer_function(self):
        """the prerenderer with type function should have access to
        the raw_value and should be able to modify it so that the item
        factory processes only the prerendered value instead of the raw data
        """
        schema_filename = '%s/DESC_TEST_prerender_function.xml' % basetestdir
        sourcefilename = '%s/csv_date_prerenderer_test.csv' % basetestdir
        source = open_file(sourcefilename, 'r')
        schemaroot = ET.parse(schema_filename)
        encoding = 'utf-8'
        reader_shell = CSVReader(encoding, schemaroot)
        caster = Caster()
        factory = ItemFactory(schemaroot, encoding, caster)
        dialect = InputDialect(reader_shell.separator)
        csv_reader = csv.reader(source, dialect)
        header = next(csv_reader)
        del header
        row = next(csv_reader)
        item = factory.create_item(row, record_num=1)
        self.assertEquals(item.Field1, 'C000301')
        self.assertEquals(item.Field2, datetime.date(2008, 5, 22))
        row = next(csv_reader)
        item = factory.create_item(row, record_num=2)
        self.assertEquals(item.Field1, '611380')
        self.assertEquals(item.Field2, datetime.date(2008, 5, 21))
        row = next(csv_reader)
        item = factory.create_item(row, record_num=3)
        self.assertEquals(item.Field1, '611380')
        self.assertEquals(item.Field2, datetime.date(2008, 5, 5))
        source.close()