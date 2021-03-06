# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/question.py
# Compiled at: 2020-04-28 08:13:47
from AccessControl import getSecurityManager
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from Acquisition.interfaces import IAcquirer
from esdrt.content import MessageFactory as _
from esdrt.content.comment import IComment
from five import grok
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from plone.dexterity.interfaces import IDexterityFTI
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from Products.statusmessages.interfaces import IStatusMessage
from time import time
from z3c.form import button
from z3c.form import field
from z3c.form.form import Form
from z3c.form.interfaces import ActionExecutionError
from zope import schema
from zope.component import createObject
from zope.component import getUtility
from zope.interface import Invalid
from zope.lifecycleevent import IObjectAddedEvent
from zope.lifecycleevent import IObjectModifiedEvent

class IQuestion(form.Schema, IImageScaleTraversable):
    """
    New Question regarding an Observation
    """
    form.write_permission(request_redraft_comments='cmf.ManagePortal')
    request_redraft_comments = schema.Text(title='Request redraft reasons', required=False)
    form.write_permission(request_redraft_comments_phase2='cmf.ManagePortal')
    request_redraft_comments_phase2 = schema.Text(title='Request redraft reasons for phase 2', required=False)


PENDING_STATUS_NAMES = [
 'answered']
OPEN_STATUS_NAMES = [
 'phase1-pending',
 'phase1-pending-answer',
 'phase1-pending-answer-validation',
 'phase1-validate-answer',
 'phase1-recalled-msa']
DRAFT_STATUS_NAMES = [
 'phase1-draft',
 'phase1-counterpart-comments',
 'phase1-drafted',
 'phase1-recalled-lr']
CLOSED_STATUS_NAMES = [
 'closed']
PENDING_STATUS_NAME = 'pending'
DRAFT_STATUS_NAME = 'draft'
OPEN_STATUS_NAME = 'open'
CLOSED_STATUS_NAME = 'closed'

def create_question(context):
    fti = getUtility(IDexterityFTI, name='Question')
    container = aq_inner(context)
    content = createObject(fti.factory)
    if hasattr(content, '_setPortalTypeName'):
        content._setPortalTypeName(fti.getId())
    if IAcquirer.providedBy(content):
        content = content.__of__(container)
    ids = [ id for id in context.keys() if id.startswith('question-') ]
    id = len(ids) + 1
    content.title = 'Question %d' % id
    return aq_base(content)


class Question(dexterity.Container):
    grok.implements(IQuestion)

    def get_state_api(self):
        return api.content.get_state(self)

    def get_questions(self):
        sm = getSecurityManager()
        values = [ v for v in self.values() if sm.checkPermission('View', v) ]
        return IContentListing(values)

    def getFirstComment(self):
        comments = [ v for v in self.values() if v.portal_type == 'Comment' ]
        comments.sort(lambda x, y: cmp(x.created(), y.created()))
        if comments:
            return comments[(-1)]
        else:
            return

    def get_state(self):
        state = api.content.get_state(self)
        workflows = api.portal.get_tool('portal_workflow').getWorkflowsFor(self)
        if workflows:
            for w in workflows:
                if state in w.states:
                    return w.states[state].title or state

    def get_status(self):
        state = api.content.get_state(self)
        if state in PENDING_STATUS_NAMES:
            return PENDING_STATUS_NAME
        if state in OPEN_STATUS_NAMES:
            return OPEN_STATUS_NAME
        if state in CLOSED_STATUS_NAMES:
            return CLOSED_STATUS_NAME
        if state in DRAFT_STATUS_NAMES:
            return DRAFT_STATUS_NAME
        return 'unknown'

    def get_observation(self):
        return aq_parent(aq_inner(self))

    def has_answers(self):
        items = self.values()
        questions = [ q for q in items if q.portal_type == 'Comment' ]
        answers = [ q for q in items if q.portal_type == 'CommentAnswer' ]
        return len(questions) == len(answers)

    def can_be_sent_to_lr(self):
        items = self.values()
        questions = [ q for q in items if q.portal_type == 'Comment' ]
        answers = [ q for q in items if q.portal_type == 'CommentAnswer' ]
        if len(questions) > len(answers):
            current_status = api.content.get_state(self)
            return current_status in ('phase1-draft', 'phase2-draft')
        return False

    def can_be_deleted(self):
        items = self.values()
        questions = [ q for q in items if q.portal_type == 'Comment' ]
        answers = [ q for q in items if q.portal_type == 'CommentAnswer' ]
        if len(questions) > len(answers):
            question_history = self.workflow_history['esd-question-review-workflow']
            current_status = api.content.get_state(self)
            previous_action = question_history[(-1)]
            if current_status == 'phase1-draft':
                return previous_action['action'] in ('phase1-add-folowup-question',
                                                     'phase1-reopen', None)
            if current_status == 'phase2-draft':
                return previous_action['action'] in ('phase2-add-folowup-question',
                                                     'phase2-reopen', 'go-to-phase2',
                                                     None)
        return False

    def unanswered_questions(self):
        items = self.values()
        questions = [ q for q in items if q.portal_type == 'Comment' ]
        answers = [ q for q in items if q.portal_type == 'CommentAnswer' ]
        return len(questions) > len(answers)

    def can_close(self):
        """
        Check if this question can be closed:
            - There has been at least, one question-answer.
        """
        items = self.values()
        questions = [ q for q in items if q.portal_type == 'Comment' ]
        answers = [ q for q in items if q.portal_type == 'CommentAnswer' ]
        return len(questions) > 0 and len(questions) == len(answers)

    def observation_not_closed(self):
        observation = self.get_observation()
        return api.content.get_state(observation) in ('phase1-pending', 'phase2-pending')

    def already_commented_by_counterpart(self):
        return True

    def one_pending_answer(self):
        if self.has_answers():
            answers = [ q for q in self.values() if q.portal_type == 'CommentAnswer' ]
            answer = answers[(-1)]
            user = api.user.get_current()
            return answer.Creator() == user.getId()
        else:
            return False

    def can_see_comment_discussion(self):
        sm = getSecurityManager()
        return sm.checkPermission('esdrt.content: View Comment Discussion', self)

    def can_see_answer_discussion(self):
        sm = getSecurityManager()
        return sm.checkPermission('esdrt.content: View Answer Discussion', self)


grok.templatedir('templates')

class QuestionView(grok.View):
    grok.context(IQuestion)
    grok.require('zope2.View')
    grok.name('view')

    def render(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return self.request.response.redirect(parent.absolute_url())


class AddForm(dexterity.AddForm):
    grok.name('esdrt.content.question')
    grok.context(IQuestion)
    grok.require('esdrt.content.AddQuestion')

    def updateFields(self):
        super(AddForm, self).updateFields()
        self.fields = field.Fields(IComment).select('text')
        self.groups = [ g for g in self.groups if g.label == 'label_schema_default' ]

    def updateWidgets(self):
        super(AddForm, self).updateWidgets()
        self.widgets['text'].rows = 15

    def create(self, data={}):
        fti = getUtility(IDexterityFTI, name=self.portal_type)
        container = aq_inner(self.context)
        content = createObject(fti.factory)
        if hasattr(content, '_setPortalTypeName'):
            content._setPortalTypeName(fti.getId())
        if IAcquirer.providedBy(content):
            content = content.__of__(container)
        context = self.context
        ids = [ id for id in context.keys() if id.startswith('question-') ]
        id = len(ids) + 1
        content.title = 'Question %d' % id
        return aq_base(content)

    def add(self, object):
        super(AddForm, self).add(object)
        item = self.context.get(object.getId())
        text = self.request.form.get('form.widgets.text', '')
        id = str(int(time()))
        item_id = item.invokeFactory(type_name='Comment', id=id)
        comment = item.get(item_id)
        comment.text = text


@grok.subscribe(IQuestion, IObjectAddedEvent)
def add_question(context, event):
    """ When adding a question, go directly to
        'open' status on the observation
    """
    observation = aq_parent(context)
    review_folder = aq_parent(observation)
    with api.env.adopt_roles(roles=['Manager']):
        if api.content.get_state(obj=review_folder) == 'ongoing-review-phase2':
            api.content.transition(obj=context, transition='go-to-phase2')
    observation.reindexObject()


@grok.subscribe(IQuestion, IObjectModifiedEvent)
def add_question(context, event):
    """ When adding a question, go directly to
        'open' status on the observation
    """
    observation = aq_parent(context)
    observation.reindexObject()


class AddCommentForm(Form):
    ignoreContext = True
    fields = field.Fields(IComment).select('text')
    label = 'Question'
    description = ''

    @button.buttonAndHandler(_('Add question'))
    def create_question(self, action):
        context = aq_inner(self.context)
        text = self.request.form.get('form.widgets.text', '')
        if not text.strip():
            raise ActionExecutionError(Invalid('Question text is empty'))
        id = str(int(time()))
        item_id = context.invokeFactory(type_name='Comment', id=id)
        comment = context.get(item_id)
        comment.text = text
        return self.request.response.redirect(context.absolute_url())

    def updateWidgets(self):
        super(AddCommentForm, self).updateWidgets()
        self.widgets['text'].rows = 15

    def updateActions(self):
        super(AddCommentForm, self).updateActions()
        for k in self.actions.keys():
            self.actions[k].addClass('standardButton')


class AddAnswerForm(Form):
    ignoreContext = True
    fields = field.Fields(IComment).select('text')
    label = 'Answer'
    description = ''

    @button.buttonAndHandler(_('Add answer'))
    def create_question(self, action):
        context = aq_inner(self.context)
        text = self.request.form.get('form.widgets.text', '')
        if not text.strip():
            raise ActionExecutionError(Invalid('Answer text is empty'))
        id = str(int(time()))
        item_id = context.invokeFactory(type_name='CommentAnswer', id=id)
        comment = context.get(item_id)
        comment.text = text
        return self.request.response.redirect(context.absolute_url())

    def updateWidgets(self):
        super(AddAnswerForm, self).updateWidgets()
        self.widgets['text'].rows = 15

    def updateActions(self):
        super(AddAnswerForm, self).updateActions()
        for k in self.actions.keys():
            self.actions[k].addClass('standardButton')


class EditAndCloseComments(grok.View):
    grok.name('edit-and-close-comments')
    grok.context(IQuestion)
    grok.require('zope2.View')

    def update(self):
        waction = self.request.get('workflow_action')
        comment = self.request.get('comment')
        if waction not in ('phase1-send-comments', 'phase2-send-comments') and comment not in self.context.keys():
            status = IStatusMessage(self.request)
            msg = _('There was an error, try again please')
            status.addStatusMessage(msg, 'error')
        else:
            self.comment = comment

    def render(self):
        if api.content.get_state(self.context).startswith('phase1-'):
            api.content.transition(obj=self.context, transition='phase1-send-comments')
        elif api.content.get_state(self.context).startswith('phase2-'):
            api.content.transition(obj=self.context, transition='phase2-send-comments')
        else:
            raise ActionExecutionError(Invalid('Invalid context'))
        url = '%s/%s/edit' % (self.context.absolute_url(), self.comment)
        return self.request.response.redirect(url)


class EditAnswerAndCloseComments(grok.View):
    grok.name('edit-answer-and-close-comments')
    grok.context(IQuestion)
    grok.require('zope2.View')

    def update(self):
        waction = self.request.get('workflow_action')
        comment = self.request.get('comment')
        if waction not in ('phase1-ask-answer-approval', 'phase2-ask-answer-aproval') and comment not in self.context.keys():
            status = IStatusMessage(self.request)
            msg = _('There was an error, try again please')
            status.addStatusMessage(msg, 'error')
            return
        self.comment = comment

    def render(self):
        if api.content.get_state(self.context).startswith('phase1-'):
            api.content.transition(obj=self.context, transition='phase1-ask-answer-approval')
        elif api.content.get_state(self.context).startswith('phase2-'):
            api.content.transition(obj=self.context, transition='phase2-ask-answer-aproval')
        else:
            raise ActionExecutionError(Invalid('Invalid context'))
        url = '%s/%s/edit' % (self.context.absolute_url(), self.comment)
        return self.request.response.redirect(url)


class AddFollowUpQuestion(grok.View):
    grok.context(IQuestion)
    grok.name('add-follow-up-question')
    grok.require('zope2.View')

    def render(self):
        if api.content.get_state(self.context).startswith('phase1-'):
            api.content.transition(obj=self.context, transition='phase1-reopen')
        elif api.content.get_state(self.context).startswith('phase2-'):
            api.content.transition(obj=self.context, transition='phase2-reopen')
        else:
            raise ActionExecutionError(Invalid('Invalid context'))
        url = '%s/++add++Comment' % self.context.absolute_url()
        return self.request.response.redirect(url)


class AddConclusions(grok.View):
    grok.context(IQuestion)
    grok.name('add-conclusions')
    grok.require('zope2.View')

    def render(self):
        parent = aq_parent(self.context)
        if api.content.get_state(parent).startswith('phase1-'):
            conclusion = parent.get_conclusion()
            if not conclusion:
                url = '%s/++add++Conclusion' % parent.absolute_url()
            else:
                url = '%s/edit' % conclusion.absolute_url()
        elif api.content.get_state(parent).startswith('phase2-'):
            conclusionsphase2 = parent.get_conclusion_phase2()
            if not conclusionsphase2:
                api.content.transition(obj=parent, transition='phase2-draft-conclusions')
                cp2 = parent.invokeFactory(id=int(time()), type_name='ConclusionsPhase2')
                conclusionsphase2 = parent.get(cp2)
            url = '%s/edit' % conclusionsphase2.absolute_url()
        else:
            raise ActionExecutionError(Invalid('Invalid context'))
        return self.request.response.redirect(url)


class DeleteLastComment(grok.View):
    grok.context(IQuestion)
    grok.name('delete-last-comment')
    grok.require('zope2.View')

    def render(self):
        catalog = api.portal.get_tool('portal_catalog')
        answers = [ c for c in self.context.values() if c.portal_type == 'CommentAnswer' ]
        comments = [ c for c in self.context.values() if c.portal_type == 'Comment' ]
        if comments and len(comments) > len(answers):
            last_comment = comments[(-1)]
            question = aq_inner(self.context)
            if len(comments) == 1:
                self.context.manage_delObjects([last_comment.getId()])
                catalog.unindexObject(last_comment)
                observation = aq_parent(question)
                del observation[question.getId()]
                return self.request.response.redirect(observation.absolute_url())
            question_state = api.content.get_state(obj=question)
            self.context.manage_delObjects([last_comment.getId()])
            catalog.unindexObject(last_comment)
            url = question.absolute_url()
            if question_state == 'phase1-draft':
                url += '/content_status_modify?workflow_action=phase1-delete-question'
            elif question_state == 'phase2-draft':
                url += '/content_status_modify?workflow_action=phase2-delete-question'
            return self.request.response.redirect(url)


class DeleteLastAnswer(grok.View):
    grok.context(IQuestion)
    grok.name('delete-last-answer')
    grok.require('zope2.View')

    def render(self):
        question = aq_inner(self.context)
        url = question.absolute_url()
        answers = [ c for c in self.context.values() if c.portal_type == 'CommentAnswer' ]
        comments = [ c for c in self.context.values() if c.portal_type == 'Comment' ]
        if answers and len(answers) == len(comments):
            last_answer = answers[(-1)]
            question_state = api.content.get_state(obj=question)
            self.context.manage_delObjects([last_answer.getId()])
            if question_state == 'phase1-pending-answer-drafting':
                url += '/content_status_modify?workflow_action=phase1-delete-answer'
            elif question_state == 'phase2-pending-answer-drafting':
                url += '/content_status_modify?workflow_action=phase2-delete-answer'
            return self.request.response.redirect(url)
        return self.request.response.redirect(url)