# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trytond/modules/lims_project_water/tests/test_lims_project.py
# Compiled at: 2017-07-19 14:59:38
# Size of source mod 2**32: 555 bytes
import unittest, trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase

class LimsTestCase(ModuleTestCase):
    __doc__ = 'Test lims_project_water module'
    module = 'lims_project_water'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LimsTestCase))
    return suite