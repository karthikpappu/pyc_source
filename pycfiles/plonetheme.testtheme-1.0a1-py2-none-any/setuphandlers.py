# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/plonetheme/terrafirma/setuphandlers.py
# Compiled at: 2008-03-17 00:10:15
from zope.component import getUtility, getMultiAdapter
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

def setPortlets(portal):
    """Since there's not GenericSetup way to do this"""
    left_column = getUtility(IPortletManager, name='plone.leftcolumn')
    left_assignable = getMultiAdapter((portal, left_column), IPortletAssignmentMapping)
    right_column = getUtility(IPortletManager, name='plone.rightcolumn')
    right_assignable = getMultiAdapter((portal, right_column), IPortletAssignmentMapping)
    for name in left_assignable.keys():
        right_assignable[name] = left_assignable[name]
        del left_assignable[name]


def setupVarious(context):
    if context.readDataFile('plonetheme.terrafirma_various.txt') is None:
        return
    portal = context.getSite()
    setPortlets(portal)
    return