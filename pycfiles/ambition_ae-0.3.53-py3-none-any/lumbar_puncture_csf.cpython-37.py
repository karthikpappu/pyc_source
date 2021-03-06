# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/lumbar_puncture_csf.py
# Compiled at: 2018-08-21 00:59:33
# Size of source mod 2**32: 4045 bytes
from ambition_labs.panels import csf_chemistry_panel, csf_panel
from ambition_visit_schedule.constants import DAY1
from django import forms
import django.apps as django_apps
from edc_constants.constants import YES, NOT_DONE
from edc_form_validators import FormValidator
from edc_form_validators import REQUIRED_ERROR
from edc_lab import CrfRequisitionFormValidatorMixin

class LumbarPunctureCsfFormValidator(CrfRequisitionFormValidatorMixin, FormValidator):
    requisition_fields = [
     ('qc_requisition', 'qc_assay_datetime'),
     ('csf_requisition', 'csf_assay_datetime')]

    def clean(self):
        Site = django_apps.get_model('sites.site')
        self.validate_opening_closing_pressure()
        self.validate_quantitative_culture()
        self.required_if(YES,
          field='csf_culture',
          field_required='other_csf_culture')
        self.validate_requisition('csf_requisition', 'csf_assay_datetime', csf_chemistry_panel)
        self.not_required_if(None,
          field='differential_lymphocyte_count', field_required='differential_lymphocyte_unit')
        self.validate_percentage(field='differential_lymphocyte_count',
          unit='differential_lymphocyte_unit')
        self.not_required_if(None,
          field='differential_neutrophil_count', field_required='differential_neutrophil_unit')
        self.validate_percentage(field='differential_neutrophil_count',
          unit='differential_neutrophil_unit')
        self.require_together(field='csf_glucose',
          field_required='csf_glucose_units')
        self.not_required_if(NOT_DONE,
          field='csf_cr_ag', field_required='csf_cr_ag_lfa')
        if self.cleaned_data.get('subject_visit').visit_code == DAY1:
            if self.cleaned_data.get('subject_visit').visit_code_sequence == 0:
                if self.cleaned_data.get('csf_cr_ag') == NOT_DONE:
                    if self.cleaned_data.get('india_ink') == NOT_DONE:
                        error_msg = 'CSF CrAg and India Ink cannot both be "not done".'
                        message = {'csf_cr_ag':error_msg,  'india_ink':error_msg}
                        raise forms.ValidationError(message, code=REQUIRED_ERROR)
        condition = Site.objects.get_current().name == 'gaborone' or 
        self.applicable_if_true(condition=condition,
          field_applicable='bios_crag')
        self.applicable_if(YES,
          field='bios_crag',
          field_applicable='crag_control_result')
        self.applicable_if(YES,
          field='bios_crag',
          field_applicable='crag_t1_result')
        self.applicable_if(YES,
          field='bios_crag',
          field_applicable='crag_t2_result')

    def validate_quantitative_culture(self):
        self.required_if_true((self.cleaned_data.get('quantitative_culture') is not None),
          field_required='qc_requisition')
        self.validate_requisition('qc_requisition', 'qc_assay_datetime', csf_panel)

    def validate_percentage(self, field=None, unit=None):
        if self.cleaned_data.get(field):
            if self.cleaned_data.get(unit) == '%':
                if self.cleaned_data.get(field) > 100:
                    raise forms.ValidationError({field: 'Cannot be greater than 100%.'})

    def validate_opening_closing_pressure(self):
        opening_pressure = self.cleaned_data.get('opening_pressure')
        closing_pressure = self.cleaned_data.get('closing_pressure')
        try:
            if opening_pressure <= closing_pressure:
                raise forms.ValidationError({'closing_pressure': 'Cannot be greater than the opening pressure.'})
        except TypeError:
            pass