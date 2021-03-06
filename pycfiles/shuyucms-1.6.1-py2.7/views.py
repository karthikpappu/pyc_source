# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/utils/views.py
# Compiled at: 2016-05-20 23:26:47
from __future__ import division, unicode_literals
from datetime import datetime, timedelta
from future.builtins import int
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen

import django
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import EmailField, URLField, Textarea
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
import shuyucms
from shuyucms.conf import settings
from shuyucms.utils.sites import has_site_permission
from shuyucms.utils.importing import import_dotted_path

def is_editable(obj, request):
    """
    Returns ``True`` if the object is editable for the request. First
    check for a custom ``editable`` handler on the object, otherwise
    use the logged in user and check change permissions for the
    object's model.
    """
    if hasattr(obj, b'is_editable'):
        return obj.is_editable(request)
    else:
        perm = obj._meta.app_label + b'.' + obj._meta.get_change_permission()
        return request.user.is_authenticated() and has_site_permission(request.user) and request.user.has_perm(perm)


def ip_for_request(request):
    """
    Returns ip address for request - first checks ``HTTP_X_FORWARDED_FOR``
    header, since app will generally be behind a public web server.
    """
    meta = request.META
    return meta.get(b'HTTP_X_FORWARDED_FOR', meta[b'REMOTE_ADDR']).split(b',')[0]


def is_spam_akismet(request, form, url):
    """
    Identifies form data as being spam, using the http://akismet.com
    service. The Akismet API key should be specified in the
    ``AKISMET_API_KEY`` setting. This function is the default spam
    handler defined in the ``SPAM_FILTERS`` setting.

    The name, email, url and comment fields are all guessed from the
    form fields:

    * name: First field labelled "Name", also taking i18n into account.
    * email: First ``EmailField`` field.
    * url: First ``URLField`` field.
    * comment: First field with a ``Textarea`` widget.

    If the actual comment can't be extracted, spam checking is passed.

    The referrer field expects a hidden form field to pass the referrer
    through, since the HTTP_REFERER will be the URL the form is posted
    from. The hidden referrer field is made available by default with
    the ``{% fields_for %}`` templatetag used for rendering form fields.
    """
    if not settings.AKISMET_API_KEY:
        return False
    else:
        if not request.is_secure():
            protocol = b'http' if 1 else b'https'
            host = protocol + b'://' + request.get_host()
            data = {b'blog': host, 
               b'user_ip': ip_for_request(request), 
               b'user_agent': request.META.get(b'HTTP_USER_AGENT', b''), 
               b'referrer': request.POST.get(b'referrer', b''), 
               b'permalink': host + url, 
               b'comment_type': b'comment' if b'comment' in request.POST else b'form'}
            for name, field in form.fields.items():
                data_field = None
                if field.label and field.label.lower() in (b'name', _(b'Name').lower()):
                    data_field = b'comment_author'
                elif isinstance(field, EmailField):
                    data_field = b'comment_author_email'
                elif isinstance(field, URLField):
                    data_field = b'comment_author_url'
                elif isinstance(field.widget, Textarea):
                    data_field = b'comment_content'
                if data_field and not data.get(data_field):
                    cleaned_data = form.cleaned_data.get(name)
                    try:
                        data[data_field] = cleaned_data.encode(b'utf-8')
                    except UnicodeEncodeError:
                        data[data_field] = cleaned_data

            return data.get(b'comment_content') or False
        api_url = b'http://%s.rest.akismet.com/1.1/comment-check' % settings.AKISMET_API_KEY
        versions = (django.get_version(), shuyucms.__version__)
        headers = {b'User-Agent': b'Django/%s | shuyucms/%s' % versions}
        try:
            response = urlopen(Request(api_url, urlencode(data), headers)).read()
        except Exception:
            return False

        return response == b'true'


def is_spam(request, form, url):
    """
    Main entry point for spam handling - called from the comment view and
    page processor for ``shuyucms.forms``, to check if posted content is
    spam. Spam filters are configured via the ``SPAM_FILTERS`` setting.
    """
    for spam_filter_path in settings.SPAM_FILTERS:
        spam_filter = import_dotted_path(spam_filter_path)
        if spam_filter(request, form, url):
            return True


def paginate(objects, page_num, per_page, max_paging_links):
    """
    Return a paginated page for the given objects, giving it a custom
    ``visible_page_range`` attribute calculated from ``max_paging_links``.
    """
    if not per_page:
        return Paginator(objects, 0)
    paginator = Paginator(objects, per_page)
    try:
        page_num = int(page_num)
    except ValueError:
        page_num = 1

    try:
        objects = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        objects = paginator.page(paginator.num_pages)

    page_range = objects.paginator.page_range
    if len(page_range) > max_paging_links:
        start = min(objects.paginator.num_pages - max_paging_links, max(0, objects.number - max_paging_links // 2 - 1))
        page_range = page_range[start:start + max_paging_links]
    objects.visible_page_range = page_range
    return objects


def render(request, templates, dictionary=None, context_instance=None, **kwargs):
    """
    Mimics ``django.shortcuts.render`` but uses a TemplateResponse for
    ``shuyucms.core.middleware.TemplateForDeviceMiddleware``
    """
    dictionary = dictionary or {}
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = RequestContext(request, dictionary)
    return TemplateResponse(request, templates, context_instance, **kwargs)


def set_cookie(response, name, value, expiry_seconds=None, secure=False):
    """
    Set cookie wrapper that allows number of seconds to be given as the
    expiry time, and ensures values are correctly encoded.
    """
    if expiry_seconds is None:
        expiry_seconds = 7776000
    expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=expiry_seconds), b'%a, %d-%b-%Y %H:%M:%S GMT')
    try:
        response.set_cookie(name, value, expires=expires, secure=secure)
    except (KeyError, TypeError):
        response.set_cookie(name.encode(b'utf-8'), value, expires=expires, secure=secure)

    return