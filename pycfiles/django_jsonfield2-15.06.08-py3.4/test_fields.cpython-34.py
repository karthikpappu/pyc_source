# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jsonfield2/tests/test_fields.py
# Compiled at: 2015-06-04 10:41:05
# Size of source mod 2**32: 6829 bytes
from django.test import TestCase as DjangoTestCase
from django.utils.encoding import force_text
from django import forms
from jsonfield2.tests.jsonfield_test_app.models import *
from jsonfield2.fields import JSONField

class JSONFieldTest(DjangoTestCase):

    def test_json_field(self):
        obj = JSONFieldTestModel(json='{\n            "spam": "eggs"\n        }')
        self.assertEqual(obj.json, {'spam': 'eggs'})

    def test_json_field_empty(self):
        obj = JSONFieldTestModel(json='')
        self.assertEqual(obj.json, None)

    def test_json_field_save(self):
        JSONFieldTestModel.objects.create(id=10, json='{\n                "spam": "eggs"\n            }')
        obj2 = JSONFieldTestModel.objects.get(id=10)
        self.assertEqual(obj2.json, {'spam': 'eggs'})

    def test_json_field_save_empty(self):
        JSONFieldTestModel.objects.create(id=10, json='')
        obj2 = JSONFieldTestModel.objects.get(id=10)
        self.assertEqual(obj2.json, None)

    def test_db_prep_save(self):
        field = JSONField('test')
        field.set_attributes_from_name('json')
        self.assertEqual(None, field.get_db_prep_save(None, connection=None))
        self.assertEqual('{"spam": "eggs"}', field.get_db_prep_save({'spam': 'eggs'}, connection=None))

    def test_formfield(self):
        from jsonfield2.forms import JSONFormField
        from jsonfield2.widgets import JSONWidget
        field = JSONField('test')
        field.set_attributes_from_name('json')
        formfield = field.formfield()
        self.assertEqual(type(formfield), JSONFormField)
        self.assertEqual(type(formfield.widget), JSONWidget)

    def test_formfield_clean_blank(self):
        field = JSONField('test')
        formfield = field.formfield()
        self.assertRaisesMessage(forms.ValidationError, force_text(formfield.error_messages['required']), formfield.clean, value='')

    def test_formfield_clean_none(self):
        field = JSONField('test')
        formfield = field.formfield()
        self.assertRaisesMessage(forms.ValidationError, force_text(formfield.error_messages['required']), formfield.clean, value=None)

    def test_formfield_null_and_blank_clean_blank(self):
        field = JSONField('test', null=True, blank=True)
        formfield = field.formfield()
        self.assertEqual(formfield.clean(value=''), '')

    def test_formfield_null_and_blank_clean_none(self):
        field = JSONField('test', null=True, blank=True)
        formfield = field.formfield()
        self.assertEqual(formfield.clean(value=None), None)

    def test_formfield_blank_clean_blank(self):
        field = JSONField('test', null=False, blank=True)
        formfield = field.formfield()
        self.assertEqual(formfield.clean(value=''), '')

    def test_formfield_blank_clean_none(self):
        field = JSONField('test', null=False, blank=True)
        formfield = field.formfield()
        self.assertEqual(formfield.clean(value=None), None)

    def test_default_value(self):
        obj = JSONFieldWithDefaultTestModel.objects.create()
        obj = JSONFieldWithDefaultTestModel.objects.get(id=obj.id)
        self.assertEqual(obj.json, {'sukasuka': 'YAAAAAZ'})

    def test_query_object(self):
        JSONFieldTestModel.objects.create(json={})
        JSONFieldTestModel.objects.create(json={'foo': 'bar'})
        self.assertEqual(2, JSONFieldTestModel.objects.all().count())
        self.assertEqual(1, JSONFieldTestModel.objects.exclude(json={}).count())
        self.assertEqual(1, JSONFieldTestModel.objects.filter(json={}).count())
        self.assertEqual(1, JSONFieldTestModel.objects.filter(json={'foo': 'bar'}).count())
        self.assertEqual(1, JSONFieldTestModel.objects.filter(json__contains={'foo': 'bar'}).count())
        JSONFieldTestModel.objects.create(json={'foo': 'bar',  'baz': 'bing'})
        self.assertEqual(2, JSONFieldTestModel.objects.filter(json__contains={'foo': 'bar'}).count())
        self.assertEqual(2, JSONFieldTestModel.objects.filter(json__contains='foo').count())
        self.assertRaises(TypeError, lambda : JSONFieldTestModel.objects.filter(json__contains=['baz', 'foo']))

    def test_query_isnull(self):
        JSONFieldTestModel.objects.create(json=None)
        JSONFieldTestModel.objects.create(json={})
        JSONFieldTestModel.objects.create(json={'foo': 'bar'})
        self.assertEqual(1, JSONFieldTestModel.objects.filter(json=None).count())
        self.assertEqual(None, JSONFieldTestModel.objects.get(json=None).json)

    def test_jsonfield_blank(self):
        BlankJSONFieldTestModel.objects.create(blank_json='', null_json=None)
        obj = BlankJSONFieldTestModel.objects.get()
        self.assertEqual(None, obj.null_json)
        self.assertEqual('', obj.blank_json)
        obj.save()
        obj = BlankJSONFieldTestModel.objects.get()
        self.assertEqual(None, obj.null_json)
        self.assertEqual('', obj.blank_json)

    def test_callable_default(self):
        CallableDefaultModel.objects.create()
        obj = CallableDefaultModel.objects.get()
        self.assertEqual({'x': 2}, obj.json)

    def test_callable_default_overridden(self):
        CallableDefaultModel.objects.create(json={'x': 3})
        obj = CallableDefaultModel.objects.get()
        self.assertEqual({'x': 3}, obj.json)

    def test_mutable_default_checking(self):
        obj1 = JSONFieldWithDefaultTestModel()
        obj2 = JSONFieldWithDefaultTestModel()
        obj1.json['foo'] = 'bar'
        self.assertNotIn('foo', obj2.json)

    def test_invalid_json(self):
        obj = JSONFieldTestModel()
        obj.json = '{"foo": 2}'
        self.assertIn('foo', obj.json)
        with self.assertRaises(forms.ValidationError):
            obj.json = '{"foo"}'

    def test_invalid_json_default(self):
        with self.assertRaises(ValueError):
            JSONField('test', default='{"foo"}')

    def test_indent(self):
        JSONField('test', indent=2)

    def test_string_is_valid_json(self):
        JSONFieldTestModel.objects.create(json='"foo"')
        self.assertEqual('foo', JSONFieldTestModel.objects.get().json)


class SavingModelsTest(DjangoTestCase):

    def test_saving_null(self):
        obj = BlankJSONFieldTestModel.objects.create(blank_json='', null_json=None)
        self.assertEqual('', obj.blank_json)
        self.assertEqual(None, obj.null_json)