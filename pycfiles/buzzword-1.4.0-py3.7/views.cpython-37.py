# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/start/views.py
# Compiled at: 2020-05-05 16:47:29
# Size of source mod 2**32: 241 bytes
from django.shortcuts import render
import explore.models

def start(request):
    context = {'corpora': explore.models.Corpus.objects.filter(disabled=False, load=True)}
    return render(request, 'start/start.html', context)