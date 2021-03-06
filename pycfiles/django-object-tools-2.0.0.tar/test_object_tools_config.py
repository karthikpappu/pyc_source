# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-object-tools/object_tools/tests/test_object_tools_config.py
# Compiled at: 2018-12-21 04:58:46
from __future__ import unicode_literals
import sys, django
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from object_tools import autodiscover
from object_tools.sites import ObjectTools
from object_tools.tests.tools import TestTool, TestInvalidTool
from object_tools.validation import validate

class InitTestCase(TestCase):
    """
    Test that tool modules are imported after autodiscover()
    """

    def test_autodiscover(self):
        autodiscover()
        self.assertTrue(b'object_tools.tests.tools' in list(sys.modules.keys()), b'Autodiscover should import tool modules from installed apps.')


class ValidateTestCase(TestCase):
    """
    Test object tool validation.
    Each object tool should have name and a label attribute.
    Each object tool should also define a view method.
    ImproperlyConfigured exception is raised for missing name and/or label.
    NotImplementedError is raised if a view is not defined.
    """

    def test_validation(self):
        self.assertRaises(ImproperlyConfigured, validate, TestInvalidTool, User)
        try:
            validate(TestInvalidTool, User)
        except ImproperlyConfigured as e:
            message = str(e)
            self.assertEqual(message, b"No 'name' attribute found for tool TestInvalidTool.")

        TestInvalidTool.name = b'test_invalid_tool'
        self.assertRaises(ImproperlyConfigured, validate, TestInvalidTool, User)
        try:
            validate(TestInvalidTool, User)
        except ImproperlyConfigured as e:
            message = str(e)
            self.assertEqual(message, b"No 'label' attribute found for tool TestInvalidTool.")

        TestInvalidTool.label = b'Test Invalid Tool'
        self.assertRaises(NotImplementedError, validate, TestInvalidTool, User)
        try:
            validate(TestInvalidTool, User)
        except NotImplementedError as e:
            message = str(e)
            self.assertEqual(message, b"No 'view' method found for tool TestInvalidTool.")


class ObjectToolsTestCase(TestCase):
    """
    Testcase for object_tools.sites.ObjectTools.
    """

    def test_init(self):
        tools = ObjectTools()
        self.assertEqual(tools.name, b'object-tools')
        self.assertEqual(tools.app_name, b'object-tools')
        self.assertEqual(tools._registry, {})

    def test_register(self):
        from django.conf import settings
        settings.DEBUG = True
        tools = ObjectTools()
        tools.register(TestTool)

    def test_urls(self):
        tools = ObjectTools()
        self.assertEqual(tools.urls, ([], b'object-tools', b'object-tools'))
        tools.register(TestTool)
        urls = tools.urls
        self.assertEqual(len(urls[0]), 6)
        if django.VERSION >= (2, 0):
            urlpatterns = [b"<URLPattern '^test_tool/$' [name='sessions_session_test_tool']>",
             b"<URLPattern '^test_tool/$' [name='auth_user_test_tool']>",
             b"<URLPattern '^test_tool/$' [name='auth_group_test_tool']>",
             b"<URLPattern '^test_tool/$' [name='auth_permission_test_tool']>",
             b"<URLPattern '^test_tool/$' [name='contenttypes_contenttype_test_tool']>",
             b"<URLPattern '^test_tool/$' [name='admin_logentry_test_tool']>"]
        else:
            urlpatterns = [b'<RegexURLPattern sessions_session_test_tool ^test_tool/$>',
             b'<RegexURLPattern auth_user_test_tool ^test_tool/$>',
             b'<RegexURLPattern auth_group_test_tool ^test_tool/$>',
             b'<RegexURLPattern auth_permission_test_tool ^test_tool/$>',
             b'<RegexURLPattern contenttypes_contenttype_test_tool ^test_tool/$>',
             b'<RegexURLPattern admin_logentry_test_tool ^test_tool/$>']
        for url in urls[0]:
            self.assertTrue(url.url_patterns[0].__repr__() in urlpatterns)