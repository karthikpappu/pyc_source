# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/italianskin/templates/browser/plone/app/controlpanel/types.py
# Compiled at: 2010-09-08 03:48:21
from plone.app.controlpanel.types import TypesControlPanel as CustomTypesControlPanel
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class TypesControlPanel(CustomTypesControlPanel):
    __module__ = __name__
    template = ViewPageTemplateFile('types.pt')