# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/atulvarma/Documents/18f/django-uswds-forms/example/app/examples/date.py
# Compiled at: 2017-05-12 17:41:34
# Size of source mod 2**32: 425 bytes
"""
Date

This example shows how to render a date input using a
uswds_forms.UswdsDateField.
"""
from django.shortcuts import render
import uswds_forms

class MyForm(uswds_forms.UswdsForm):
    date = uswds_forms.UswdsDateField(label='What is your favorite date?')


def view(request):
    return render(request, 'examples/radios.html', {'form': MyForm() if request.method == 'GET' else MyForm(request.POST)})