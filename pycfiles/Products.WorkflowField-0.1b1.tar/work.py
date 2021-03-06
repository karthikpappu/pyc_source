# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Work/content/work.py
# Compiled at: 2011-06-07 12:12:56
from zope.interface import implements
from Products.CMFCore import permissions
try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    from Products.Archetypes import atapi

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.Work import config
from Products.Work.interfaces import IWork
from Products.Work import WorkMessageFactory as _
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.document import finalizeATCTSchema
WorkSchema = ATDocument.schema.copy() + atapi.Schema(())
finalizeATCTSchema(WorkSchema)

class Work(atapi.OrderedBaseFolder, ATDocument):
    """An Archetype for an Work application"""
    implements(IWork)
    portal_type = meta_type = 'Work'
    schema = WorkSchema
    _at_rename_after_creation = True

    def canSetDefaultPage(self):
        return False


atapi.registerType(Work, config.PROJECTNAME)