# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/local/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/ftpysetup/runtest/unit.py
# Compiled at: 2014-12-30 15:36:44
# Size of source mod 2**32: 1588 bytes
"""Setuptools command to execute unit tests."""
__author__ = ('Lance Finn Helsten', )
__version__ = '0.7.3'
__copyright__ = 'Copyright (C) 2014 Lance Helsten'
__docformat__ = 'reStructuredText en'
__license__ = '\n    Licensed under the Apache License, Version 2.0 (the "License");\n    you may not use this file except in compliance with the License.\n    You may obtain a copy of the License at\n\n        http://www.apache.org/licenses/LICENSE-2.0\n\n    Unless required by applicable law or agreed to in writing, software\n    distributed under the License is distributed on an "AS IS" BASIS,\n    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n    See the License for the specific language governing permissions and\n    limitations under the License.\n'
from .testbase import TestBase
__all__ = [
 'UnitTestRunner']

class UnitTestRunner(TestBase):
    description = 'Run all unit tests on the system.'
    user_options = [
     ('suite=', 's', 'Run specific test suite [default: all tests].'),
     ('debug=', 'd', 'Debug a specific test with preset breakpoints.'),
     ('coverage', 'c', 'Turn on code coverage for the tests.'),
     ('bSetup', None, 'Add a breakpoint in setUp for debug.'),
     ('bTeardown', None, 'Add a breakpoint in tearDown for debug.')]

    def initialize_options(self):
        super().initialize_options()
        self.test_type = 'unit'
        self.suite_name = 'UnitTestSuite'