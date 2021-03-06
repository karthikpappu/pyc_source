# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.freebsd-7.1-PRERELEASE-i386/egg/Products/ProxyIndex/tests/testProxyIndex.py
# Compiled at: 2008-08-08 04:07:43
__doc__ = '\nbasic for proxy index using different delegated indexes\n\nauthor: kapil thangavelu <k_vertigo@objectrealms.net>\n\n'
from Testing import ZopeTestCase
import unittest, os, sys, whrandom, string, random
from OFS.SimpleItem import SimpleItem
from DateTime import DateTime
from Products.CMFCore.tests.base.testcase import SecurityRequestTest
from Products.ZCatalog import ZCatalog, Vocabulary
from Products.ZCatalog.Catalog import Catalog, CatalogError
from Products.PluginIndexes.FieldIndex.FieldIndex import FieldIndex
from Products.PluginIndexes.TextIndex.TextIndex import TextIndex
from Products.PluginIndexes.TextIndex.Lexicon import Lexicon
from Products.PluginIndexes.KeywordIndex.KeywordIndex import KeywordIndex
from Products.PluginIndexes.DateIndex.DateIndex import DateIndex
from Products.ZCTextIndex.ZCTextIndex import ZCTextIndex, PLexicon
from Products.ZCTextIndex.Lexicon import Splitter
from Products.ZCTextIndex.Lexicon import CaseNormalizer, StopWordRemover
ZopeTestCase.installProduct('ZCatalog')
ZopeTestCase.installProduct('ZCTextIndex')
ZopeTestCase.installProduct('ProxyIndex')
query_time = DateTime()
text = [
 "Here's a knocking indeed! If a\n    man were porter of hell-gate, he should have\n    old turning the key.  knock (that made sure\n    sure there's at least one word in common).", "Knock,\n    knock, knock! Who's there, i' the name of\n    Beelzebub? Here's a farmer, that hanged\n    himself on the expectation of plenty: come in\n    time; have napkins enow about you; here\n    you'll sweat for't."]

class TestObject(SimpleItem):
    __module__ = __name__

    def __init__(self, id, body=''):
        self.id = id
        self.body = body

    def SearchableText(self):
        return self.body


class ProxyIndexTests(ZopeTestCase.ZopeTestCase):
    __module__ = __name__

    def afterSetUp(self):
        catalog = ZCatalog.ZCatalog('portal_catalog')
        self.app._setObject('portal_catalog', catalog)
        self.app.portal_catalog.manage_addProduct['ZCatalog'].manage_addVocabulary('Vocabulary', 'test vocabulary', globbing=1)
        self.app.portal_catalog._setObject('lexicon', PLexicon('lexicon', '', Splitter(), CaseNormalizer(), StopWordRemover()))
        self.cat = self.app.portal_catalog
        self.addProxyIndex = self.cat.manage_addProduct['ProxyIndex'].manage_addProxyIndex
        self.app._setObject('test1', TestObject('test1', text[0]))
        self.app._setObject('test2', TestObject('test2', text[1]))

    def testProxyWFieldIndex(self):
        self.addProxyIndex('field_id', idx_type=FieldIndex.meta_type, value_expr='python: object.getId()')
        test1_ob = getattr(self.app, 'test1')
        test2_ob = getattr(self.app, 'test2')
        self.cat.catalog_object(test1_ob)
        self.cat.catalog_object(test2_ob)
        res = self.cat(field_id='test1')
        self.assertEqual(len(res), 1, 'field index should match only 1 object')

    def testProxyWDateIndex(self):
        self.addProxyIndex('mod_date', idx_type=DateIndex.meta_type, value_expr='object/bobobase_modification_time')
        test1_ob = getattr(self.app, 'test1')
        test2_ob = getattr(self.app, 'test2')
        self.cat.catalog_object(test1_ob)
        self.cat.catalog_object(test2_ob)
        res = self.cat(mod_date={'query': query_time, 'range': 'min'})
        self.assertEqual(len(res), 2, 'date index query should have found 2 objects')

    def testProxyWTextIndex(self):
        self.addProxyIndex('searchable_text', idx_type=TextIndex.meta_type, value_expr='object/SearchableText')
        test1_ob = getattr(self.app, 'test1')
        test2_ob = getattr(self.app, 'test2')
        self.cat.catalog_object(test1_ob)
        self.cat.catalog_object(test2_ob)
        res = self.cat(searchable_text='farmer')
        self.assertEqual(len(res), 1, 'Invalid Search Results for TextIndex')

    def testProxyWZCTextIndex(self):
        self.addProxyIndex('zc_text', idx_type=ZCTextIndex.meta_type, value_expr='object/SearchableText', doc_attr='proxy_value', lexicon_id='lexicon', index_type='Cosine Measure')
        test1_ob = getattr(self.app, 'test1')
        test2_ob = getattr(self.app, 'test2')
        self.cat.catalog_object(test1_ob)
        self.cat.catalog_object(test2_ob)
        res = self.cat(zc_text='gate')
        self.assertEqual(len(res), 1, 'Invalid Search Results for ZCTextIndex')

    def testSearchAll(self):
        self.addProxyIndex('zc_text', idx_type=ZCTextIndex.meta_type, value_expr='object/SearchableText', doc_attr='proxy_value', lexicon_id='lexicon', index_type='Cosine Measure')
        test1_ob = getattr(self.app, 'test1')
        test2_ob = getattr(self.app, 'test2')
        self.cat.catalog_object(test1_ob)
        self.cat.catalog_object(test2_ob)
        res = self.cat()
        self.assertEqual(len(res), 2, 'invalid search all results')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ProxyIndexTests))
    return suite


if __name__ == '__main__':
    unittest.main()