# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/content/epidemiologicalyear.py
# Compiled at: 2014-12-12 07:13:54
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import BaseContent
from Products.Archetypes.public import DateTimeField
from Products.Archetypes.public import registerType
from Products.Archetypes.public import Schema
from bika.lims.browser.widgets import DateTimeWidget
from bika.lims.content.bikaschema import BikaSchema
from bika.health.config import PROJECTNAME
from bika.lims import bikaMessageFactory as _b
from bika.health import bikaMessageFactory as _
schema = BikaSchema.copy() + Schema((
 DateTimeField('StartDate', schemata='default', required=True, widget=DateTimeWidget(label=_('Epidemiological year start date'))),
 DateTimeField('EndDate', schemata='default', required=True, widget=DateTimeWidget(label=_('Epidemiological year end date')))))
schema['description'].widget.visible = False
schema['description'].schemata = 'default'

class EpidemiologicalYear(BaseContent):
    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema
    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from bika.lims.idserver import renameAfterCreation
        renameAfterCreation(self)


registerType(EpidemiologicalYear, PROJECTNAME)