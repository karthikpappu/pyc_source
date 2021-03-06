# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/bricklayer/testsuite/generatetestpackage.py
# Compiled at: 2013-11-21 19:28:55
from django.test import TestCase
from bricklayer.utils import *
import test_app, os, imp

class GenerateTestPackageTestCase(TestCase):

    def setUp(self):
        self.app_path = os.path.abspath(test_app.__path__[0])
        with open(os.path.join(self.app_path, 'tests.py')) as (f):
            self.tests_content = f.read()
        run_manage_py('generatetestpackage test_app')

    def test_folder_structure(self):
        """
                        Test folder structure
                """
        self.assertTrue(exists_dir(self.app_path, 'testsuite'))
        self.assertTrue(exists_path(self.app_path, 'testsuite', '__init__.py'))
        self.assertTrue(exists_path(self.app_path, 'testsuite', 'test_app_tests.py'))

    def test_testsuite_module(self):
        with open(os.path.join(self.app_path, 'testsuite', '__init__.py')) as (f):
            test_text = f.read()
        self.assertIn('from test_app.testsuite.test_app_tests import *', test_text)

    def test_imports_in_tests_py(self):
        with open(os.path.join(self.app_path, 'tests.py')) as (f):
            test_text = f.read()
        self.assertIn('from test_app.testsuite import *', test_text)

    def test_orginal_test_file_has_been_copied(self):
        with open(os.path.join(self.app_path, 'testsuite', 'test_app_tests.py')) as (f):
            test_py_text = f.read()
        self.assertEqual(test_py_text.strip(), self.tests_content.strip())

    def tearDown(self):
        self.app_path = os.path.abspath(test_app.__path__[0])
        with open(os.path.join(self.app_path, 'tests.py'), 'w') as (f):
            f.write(self.tests_content)
        for file in os.listdir(os.path.join(self.app_path, 'testsuite')):
            os.remove(os.path.join(self.app_path, 'testsuite', file))

        os.rmdir(os.path.join(self.app_path, 'testsuite'))