# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/xadmin/views/website.py
# Compiled at: 2020-02-22 05:09:52
# Size of source mod 2**32: 6531 bytes
from __future__ import absolute_import
from functools import wraps
import httplib2, urllib
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import LoginView as login
from django.contrib.auth.views import LogoutView as logout
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.utils import six
from django.conf import settings
from .base import BaseAdminView, filter_hook
from .dashboard import Dashboard
from xadmin.forms import AdminAuthenticationForm
from xadmin.models import UserSettings
from xadmin.layout import FormHelper
from xadmin.util import json

def check_recaptcha(view_func):

    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        request = args[(-1)] if len(args) > 0 else None
        if request is None or not isinstance(request, HttpRequest):
            return HttpResponseBadRequest()
        else:
            request.recaptcha_is_valid = None
            if request.method == 'POST' and getattr(settings, 'GOOGLE_RECAPTCHA_SECRET_KEY', ''):
                recaptcha_response = request.POST.get('g-recaptcha-response')
                request.recaptcha_is_valid = False
                if recaptcha_response:
                    data = {'secret':settings.GOOGLE_RECAPTCHA_SECRET_KEY,  'response':recaptcha_response}
                    content = {}
                    try:
                        import requests
                    except:
                        h = httplib2.Http()
                        try:
                            resp, content = h.request('https://www.google.com/recaptcha/api/siteverify', method='POST',
                              body=(urllib.urlencode(data)),
                              headers={'Content-type':'application/x-www-form-urlencoded', 
                             'User-agent':request.META.get('HTTP_USER_AGENT', '')})
                            if six.PY3:
                                content = content.decode()
                            content = json.loads(content)
                        except:
                            pass

                    else:
                        try:
                            resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data,
                              headers={'user-agent': request.META.get('HTTP_USER_AGENT', '')})
                            resp.raise_for_status()
                            content = resp.json()
                        except:
                            pass

                        if content.get('success'):
                            request.recaptcha_is_valid = True
            return view_func(*args, **kwargs)

    return _wrapped_view


class IndexView(Dashboard):
    title = _('Main Dashboard')
    icon = 'fa fa-dashboard'

    def get_page_id(self):
        return 'home'


class UserSettingView(BaseAdminView):

    @never_cache
    def post(self, request):
        key = request.POST['key']
        val = request.POST['value']
        us, created = UserSettings.objects.get_or_create(user=(self.user),
          key=key)
        us.value = val
        us.save()
        return HttpResponse('')


class LoginView(BaseAdminView):
    title = _('Please Login')
    login_form = None
    login_template = None

    @filter_hook
    def update_params(self, defaults):
        pass

    @never_cache
    def get(self, request, *args, **kwargs):
        context = self.get_context()
        helper = FormHelper()
        helper.form_tag = False
        helper.include_media = False
        if request.get_full_path() == self.get_admin_url('login'):
            next_url = self.get_admin_url('index')
        else:
            next_url = request.get_full_path()
        context.update({'title': self.title, 
         'helper': helper, 
         'app_path': request.get_full_path(), 
         'site_title': self.site_title, 
         'site_footer': self.site_footer, 
         REDIRECT_FIELD_NAME: next_url})
        defaults = {'extra_context':context, 
         'authentication_form':self.login_form or AdminAuthenticationForm, 
         'template_name':self.login_template or 'xadmin/views/login.html'}
        self.update_params(defaults)
        if getattr(settings, 'GOOGLE_RECAPTCHA_SITE_ID', ''):
            context['GOOGLE_RECAPTCHA_SITE_ID'] = settings.GOOGLE_RECAPTCHA_SITE_ID
            if request.method == 'POST':
                if getattr(settings, 'GOOGLE_RECAPTCHA_SECRET_KEY', ''):
                    if not request.recaptcha_is_valid:
                        context.update({'recaptcha_message': _('Please check the above verify box!')})
                        return render(request, defaults['template_name'], context)
        return (login.as_view)(**defaults)(request)

    @never_cache
    @check_recaptcha
    def post(self, request, *args, **kwargs):
        return self.get(request)


class LogoutView(BaseAdminView):
    logout_template = None
    need_site_permission = False

    @filter_hook
    def update_params(self, defaults):
        pass

    @never_cache
    def get(self, request, *args, **kwargs):
        context = self.get_context()
        defaults = {'extra_context':context, 
         'template_name':self.logout_template or 'xadmin/views/logged_out.html'}
        if self.logout_template is not None:
            defaults['template_name'] = self.logout_template
        self.update_params(defaults)
        return (logout.as_view)(**defaults)(request)

    @never_cache
    def post(self, request, *args, **kwargs):
        return self.get(request)