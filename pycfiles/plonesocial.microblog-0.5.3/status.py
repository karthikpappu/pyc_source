# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.microblog/plonesocial/microblog/browser/status.py
# Compiled at: 2014-03-11 12:09:55
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.interface import implements
from zope.component import adapts
from zope.component import queryUtility
from AccessControl import getSecurityManager
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Acquisition import aq_inner
from Acquisition import aq_chain
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from z3c.form import form, field, button
from z3c.form.interfaces import IFormLayer
from plone.z3cform import z2
from plone.z3cform.fieldsets import extensible
from plone.z3cform.interfaces import IWrappedForm
from ..interfaces import IMicroblogTool
from ..interfaces import IStatusUpdate
from ..interfaces import IMicroblogContext
from plonesocial.microblog.statusupdate import StatusUpdate
from plonesocial.microblog.utils import get_microblog_context
from .interfaces import IPlonesocialMicroblogLayer
from .interfaces import IStatusProvider
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('plonesocial.microblog')

class StatusForm(extensible.ExtensibleForm, form.Form):
    ignoreContext = True
    id = None
    label = _('Add a comment')
    fields = field.Fields(IStatusUpdate).omit('portal_type', '__parent__', '__name__', 'id', 'mime_type', 'creator', 'userid', 'creation_date')

    def updateFields(self):
        super(StatusForm, self).updateFields()

    def updateWidgets(self):
        super(StatusForm, self).updateWidgets()

    def updateActions(self):
        super(StatusForm, self).updateActions()
        self.actions['cancel'].addClass('hide')
        self.actions['statusupdate'].addClass('standalone')

    @button.buttonAndHandler(_('label_statusupdate', default='Status Update'), name='statusupdate')
    def handleComment(self, action):
        data, errors = self.extractData()
        if errors:
            return
        container = queryUtility(IMicroblogTool)
        microblog_context = get_microblog_context(self.context)
        status = StatusUpdate(data['text'], context=microblog_context)
        container.add(status)
        self.request.response.redirect(self.action)

    @button.buttonAndHandler(_('Cancel'))
    def handleCancel(self, action):
        pass


class StatusProvider(object):
    """Re-usable microblog status form provider"""
    implements(IStatusProvider)
    adapts(Interface, IPlonesocialMicroblogLayer, Interface)
    form = StatusForm
    index = ViewPageTemplateFile('status.pt')
    comment_transform_message = "What's on your mind?"

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view
        self.portlet_data = None
        for obj in aq_chain(self.context):
            if IMicroblogContext.providedBy(obj) or IPloneSiteRoot.providedBy(obj):
                self.context = obj
                return

        return

    def update(self):
        self._update()

    def _update(self):
        if self.available:
            z2.switch_on(self, request_layer=IFormLayer)
            self.form = self.form(aq_inner(self.context), self.request)
            alsoProvides(self.form, IWrappedForm)
            self.form.update()

    def render(self):
        return self.index()

    __call__ = render

    @property
    def available(self):
        permission = 'Plone Social: Add Microblog Status Update'
        have_permission = getSecurityManager().checkPermission(permission, self.context)
        is_installed = queryUtility(IMicroblogTool)
        return have_permission and is_installed

    @property
    def compact(self):
        if not self.portlet_data:
            return True
        else:
            return self.portlet_data.compact


class StatusViewlet(StatusProvider, ViewletBase):

    def __init__(self, context, request, view, manager):
        StatusProvider.__init__(self, context, request, view)
        ViewletBase.__init__(self, context, request, view, manager)

    def update(self):
        self._update()
        ViewletBase.update(self)