# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/tests/test_week2_form.py
# Compiled at: 2018-07-21 08:49:31
# Size of source mod 2**32: 7739 bytes
from ambition_visit_schedule import DAY1
from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, OTHER
from ..form_validators import Week2FormValidator, SignificantDiagnosesFormValidator
from ..form_validators import FluconazoleMissedDosesFormValidator
from .models import SubjectVisit, TestModel

class TestWeek2Form(TestCase):

    def test_discharged_yes_require_discharged_date(self):
        cleaned_data = {'discharged':YES, 
         'discharge_date':None}
        week2 = Week2FormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, week2.validate)
        cleaned_data = {'discharged':YES, 
         'discharge_date':get_utcnow(), 
         'research_discharge_date':get_utcnow()}
        week2 = Week2FormValidator(cleaned_data=cleaned_data)
        try:
            week2.validate()
        except forms.ValidationError as e:
            try:
                self.fail(f"ValidationError unexpectedly raised. Got{e}")
            finally:
                e = None
                del e

    def test_discharged_yes_require_research_discharge_date(self):
        cleaned_data = {'discharged':YES, 
         'research_discharge_date':None}
        week2 = Week2FormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, week2.validate)
        cleaned_data = {'discharged':YES, 
         'discharge_date':get_utcnow(), 
         'research_discharge_date':get_utcnow()}
        week2 = Week2FormValidator(cleaned_data=cleaned_data)
        try:
            week2.validate()
        except forms.ValidationError as e:
            try:
                self.fail(f"ValidationError unexpectedly raised. Got{e}")
            finally:
                e = None
                del e

    def test_died_yes_require_date_of_death(self):
        cleaned_data = {'died':YES, 
         'death_date_time':None}
        week2 = Week2FormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, week2.validate)
        cleaned_data = {'died':YES, 
         'death_date_time':get_utcnow()}
        week2 = Week2FormValidator(cleaned_data=cleaned_data)
        try:
            week2.validate()
        except forms.ValidationError as e:
            try:
                self.fail(f"ValidationError unexpectedly raised. Got{e}")
            finally:
                e = None
                del e

    def test_blood_recieved_yes_requires_units(self):
        cleaned_data = {'blood_received':YES, 
         'units':None}
        week2 = Week2FormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, week2.validate)
        cleaned_data = {'blood_received':YES, 
         'units':2}
        week2 = Week2FormValidator(cleaned_data=cleaned_data)
        try:
            week2.validate()
        except forms.ValidationError as e:
            try:
                self.fail(f"ValidationError unexpectedly raised. Got{e}")
            finally:
                e = None
                del e


class TestSignificantDiagnosesForm(TestCase):

    def setUp(self):
        appointment = Appointment.objects.create(subject_identifier='11111111',
          appt_datetime=(get_utcnow()),
          visit_code=DAY1)
        self.subject_visit = SubjectVisit.objects.create(appointment=appointment)
        self.week2 = TestModel.objects.create(subject_visit=(self.subject_visit),
          other_significant_dx=YES)

    def test_significant_diagnoses_no_specification_invalid(self):
        cleaned_data = {'week2':self.week2, 
         'other_significant_diagnoses':YES, 
         'possible_diagnoses':None}
        form = SignificantDiagnosesFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)

    def test_significant_diagnoses_specification_valid(self):
        cleaned_data = {'week2':self.week2, 
         'other_significant_diagnoses':YES, 
         'possible_diagnoses':'pneumonia'}
        form = SignificantDiagnosesFormValidator(cleaned_data=cleaned_data)
        try:
            form.validate()
        except forms.ValidationError as e:
            try:
                self.fail(f"ValidationError unexpectedly raised. Got{e}")
            finally:
                e = None
                del e

    def test_significant_diagnoses_no_date_invalid(self):
        cleaned_data = {'week2':self.week2, 
         'other_significant_diagnoses':YES, 
         'possible_diagnoses':'pneumonia', 
         'dx_date':None}
        form = SignificantDiagnosesFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)

    def test_significant_diagnoses_date_valid(self):
        cleaned_data = {'week2':self.week2, 
         'other_significant_diagnoses':YES, 
         'possible_diagnoses':'pneumonia', 
         'dx_date':get_utcnow()}
        form = SignificantDiagnosesFormValidator(cleaned_data=cleaned_data)
        try:
            form.validate()
        except forms.ValidationError as e:
            try:
                self.fail(f"ValidationError unexpectedly raised. Got{e}")
            finally:
                e = None
                del e

    def test_significant_diagnoses_other_not_specified_invalid(self):
        cleaned_data = {'week2':self.week2, 
         'other_significant_diagnoses':YES, 
         'possible_diagnoses':OTHER, 
         'dx_other':None}
        form = SignificantDiagnosesFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)

    def test_significant_diagnoses_other_specified_valid(self):
        cleaned_data = {'week2':self.week2, 
         'other_significant_diagnoses':YES, 
         'possible_diagnoses':OTHER, 
         'dx_other':'blah'}
        form = SignificantDiagnosesFormValidator(cleaned_data=cleaned_data)
        try:
            form.validate()
        except forms.ValidationError as e:
            try:
                self.fail(f"ValidationError unexpectedly raised. Got{e}")
            finally:
                e = None
                del e

    def test_flucon_day_missed_no_reason_invalid(self):
        cleaned_data = {'week2':self.week2, 
         'flucon_day_missed':1, 
         'flucon_missed_reason':None}
        form = FluconazoleMissedDosesFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)

    def test_flucon_day_missed_reason_ivalid(self):
        cleaned_data = {'week2':self.week2, 
         'flucon_day_missed':1, 
         'flucon_missed_reason':'blah'}
        form = FluconazoleMissedDosesFormValidator(cleaned_data=cleaned_data)
        try:
            form.validate()
        except forms.ValidationError as e:
            try:
                self.fail(f"ValidationError unexpectedly raised. Got{e}")
            finally:
                e = None
                del e

    def test_flucon_day_missed_no_reason_other_not_provided_invalid(self):
        cleaned_data = {'week2':self.week2, 
         'flucon_day_missed':1, 
         'flucon_missed_reason':OTHER, 
         'missed_reason_other':None}
        form = FluconazoleMissedDosesFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)

    def test_flucon_day_missed_reason_other_not_provided_ivalid(self):
        cleaned_data = {'week2':self.week2, 
         'flucon_day_missed':1, 
         'flucon_missed_reason':OTHER, 
         'missed_reason_other':'blah'}
        form = FluconazoleMissedDosesFormValidator(cleaned_data=cleaned_data)
        try:
            form.validate()
        except forms.ValidationError as e:
            try:
                self.fail(f"ValidationError unexpectedly raised. Got{e}")
            finally:
                e = None
                del e