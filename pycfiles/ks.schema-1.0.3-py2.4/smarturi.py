# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/schema/smarturi/smarturi.py
# Compiled at: 2008-12-22 08:23:25
"""HMTMLDisplayWidget class for the Zope 3 based ks.widget package

$Id: smarturi.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Anatoly Bubenkov'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
from zope.schema import Object
from interfaces import ISmartURI, IURI
from zope.interface import implements
from zope.interface.interfaces import IInterface

class URI(object):
    __module__ = __name__
    implements(IURI)
    title = IURI['title'].default
    uri = IURI['uri'].default

    def __init__(self, title=None, uri=None):
        self.title = title
        self.uri = uri


class SmartURI(Object):
    __module__ = __name__
    implements(ISmartURI)

    def __init__(self, **kw):
        schema = kw.get('schema', None)
        if not IInterface.providedBy(schema):
            schema = IURI
        super(SmartURI, self).__init__(schema, **kw)
        return