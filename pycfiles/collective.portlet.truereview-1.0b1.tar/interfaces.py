# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/portlet/toc/interfaces.py
# Compiled at: 2010-03-01 12:20:27
from zope.viewlet.interfaces import IViewletManager

class IFullViewManager(IViewletManager):
    """Viewlet manager on top of the full view on the expanded view
       used to show the table of contents
    """
    __module__ = __name__