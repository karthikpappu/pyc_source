# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/browser/comment_form.py
# Compiled at: 2007-10-06 06:19:54
from AccessControl import Unauthorized
from datetime import datetime
from datetime import timedelta
from zope.component import getMultiAdapter
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('iqpp.plone.commenting')
from Products.Five.browser import BrowserView
from Products.Five.browser import pagetemplatefile
from Products.CMFCore.utils import getToolByName
from iqpp.plone.commenting.config import MESSAGES
from iqpp.plone.commenting.interfaces import ICommenting
from iqpp.plone.commenting.interfaces import ICommentingOptions

class CommentFormView(BrowserView):
    """Base form view.
    """
    __module__ = __name__
    template = pagetemplatefile.ZopeTwoPageTemplateFile('comment_form.pt')

    def __init__(self, context, request):
        """
        """
        super(CommentFormView, self).__init__(context, request)
        self._errors = {}
        self.options = ICommentingOptions(self.context)
        self.utils = getToolByName(self.context, 'plone_utils')

    def addMessage(self):
        """
        """
        ptool = getToolByName(self.context, 'plone_utils')
        options = ICommentingOptions(self.context)
        if options.getEffectiveOption('is_moderated') == True:
            ptool.addPortalMessage(_(MESSAGES['comment-added-moderated']))
        else:
            ptool.addPortalMessage(_(MESSAGES['comment-added']))

    def getErrors(self):
        """Returns validation errors.
        """
        return self._errors

    def isMember(self):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        return not mtool.isAnonymousUser()

    def redirect(self):
        """
        """
        url = self.context.absolute_url()
        self.request.response.redirect(url)

    def showAddButton(self):
        """Returns True if user adds a comment.
        """
        if self.request.get('action') == 'add':
            return True
        else:
            return False

    def showEditButton(self):
        """Returns True if user edits a comment.
        """
        return not self.showAddButton()

    def validate(self):
        """
        """
        name = self.request.get('name', '')
        email = self.request.get('email', '')
        subject = self.request.get('subject', '')
        message = self.request.get('message', '')
        if subject == '':
            self._errors['subject'] = _('Subject is required.')
        if message == '':
            self._errors['message'] = _('Message is required.')
        if self.isMember() == False:
            if name == '':
                self._errors['name'] = _('Name is required.')
            if email == '':
                self._errors['email'] = _('E-mail is required.')


class AddCommentFormView(CommentFormView):
    """A form to add new comments
    """
    __module__ = __name__

    def addComment(self):
        """Adds a comment.
        """
        mtool = getToolByName(self.context, 'portal_membership')
        comment_id = self.request.get('comment_id', '')
        if comment_id == '':
            if mtool.checkPermission('Reply to item', self.context) is None:
                raise Unauthorized
        elif mtool.checkPermission('Reply to comment', self.context) is None:
            raise Unauthorized
        self.validate()
        if len(self._errors) > 0:
            ptool = getToolByName(self.context, 'plone_utils')
            ptool.addPortalMessage(_('Please correct the indicated errors.'))
            return self.template()
        options = ICommentingOptions(self.context)
        if options.getEffectiveOption('show_preview') and self.request.get('is_previewed', False) == False:
            preview = getMultiAdapter((self.context, self.request), name='preview_comment')
            return preview()
        subject = self.request.get('subject', '')
        message = self.request.get('message', '')
        if self.isMember() == False:
            name = self.request.get('name', '')
            email = self.request.get('email', '')
            member_id = None
        else:
            member = mtool.getAuthenticatedMember()
            name = ''
            email = ''
            member_id = member.getId()
        commenting = ICommenting(self.context)
        result = commenting.addComment(reply_to=comment_id, subject=subject, message=message, name=name, email=email, member_id=member_id)
        self.addMessage()
        self.redirect()
        return

    def getFieldValues(self):
        """Returns all field values as a dict.
        """
        return {'id': self.request.get('comment_id'), 'name': self.request.get('name'), 'email': self.request.get('email'), 'subject': self.request.get('subject'), 'message': self.request.get('message')}


class EditCommentFormView(CommentFormView):
    """A form to let owner edit their existing comments.
    """
    __module__ = __name__

    def editComment(self):
        """Edits a comment.
        """
        mtool = getToolByName(self.context, 'portal_membership')
        comment_id = self.request.get('comment_id', None)
        commenting = ICommenting(self.context)
        comment = commenting.getComment(comment_id)
        self.validate()
        if len(self._errors) > 0:
            ptool = getToolByName(self.context, 'plone_utils')
            ptool.addPortalMessage(_('Please correct the indicated errors.'))
            return self.template()
        options = ICommentingOptions(self.context)
        if options.getEffectiveOption('show_preview') and self.request.get('is_previewed', False) == False:
            preview = getMultiAdapter((self.context, self.request), name='preview_comment')
            return preview()
        subject = self.request.get('subject', '')
        message = self.request.get('message', '')
        if self.isMember() == False:
            name = self.request.get('name', '')
            email = self.request.get('email', '')
            member_id = None
        else:
            member = mtool.getAuthenticatedMember()
            name = ''
            email = ''
            member_id = member.getId()
        result = commenting.editComment(comment_id=comment_id, subject=subject, message=message)
        self.addMessage()
        self.redirect()
        return

    def getFieldValues(self):
        """Returns all field values as a dict.
        """
        comment_id = self.request.get('comment_id')
        commenting = ICommenting(self.context)
        comment = commenting.getComment(comment_id)
        name = self.request.get('name') or comment.name
        email = self.request.get('email') or comment.email
        subject = self.request.get('subject') or comment.subject
        message = self.request.get('message') or comment.message
        return {'id': comment_id, 'name': name, 'email': email, 'subject': subject, 'message': message}