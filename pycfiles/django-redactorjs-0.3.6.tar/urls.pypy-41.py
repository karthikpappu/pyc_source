# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tigorc/repo/django-redactorjs/redactor/urls.py
# Compiled at: 2016-08-30 10:29:24
try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url, patterns

from redactor.views import DefaultRedactorUploadView
from redactor.forms import FileForm
urlpatterns = [
 url('^upload/image/(?P<upload_to>.*)', DefaultRedactorUploadView.as_view(), name='redactor_upload_image'),
 url('^upload/file/(?P<upload_to>.*)', DefaultRedactorUploadView.as_view(), {'form_class': FileForm}, name='redactor_upload_file')]