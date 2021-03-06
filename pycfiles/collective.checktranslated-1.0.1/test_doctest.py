# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/checkpermission/tests/test_doctest.py
# Compiled at: 2009-11-06 11:57:19
import unittest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()
import collective.checkpermission
from collective.checkpermission.tests import base

class TestCase(ptc.PloneTestCase):
    __module__ = __name__

    class layer(PloneSite):
        __module__ = __name__

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', collective.checkpermission)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([doctestunit.DocTestSuite(module='collective.checkpermission.check', setUp=testing.setUp, tearDown=testing.tearDown), ztc.FunctionalDocFileSuite('check.txt', package='collective.checkpermission', test_class=base.FunctionalTestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')