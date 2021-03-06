# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\tests\common.py
# Compiled at: 2008-11-19 15:29:07
__doc__ = 'Common imports and declarations\n\ncommon includes a set of basic things that every test needs.\n\n$$\n'
__author__ = ''
__docformat__ = 'restructuredtext'
try:
    dummy = True
except NameError:
    True = 1
    False = 0

import time

def Xprint(s):
    """print helper

    print data via print is not possible, you have to use
    ZopeTestCase._print or this function
    """
    ZopeTestCase._print(str(s) + '\n')


def dcEdit(obj):
    """dublin core edit (inplace)
    """
    obj.setTitle('Test Title')
    obj.setDescription('Test description')


from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Testing import ZopeTestCase
ZopeTestCase.installProduct('CMFCore', 1)
ZopeTestCase.installProduct('CMFDefault', 1)
ZopeTestCase.installProduct('CMFCalendar', 1)
ZopeTestCase.installProduct('CMFTopic', 1)
ZopeTestCase.installProduct('DCWorkflow', 1)
ZopeTestCase.installProduct('CMFActionIcons', 1)
ZopeTestCase.installProduct('CMFQuickInstallerTool', 1)
ZopeTestCase.installProduct('CMFFormController', 1)
ZopeTestCase.installProduct('GroupUserFolder', 1)
ZopeTestCase.installProduct('ZCTextIndex', 1)
ZopeTestCase.installProduct('CMFPlone', 1)
ZopeTestCase.installProduct('MailHost', 1)
ZopeTestCase.installProduct('PageTemplates', 1)
ZopeTestCase.installProduct('PythonScripts', 1)
ZopeTestCase.installProduct('ExternalMethod', 1)
ZopeTestCase.installProduct('ZCatalog', 1)
ZopeTestCase.installProduct('Archetypes', 1)
ZopeTestCase.installProduct('PortalTransforms', 1)
ZopeTestCase.installProduct('PloneBooking', 1)
from Products.Archetypes.public import *
from Products.Archetypes.config import PKG_NAME
from Products.Archetypes.tests import ArchetypesTestCase
from Products.Archetypes.tests.test_baseschema import BaseSchemaTest
from Products.Archetypes.interfaces.layer import ILayerContainer
from Products.Archetypes.Storage import AttributeStorage, MetadataStorage
from Products.Archetypes import listTypes
from Products.Archetypes.Widget import IdWidget, StringWidget, BooleanWidget, KeywordWidget, TextAreaWidget, CalendarWidget, SelectionWidget
from Products.Archetypes.utils import DisplayList
from Products.CMFCore import CMFCorePermissions
from Products.Archetypes.ExtensibleMetadata import FLOOR_DATE, CEILING_DATE
from Globals import package_home
from Products.PloneBooking.config import GLOBALS
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
try:
    import Interface
except ImportError:

    def verifyClass(iface, candidate, tentative=0):
        return True


    def verifyObject(iface, candidate, tentative=0):
        return True


    def getImplementsOfInstances(object):
        return ()


    def getImplements(object):
        return ()


    def flattenInterfaces(interfaces, remove_duplicates=1):
        return ()


    class BrokenImplementation(Exception):
        __module__ = __name__


    class DoesNotImplement(Exception):
        __module__ = __name__


    class BrokenMethodImplementation(Exception):
        __module__ = __name__


else:
    from Interface.Implements import getImplementsOfInstances, getImplements, flattenInterfaces
    from Interface.Verify import verifyClass, verifyObject
    from Interface.Exceptions import BrokenImplementation, DoesNotImplement
    from Interface.Exceptions import BrokenMethodImplementation

from PloneBookingTestCase import PloneBookingTestCase
from Products.PloneBooking.interfaces.interfaces import IBooking
from Products.PloneBooking import BookingPermissions