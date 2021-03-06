# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/tests/testDocumentation.py
# Compiled at: 2008-09-11 19:48:09
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
package = 'Products.Relations.doc'
from Products.PloneTestCase import PloneTestCase
import common
common.installWithinPortal()

class TestOverviewTxt(PloneTestCase.PloneTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.folder.invokeFactory('SimpleType', 'alfred')
        self.folder.invokeFactory('ComplexType', 'manfred')
        self.ruleset = common.createRuleset(self, 'IsParentOf')


def test_suite():
    from unittest import TestSuite
    from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
    return TestSuite((ZopeDocFileSuite('Overview.txt', package='Products.Relations.doc', test_class=TestOverviewTxt),))


if __name__ == '__main__':
    framework()