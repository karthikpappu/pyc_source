# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dpwrussell/Checkout/OME/forms/omero_forms/urls.py
# Compiled at: 2020-01-18 11:58:06
# Size of source mod 2**32: 2422 bytes
from django.conf.urls import url
from . import views
urlpatterns = [
 url('^designer/$', (views.designer), name='omeroforms_designer'),
 url('^$', (lambda x: None), name='omeroforms_base'),
 url('^list_forms/$', (views.list_forms), name='omeroforms_list_forms'),
 url('^list_applicable_forms/(?P<obj_type>\\w+)/$',
   (views.list_applicable_forms),
   name='omeroforms_list_applicable_forms'),
 url('^get_form/(?P<form_id>[\\w ]+)/$', (views.get_form), name='omeroforms_get_form'),
 url('^get_form_data/(?P<form_id>[\\w ]+)/(?P<obj_type>\\w+)/(?P<obj_id>[\\w ]+)/$',
   (views.get_form_data),
   name='omeroforms_get_form_data'),
 url('get_form_assignments/$',
   (views.get_form_assignments),
   name='omeroforms_get_form_assignments'),
 url('^get_form_data_history/(?P<form_id>[\\w ]+)/(?P<obj_type>\\w+)/(?P<obj_id>[\\w ]+)/$',
   (views.get_form_data_history),
   name='omeroforms_get_form_data_history'),
 url('^get_managed_groups/$',
   (views.get_managed_groups),
   name='omeroforms_get_managed_groups'),
 url('^get_users/$', (views.get_users), name='omeroforms_get_users'),
 url('^get_formid_editable/(?P<form_id>[\\w ]+)/$',
   (views.get_formid_editable),
   name='omeroforms_get_formid_editable'),
 url('^save_form/$', (views.save_form), name='omeroforms_save_form'),
 url('^save_form_data/(?P<form_id>[\\w ]+)/(?P<obj_type>\\w+)/(?P<obj_id>[\\w ]+)/$',
   (views.save_form_data),
   name='omeroforms_save_form_data'),
 url('^save_form_assignment/$',
   (views.save_form_assignment),
   name='omeroforms_save_form_assignment')]