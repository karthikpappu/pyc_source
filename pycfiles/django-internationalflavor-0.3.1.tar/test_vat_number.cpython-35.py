# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ralph/Development/django-internationalflavor/tests/test_vat_number.py
# Compiled at: 2016-04-08 16:44:15
# Size of source mod 2**32: 5119 bytes
from __future__ import unicode_literals
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.test import TestCase
from internationalflavor.vat_number import VATNumberValidator
from internationalflavor.vat_number.forms import VATNumberFormField
from internationalflavor.vat_number.models import VATNumberField

class VATNumberTestCase(TestCase):
    valid = {'NL820646660B01': 'NL820646660B01', 
     'NL82064-6660.B01': 'NL820646660B01', 
     'DE 114 103 379': 'DE114103379', 
     'DE114103379': 'DE114103379', 
     'BE 0203.201.340': 'BE0203201340'}
    invalid = {'NL820646661B01': ['This VAT number does not match the requirements for NL.'], 
     'BE0203201341': ['This VAT number does not match the requirements for BE.'], 
     'DE11410337': ['This VAT number does not match the requirements for DE.'], 
     'US123414132': ['US VAT numbers are not allowed in this field.'], 
     '123456': ['This VAT number does not start with a country code, or contains invalid characters.'], 
     'IE0É12345A': ['This VAT number does not start with a country code, or contains invalid characters.']}

    def test_validator(self):
        validator = VATNumberValidator()
        for iban, cleaned in self.valid.items():
            if iban == cleaned:
                validator(iban)
            else:
                validator(cleaned)
                self.assertRaises(ValidationError, validator, iban)

        for iban, message in self.invalid.items():
            self.assertRaisesMessage(ValidationError, message[0], validator, iban)

    def test_form_field(self):
        self.assertFieldOutput(VATNumberFormField, valid=self.valid, invalid=self.invalid)

    def test_model_field(self):
        model_field = VATNumberField()
        for input, output in self.valid.items():
            self.assertEqual(model_field.clean(input, None), output)

        for input, errors in self.invalid.items():
            with self.assertRaises(ValidationError) as (context_manager):
                model_field.clean(input, None)
            self.assertEqual(context_manager.exception.messages, errors[::-1])

    include_countries = ('NL', 'BE')
    include_countries_valid = {'NL820646660B01': 'NL820646660B01', 
     'BE0203201340': 'BE0203201340'}
    include_countries_invalid = {'DE114103379': ['DE VAT numbers are not allowed in this field.']}

    def test_include_countries_form_field(self):
        self.assertFieldOutput(VATNumberFormField, field_kwargs={'countries': self.include_countries}, valid=self.include_countries_valid, invalid=self.include_countries_invalid)

    def test_include_countries_model_field(self):
        model_field = VATNumberField(countries=self.include_countries)
        for input, output in self.include_countries_valid.items():
            self.assertEqual(model_field.clean(input, None), output)

        for input, errors in self.include_countries_invalid.items():
            with self.assertRaises(ValidationError) as (context_manager):
                model_field.clean(input, None)
            self.assertEqual(context_manager.exception.messages, errors[::-1])

    def test_vies_check_validator(self):
        validator = VATNumberValidator(vies_check=True)
        validator('DE114103379')
        try:
            with self.assertRaises(ValidationError) as (context_manager):
                validator('DE999999999')
            self.assertEqual(context_manager.exception.messages, ['This VAT number does not exist.'])
        except AssertionError:
            if validator._wsdl_exception is not None:
                print('Suds WSDL test skipped due to connection failure')
                self.skipTest('Suds WSDL client failed')
            else:
                raise

    def test_vies_check_validator_native(self):
        validator = VATNumberValidator(vies_check=True)
        validator._check_vies = validator._check_vies_native
        validator('DE114103379')
        try:
            with self.assertRaises(ValidationError) as (context_manager):
                validator('DE999999999')
            self.assertEqual(context_manager.exception.messages, ['This VAT number does not exist.'])
        except AssertionError:
            if validator._wsdl_exception is not None:
                print('Native WSDL test skipped due to connection failure')
                self.skipTest('Native WSDL client failed')
            else:
                raise