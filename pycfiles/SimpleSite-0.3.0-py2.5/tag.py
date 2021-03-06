# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplesite/controllers/tag.py
# Compiled at: 2008-11-08 10:05:16
import logging
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from simplesite.lib.base import BaseController, render
from simplesite import model
import simplesite.model.meta as meta, simplesite.lib.helpers as h, formencode
from formencode import htmlfill
from pylons.decorators import validate
from pylons.decorators.rest import restrict
import webhelpers.paginate as paginate
from sqlalchemy import delete
log = logging.getLogger(__name__)
import re

class UniqueTag(formencode.validators.FancyValidator):

    def _to_python(self, value, state):
        value = formencode.validators.String(max=20).to_python(value, state)
        result = re.compile('[^a-zA-Z0-9 ]').search(value)
        if result:
            raise formencode.Invalid('Tags can only contain letters, numbers and spaces', value, state)
        tag_q = meta.Session.query(model.Tag).filter_by(name=value)
        if request.urlvars['action'] == 'save':
            tag_q = tag_q.filter(model.Tag.id != int(request.urlvars['id']))
        first_tag = tag_q.first()
        if first_tag is not None:
            raise formencode.Invalid('This tag name already exists', value, state)
        return value


class NewTagForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = UniqueTag(not_empty=True)


class TagController(BaseController):

    def view(self, id=None):
        if id is None:
            abort(404)
        tag_q = meta.Session.query(model.Tag)
        c.tag = tag_q.get(int(id))
        if c.tag is None:
            abort(404)
        return render('/derived/tag/view.html')

    def new(self):
        return render('/derived/tag/new.html')

    @restrict('POST')
    @validate(schema=NewTagForm(), form='new')
    def create(self):
        tag = model.Tag()
        for (k, v) in self.form_result.items():
            setattr(tag, k, v)

        meta.Session.add(tag)
        meta.Session.commit()
        response.status_int = 302
        response.headers['location'] = h.url_for(controller='tag', action='view', id=tag.id)
        return 'Moved temporarily'

    @h.auth.authorize(h.auth.has_delete_role)
    def edit(self, id=None):
        if id is None:
            abort(404)
        tag_q = meta.Session.query(model.Tag)
        tag = tag_q.filter_by(id=id).first()
        if tag is None:
            abort(404)
        values = {'name': tag.name}
        return htmlfill.render(render('/derived/tag/edit.html'), values)

    @h.auth.authorize(h.auth.has_delete_role)
    @restrict('POST')
    @validate(schema=NewTagForm(), form='edit')
    def save(self, id=None):
        tag_q = meta.Session.query(model.Tag)
        tag = tag_q.filter_by(id=id).first()
        if tag is None:
            abort(404)
        for (k, v) in self.form_result.items():
            if getattr(tag, k) != v:
                setattr(tag, k, v)

        meta.Session.commit()
        session['flash'] = 'Tag successfully updated.'
        session.save()
        response.status_int = 302
        response.headers['location'] = h.url_for(controller='tag', action='view', id=tag.id)
        return 'Moved temporarily'

    @h.auth.authorize(h.auth.has_delete_role)
    def list(self):
        tag_q = meta.Session.query(model.Tag)
        c.paginator = paginate.Page(tag_q, page=int(request.params.get('page', 1)), items_per_page=10, controller='tag', action='list')
        return render('/derived/tag/list.html')

    @h.auth.authorize(h.auth.has_delete_role)
    def delete(self, id=None):
        if id is None:
            abort(404)
        tag_q = meta.Session.query(model.Tag)
        tag = tag_q.filter_by(id=id).first()
        if tag is None:
            abort(404)
        meta.Session.execute(delete(model.pagetag_table, model.pagetag_table.c.tagid == tag.id))
        meta.Session.delete(tag)
        meta.Session.commit()
        return render('/derived/tag/deleted.html')