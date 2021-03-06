# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/archetypes/schematuning/tests/test_fields.py
# Compiled at: 2010-01-22 07:59:46
import os
from OFS.Image import File, Image
from DateTime import DateTime
from zope.interface import implements
from zope.component import getSiteManager
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from Products import PortalTransforms
from Products.Archetypes import Field as at_field
from Products.Archetypes.Field import ScalableImage
from Products.Archetypes.atapi import *
from Products.Archetypes.interfaces import IFieldDefaultProvider
from Products.Archetypes.interfaces.vocabulary import IVocabulary
from Products.Archetypes.tests.atsitetestcase import portal_name
from Products.Archetypes.tests.utils import PACKAGE_HOME
from Products.Archetypes.tests.utils import mkDummyInContext
from archetypes.schematuning.tests.base import SchemaTuningTestCase
test_fields = [
 ('ObjectField', 'objectfield'), ('StringField', 'stringfield'), ('FileField', 'filefield'), ('TextField', 'textfield'), ('DateTimeField', 'datetimefield'), ('LinesField', 'linesfield'), ('IntegerField', 'integerfield'), ('FloatField', 'floatfield'), ('FixedPointField', 'fixedpointfield1'), ('FixedPointField', 'fixedpointfield2'), ('BooleanField', 'booleanfield'), ('ImageField', 'imagefield'), ('PhotoField', 'photofield')]
field_instances = []
for (type, name) in test_fields:
    field_instances.append(getattr(at_field, type)(name))

txt_file = open(os.path.join(PACKAGE_HOME, 'input', 'rest1.rst'))
txt_content = txt_file.read()
img_file = open(os.path.join(PACKAGE_HOME, 'input', 'tool.gif'), 'rb')
img_content = img_file.read()
field_values = {'objectfield': 'objectfield', 'stringfield': 'stringfield', 'filefield_file': txt_file, 'textfield': 'textfield', 'datetimefield': '', 'datetimefield_year': '2003', 'datetimefield_month': '01', 'datetimefield_day': '01', 'datetimefield_hour': '03', 'datetimefield_minute': '04', 'linesfield': 'bla\nbla', 'integerfield': '1', 'floatfield': '1.5', 'fixedpointfield1': '1.5', 'fixedpointfield2': '1,5', 'booleanfield': '1', 'imagefield_file': img_file, 'photofield_file': img_file}
expected_values = {'objectfield': 'objectfield', 'stringfield': 'stringfield', 'filefield': txt_content, 'textfield': 'textfield', 'datetimefield': DateTime('2003-01-01 03:04'), 'linesfield': ('bla', 'bla'), 'integerfield': 1, 'floatfield': 1.5, 'fixedpointfield1': '1.50', 'fixedpointfield2': '1.50', 'booleanfield': 1, 'imagefield': '<img src="%s/dummy/imagefield" alt="Spam" title="Spam" height="16" width="16" />' % portal_name, 'photofield': '<img src="%s/dummy/photofield/variant/original" alt="" title="" height="16" width="16" border="0" />' % portal_name}
empty_values = {'objectfield': None, 'stringfield': '', 'filefield': None, 'textfield': '', 'datetimefield': '2007-00-00', 'linesfield': (), 'integerfield': None, 'floatfield': None, 'fixedpointfield1': None, 'fixedpointfield2': None, 'booleanfield': None}
schema = Schema(tuple(field_instances))
sampleDisplayList = DisplayList([('e1', 'e1'), ('element2', 'element2')])

class sampleInterfaceVocabulary:
    __module__ = __name__
    __implements__ = IVocabulary

    def getDisplayList(self, instance):
        return sampleDisplayList


class Dummy(BaseContentMixin):
    __module__ = __name__

    def Title(self):
        return 'Spam'

    def aMethod(self):
        return sampleDisplayList

    def default_val(self):
        return 'World'


class DummyVocabulary(object):
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary.fromItems([('title1', 'value1'), ('t2', 'v2')])


DummyVocabFactory = DummyVocabulary()

class FakeRequest:
    __module__ = __name__

    def __init__(self):
        self.other = {}
        self.form = {}


class ProcessingTest(SchemaTuningTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.setRoles(['Manager'])
        SchemaTuningTestCase.afterSetUp(self)
        self._dummy = mkDummyInContext(Dummy, oid='dummy', context=self.portal, schema=schema)
        txt_file.seek(0)
        img_file.seek(0)

    def makeDummy(self):
        self._dummy.invalidateSchema()
        return self._dummy

    def test_processing(self):
        dummy = self.makeDummy()
        request = FakeRequest()
        request.form.update(field_values)
        dummy.REQUEST = request
        dummy.processForm(data=1)
        for (k, v) in expected_values.items():
            got = dummy.getField(k).get(dummy)
            if isinstance(got, File):
                got = str(got)
            self.assertEquals(got, v, 'got: %r, expected: %r, field "%s"' % (got, v, k))

    def test_processing_fieldset(self):
        dummy = self.makeDummy()
        request = FakeRequest()
        request.form.update(field_values)
        request.form['fieldset'] = 'default'
        dummy.REQUEST = request
        dummy.processForm()
        for (k, v) in expected_values.items():
            got = dummy.getField(k).get(dummy)
            if isinstance(got, (File, ScalableImage, Image)):
                got = str(got)
            self.assertEquals(got, v, 'got: %r, expected: %r, field "%s"' % (got, v, k))

    def test_get_size(self):
        dummy = self.makeDummy()
        request = FakeRequest()
        request.form.update(field_values)
        request.form['fieldset'] = 'default'
        dummy.REQUEST = request
        dummy.processForm()
        size = 0
        for (k, v) in expected_values.items():
            field = dummy.getField(k)
            s = field.get_size(dummy)
            size += s
            self.failUnless(s, 'got: %s, field: %s' % (s, k))

        self.failUnlessEqual(size, dummy.get_size())

    def test_validation(self):
        dummy = self.makeDummy()
        request = FakeRequest()
        request.form.update(field_values)
        request.form['fieldset'] = 'default'
        dummy.REQUEST = request
        errors = {}
        dummy.validate(errors=errors)
        self.failIf(errors, errors)

    def test_required(self):
        request = FakeRequest()
        request.form.update(empty_values)
        request.form['fieldset'] = 'default'
        self._test_required(request)

    def test_required_empty_request(self):
        request = FakeRequest()
        request.form = {}
        request.form['fieldset'] = 'default'
        self._test_required(request)

    def _test_required(self, request):
        dummy = self.makeDummy()
        f_names = []
        schema = dummy.Schema()
        for f in schema.fields():
            name = f.getName()
            f.required = 1
            f_names.append(name)

        errors = {}
        dummy.validate(REQUEST=request, errors=errors)
        self.failUnless(errors, 'Errors dictionary is empty.')
        err_fields = errors.keys()
        failures = []
        for f_name in f_names:
            if f_name not in err_fields:
                failures.append(f_name)

        self.failIf(failures, '%s failed to report error.' % failures)

    def test_static_vocabulary(self):
        dummy = self.makeDummy()
        request = FakeRequest()
        field = dummy.Schema().fields()[0]
        self.failUnlessEqual(field.Vocabulary(), DisplayList())
        field.vocabulary = sampleDisplayList()
        dummy.invalidateSchema()
        self.failUnlessEqual(field.Vocabulary(), sampleDisplayList)
        field.vocabulary = [
         'e1', 'element2']
        dummy.invalidateSchema()
        self.failUnlessEqual(field.Vocabulary(), sampleDisplayList)
        field.vocabulary = [
         ('e1', 'e1'), ('element2', 'element2')]
        dummy.invalidateSchema()
        self.failUnlessEqual(field.Vocabulary(), sampleDisplayList)

    def test_dynamic_vocabulary(self):
        dummy = self.makeDummy()
        request = FakeRequest()
        field = dummy.Schema().fields()[0]
        self.failUnlessEqual(field.Vocabulary(dummy), DisplayList())
        field.vocabulary = 'aMethod'
        dummy.invalidateSchema()
        self.failUnlessEqual(field.Vocabulary(dummy), sampleDisplayList)
        field.vocabulary = sampleDisplayList()
        dummy.invalidateSchema()
        self.failUnlessEqual(field.Vocabulary(dummy), sampleDisplayList)
        field.vocabulary = [
         'e1', 'element2']
        dummy.invalidateSchema()
        self.failUnlessEqual(field.Vocabulary(dummy), sampleDisplayList)
        field.vocabulary = [
         ('e1', 'e1'), ('element2', 'element2')]
        dummy.invalidateSchema()
        self.failUnlessEqual(field.Vocabulary(dummy), sampleDisplayList)
        field.vocabulary = sampleInterfaceVocabulary()
        dummy.invalidateSchema()
        self.failUnlessEqual(field.Vocabulary(dummy), sampleDisplayList)

    def test_factory_vocabulary(self):
        dummy = self.makeDummy()
        request = FakeRequest()
        field = dummy.Schema().fields()[0]
        self.failUnlessEqual(field.Vocabulary(dummy), DisplayList())
        expected = DisplayList([('value1', 'title1'), ('v2', 't2')])
        field.vocabulary = ()
        field.vocabulary_factory = 'archetypes.tests.dummyvocab'
        dummy.invalidateSchema()
        getSiteManager().registerUtility(component=DummyVocabFactory, name='archetypes.tests.dummyvocab')
        self.failUnlessEqual(field.Vocabulary(dummy), expected)
        getSiteManager().unregisterUtility(component=DummyVocabFactory, name='archetypes.tests.dummyvocab')

    def test_defaults(self):
        dummy = self.makeDummy()
        request = FakeRequest()
        field = dummy.Schema().fields()[0]
        self.failUnlessEqual(field.getDefault(dummy), None)
        field.default = 'Hello'
        self.failUnlessEqual(field.getDefault(dummy), 'Hello')
        field.default = None
        field.default_method = 'default_val'
        self.failUnlessEqual(field.getDefault(dummy), 'World')
        field.default_method = None

        class DefaultFor(object):
            __module__ = __name__
            implements(IFieldDefaultProvider)

            def __init__(self, context):
                self.context = context

            def __call__(self):
                return 'Adapted'

        getSiteManager().registerAdapter(factory=DefaultFor, required=(Dummy,), name=field.__name__)
        self.failUnlessEqual(field.getDefault(dummy), 'Adapted')
        getSiteManager().unregisterAdapter(factory=DefaultFor, required=(Dummy,), name=field.__name__)
        return


class DownloadTest(SchemaTuningTestCase):
    __module__ = __name__

    def afterSetUp(self):
        SchemaTuningTestCase.afterSetUp(self)
        self.dummy = mkDummyInContext(Dummy, oid='dummy', context=self.portal, schema=schema)
        self.field = self.dummy.getField('textfield')
        ptpath = PortalTransforms.__path__[0]
        self.wordfile = open('%s/tests/input/test.doc' % ptpath)
        self.field.getMutator(self.dummy)(self.wordfile.read())
        self.request = self.app.REQUEST
        self.response = self.request.response

    def test_download_from_textfield(self):
        value = self.field.download(self.dummy, no_output=True)
        self.failIf(isinstance(value, str))

    def test_download_filename_encoding(self):
        self.field.setFilename(self.dummy, 'überzeugen')
        self.field.download(self.dummy, no_output=True)
        self.assertEqual(self.response.headers['content-disposition'], 'attachment; filename="uberzeugen"')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ProcessingTest))
    suite.addTest(makeSuite(DownloadTest))
    return suite