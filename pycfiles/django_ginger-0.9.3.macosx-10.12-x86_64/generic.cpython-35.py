# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/views/generic.py
# Compiled at: 2017-01-03 06:43:46
# Size of source mod 2**32: 24485 bytes
from django import forms
import os, inspect
from datetime import timedelta
from django.utils.six.moves.urllib.parse import urljoin
from django.core.paginator import EmptyPage, Page
from django.forms.fields import FileField
from django.contrib import messages
from django.utils import timezone, six
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.forms.models import ModelForm
from django.utils.functional import cached_property
from django.views.generic.base import TemplateResponseMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from ginger.exceptions import Http404, Redirect, BadRequest
from ginger.serializer import process_redirect
from ginger.templates import GingerResponse
from ginger.paginator import paginate
from . import storages
from . import steps
from .base import GingerView, GingerViewSetMixin
from ginger.ui import Link
__all__ = [
 'GingerView', 'GingerTemplateView', 'GingerSearchView',
 'GingerDetailView', 'GingerFormView', 'GingerWizardView',
 'GingerFormDoneView', 'GingerListView', 'GingerDeleteView',
 'GingerEditView', 'GingerEditDoneView', 'GingerEditWizardView',
 'GingerNewDoneView', 'GingerNewView', 'GingerNewWizardView', 'PostFormMixin',
 'GingerMultipleFormView']

class GingerTemplateView(GingerView, TemplateResponseMixin):
    view_icon = None
    view_label = None
    page_title = None
    page_heading = None
    page_actions = ()
    page_css_class = None
    response_class = GingerResponse

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def process_exception(self, request, ex):
        result = super(GingerTemplateView, self).process_exception(request, ex)
        if result is None and isinstance(ex, Redirect):
            url = ex.create_url(request)
            result = self.redirect(url)
        return result

    def redirect(self, to, **kwargs):
        response = redirect(to, **kwargs)
        if self.request.is_ajax():
            status, content = process_redirect(self.request, response)
            return self.render_to_response(content, status=status, content_type='application/json')
        else:
            return response

    def get_template_names(self):
        template_name = getattr(self, 'template_name', None)
        if template_name is None:
            return [self.meta.template_name]
        return [
         template_name]

    def build_link(self):
        url = self.reverse(*self.args, **self.kwargs)
        is_active = self.request.path_info == url
        return Link(content=self.get_page_label(), icon=self.get_page_icon(), is_active=is_active, url=url)

    @classmethod
    def as_link(cls, *args, **kwargs):
        ins = cls.instantiate(*args, **kwargs)
        return ins.build_link()

    def get_page_css_class(self, ctx):
        return self.page_css_class

    def get_page_title(self, ctx):
        return self.page_title or self.get_page_heading(ctx)

    def get_page_heading(self, ctx):
        return self.page_heading

    def get_page_actions(self, ctx):
        return self.page_actions

    def get_view_icon(self):
        return self.view_icon

    def get_view_label(self):
        return self.view_label

    def render_to_response(self, ctx, **response_kwargs):
        if not self.request.is_ajax():
            if six.PY2:
                len(inspect.getargspec(self.get_page_heading).args)
                safe_call = lambda fn, arg: fn(arg) if len(inspect.getargspec(fn).args) > 1 else fn()
            else:
                safe_call = lambda fn, arg: fn(arg) if len(inspect.Signature.from_callable(fn).parameters) > 0 else fn()
            ctx['view'] = self
            ctx.setdefault('page_heading', safe_call(self.get_page_heading, ctx))
            ctx.setdefault('page_title', safe_call(self.get_page_title, ctx))
            ctx.setdefault('page_actions', safe_call(self.get_page_actions, ctx))
            ctx.setdefault('page_css_class', safe_call(self.get_page_css_class, ctx))
        response = super(GingerTemplateView, self).render_to_response(ctx, **response_kwargs)
        return response


class GingerFormView(GingerTemplateView):
    success_url = None
    form_class = None
    context_form_key = 'form'

    def get_context_form_key(self, form):
        key = self.context_form_key or 'form'
        return key

    def get_success_url(self, form):
        return self.success_url

    def get_form_class(self, form_key=None):
        return self.form_class

    def get_form_key(self):
        pass

    def can_submit(self):
        return self.request.method == 'POST'

    def post(self, request, *args, **kwargs):
        if self.can_submit():
            return self.process_submit(form_key=self.get_form_key(), data=request.POST, files=request.FILES)
        return self.redirect(request.get_full_path())

    def get(self, request, *args, **kwargs):
        form_key = self.get_form_key()
        if self.can_submit():
            return self.process_submit(form_key=form_key, data=request.GET)
        else:
            data, files = self.get_form_data(form_key)
            form = self.get_form(form_key=form_key, data=data, files=files)
            return self.render_form(form)

    def get_form_data(self, form_key):
        return (None, None)

    def set_form_data(self, form_key, data, files=None):
        raise NotImplementedError

    def form_valid(self, form):
        url = self.get_success_url(form)
        msg = form.get_success_message()
        self.add_message(level=messages.SUCCESS, message=msg)
        return self.redirect(url)

    def form_invalid(self, form):
        msg = form.get_failure_message()
        self.add_message(level=messages.ERROR, message=msg)
        return self.render_form(form)

    def render_form(self, form):
        form_key = self.get_form_key()
        kwargs = {self.get_context_form_key(form_key): form}
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_form_initial(self, form_key):
        pass

    def get_form_prefix(self, form_key):
        pass

    def get_form_instance(self, form_key):
        pass

    def get_form_context(self, form_key):
        action = self.action
        ctx = {'request': self.request, 
         'user': self.user}
        if action:
            ctx['action'] = action
        return ctx

    def get_form_kwargs(self, form_key):
        kwargs = {'initial': self.get_form_initial(form_key), 
         'prefix': self.get_form_prefix(form_key)}
        form_class = self.get_form_class(form_key)
        if form_class and issubclass(form_class, ModelForm):
            kwargs['instance'] = self.get_form_instance(form_key)
        ctx = self.get_form_context(form_key)
        if ctx:
            kwargs.update(ctx)
        return kwargs

    def process_submit(self, form_key, data=None, files=None):
        form_obj = self.get_form(form_key, data=data, files=files)
        if form_obj.is_valid():
            return self.form_valid(form_obj)
        else:
            return self.form_invalid(form_obj)

    def get_form(self, form_key, data=None, files=None):
        form_class = self.get_form_class(form_key)
        kwargs = self.get_form_kwargs(form_key)
        kwargs['data'] = data
        kwargs['files'] = files
        form_obj = form_class(**kwargs)
        return form_obj


class GingerMultipleFormView(GingerFormView):
    form_classes = {}
    form_key_parameter = '_fkey'

    def get_context_form_key(self, form_key):
        suffix = 'form'
        if not form_key:
            return suffix
        return '%s_%s' % (form_key, suffix)

    def get_form_key(self):
        if not self.can_submit():
            return
        name = self.form_key_parameter
        request = self.request
        data = request.GET if request.method == 'GET' else request.POST
        for key in self.form_classes:
            field_name = '%s-%s' % (key, name)
            if field_name in data:
                return data[field_name]

    def get_form(self, form_key, data=None, files=None):
        form_obj = super(GingerMultipleFormView, self).get_form(form_key, data, files)
        form_obj.fields[self.form_key_parameter] = forms.CharField(widget=forms.HiddenInput, initial=form_key)
        return form_obj

    def get_form_prefix(self, form_key):
        return form_key

    def get_form_class(self, form_key):
        return self.form_classes[form_key]

    def get_unbound_form_keys(self):
        return [k for k in self.form_classes.keys() if k != self.get_form_key()]

    def get(self, request, *args, **kwargs):
        key = self.get_form_key()
        if key is None:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return self.process_submit(key, data=request.GET, files=None)

    def post(self, request, *args, **kwargs):
        key = self.get_form_key()
        if key is None:
            return self.redirect(request.get_full_path())
        return self.process_submit(key, data=request.POST, files=request.FILES)

    def get_context_data(self, **kwargs):
        context = super(GingerMultipleFormView, self).get_context_data(**kwargs)
        for form_key in self.get_unbound_form_keys():
            data, files = self.get_form_data(form_key)
            form = self.get_form(form_key=form_key, data=data, files=files)
            context[self.get_context_form_key(form_key)] = form

        return context


class GingerSearchView(GingerFormView):
    per_page = 20
    page_parameter_name = 'page'
    page_limit = 10
    paginate = True
    context_object_list_key = 'object_list'
    context_page_key = 'page_object'

    def get_form_kwargs(self, form_key):
        ctx = super(GingerSearchView, self).get_form_kwargs(form_key)
        if self.paginate:
            ctx['parameter_name'] = self.page_parameter_name
            ctx['page_limit'] = self.page_limit
            ctx['per_page'] = self.per_page
            ctx['page'] = self.request
            if hasattr(self, 'queryset'):
                ctx['queryset'] = self.queryset
        return ctx

    def get_context_data(self, **kwargs):
        ctx = super(GingerSearchView, self).get_context_data(**kwargs)
        form = ctx['form']
        ctx[self.context_object_list_key] = form.result
        if isinstance(form.result, Page):
            ctx[self.context_page_key] = form.result
        return ctx

    def can_submit(self):
        return self.request.method == 'GET'

    def form_valid(self, form):
        return self.render_form(form)

    def get(self, request, *args, **kwargs):
        try:
            return super(GingerSearchView, self).get(request, *args, **kwargs)
        except EmptyPage:
            raise Http404


class GingerStepViewMixin(object):
    step_parameter_name = 'step'
    done_step = 'done'
    context_done_object_name = 'done_object'

    def commit(self, form_data):
        raise NotImplementedError

    def get_step_names(self):
        raise NotImplementedError

    def get_form_key(self):
        return self.current_step_name()

    def current_step_name(self):
        return self.kwargs.get(self.step_parameter_name)

    def get_step_url(self, step_name):
        match = self.request.resolver_match
        params = self.kwargs.copy()
        params.pop(self.step_parameter_name, None)
        if step_name is not None:
            params[self.step_parameter_name] = step_name
        return reverse(match.url_name, args=tuple(self.args), kwargs=params)

    def get_done_url(self):
        return self.get_step_url(self.done_step)

    def process_commit(self):
        raise NotImplementedError

    def process_submit(self, *args, **kwargs):
        self.clear_session_data()
        return super(GingerStepViewMixin, self).process_submit(*args, **kwargs)

    def render_done(self):
        data = self.get_session_data()
        if data is None:
            response = self.process_commit()
            if response:
                return response
            data = self.get_session_data()
        kwargs = self.kwargs.copy()
        kwargs[self.context_done_object_name] = data
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def is_done_step(self):
        return self.current_step_name() == self.done_step and self.request.method == 'GET'

    def dispatch(self, request, *args, **kwargs):
        step_name = self.current_step_name()
        step_names = self.get_step_names()
        if step_name is None:
            if step_names:
                return self.redirect(self.get_step_url(step_names[0]))
        elif step_name not in step_names and not self.is_done_step():
            raise Http404
        return super(GingerStepViewMixin, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        step_name = self.current_step_name()
        method = getattr(self, 'process_%s_step' % step_name, None)
        if method:
            response = method()
            if response:
                pass
            return response
        if self.is_done_step():
            return self.render_done()
        return super(GingerStepViewMixin, self).get(request, *args, **kwargs)


class GingerFormDoneView(GingerStepViewMixin, GingerFormView):

    def get_step_names(self):
        return ()

    def process_commit(self):
        return self.redirect(self.get_step_url(None))

    def form_valid(self, form):
        result = form.result
        self.set_session_data(result)
        return self.redirect(self.get_done_url())

    def get_template_names(self):
        template_names = super(GingerFormDoneView, self).get_template_names()
        if not isinstance(template_names, (list, tuple)):
            template_names = [
             template_names]
        if self.is_done_step():
            result = []
            for template_name in template_names:
                base, ext = os.path.splitext(template_name)
                result.append('%s_%s%s' % (base, self.done_step, ext))

            template_names = result
        return template_names


class GingerWizardView(GingerStepViewMixin, GingerFormView):
    template_format = None
    file_upload_dir = 'tmp/'
    form_storage_class = storages.SessionFormStorage

    def __init__(self, *args, **kwargs):
        super(GingerWizardView, self).__init__(*args, **kwargs)
        self.file_storage = self.get_file_storage()
        self.steps = steps.StepList(self)

    def is_submitted(self, form_key):
        return form_key == self.current_step_name() and self.can_submit()

    def get_form_initial(self, form_key):
        initial = {}
        if self.is_submitted(form_key):
            _, files = self.get_form_data(form_key)
            if files:
                initial.update(files)
        return initial

    @cached_property
    def form_storage(self):
        return self.get_form_storage()

    def get_form_storage(self):
        return self.form_storage_class(self)

    def get_file_storage(self):
        location = self.file_upload_dir or getattr(settings, 'TEMP_MEDIA_DIR', 'tmp')
        return FileSystemStorage(os.path.join(settings.MEDIA_ROOT, location), base_url=urljoin(settings.MEDIA_URL, location))

    def get_template_names(self):
        if self.template_format is None:
            raise ImproperlyConfigured('template_format cannot be None in %r' % self.__class__)
        step_name = self.current_step_name()
        return self.template_format % {'step': step_name}

    def get_form_data(self, form_key):
        return self.form_storage.get(form_key)

    def set_form_data(self, form_key, data, files=None):
        self.form_storage.set(form_key, data, files)

    def get_form_class(self, form_key=None):
        step_name = form_key
        if step_name is None:
            step_name = self.current_step_name()
        return self.steps[step_name].get_form_class()

    def get_next_url(self):
        step = self.steps.next()
        if step:
            return step.url
        return self.get_done_url()

    def form_valid(self, form):
        step_name = self.current_step_name()
        files = form.files.copy()
        data = form.data.copy()
        cleaned_data = form.cleaned_data
        for name, f in six.iteritems(form.fields):
            if isinstance(f, FileField) and name not in files and name in cleaned_data:
                file_obj = cleaned_data[name]
                if file_obj is not None:
                    files[name] = cleaned_data[name]
                    data.pop(name, None)

        self.set_form_data(step_name, data, files)
        url = self.get_next_url()
        return self.redirect(url)

    def process_commit(self):
        form_data = {}
        for step_name in self.get_step_names():
            form_obj = self.validate_step(step_name)
            step = self.steps[step_name]
            if not form_obj.is_valid() and (not step.can_skip or form_obj.is_bound):
                return self.redirect(self.get_step_url(step_name))
            form_data.update(form_obj.cleaned_data)

        data = self.commit(form_data)
        self.set_session_data(data)
        self.form_storage.clear()

    def get_step_names(self):
        return self.steps.names()

    def commit(self, form_data):
        return {}

    def get_cleaned_data_for_step(self, step_name):
        form_obj = self.validate_step(step_name)
        try:
            return form_obj.cleaned_data
        except AttributeError:
            return

    def get_cleaned_data(self, step_names=None):
        result = {}
        for form_obj in self.validate_steps(step_names):
            try:
                data = form_obj.cleaned_data
                result.update(data)
            except AttributeError:
                continue

        return result

    def can_submit(self):
        if self.is_done_step():
            return False
        method = self.steps.current.method
        request = self.request
        if request.method == 'POST' or method == 'GET' and request.method == 'GET' and request.GET:
            return True
        return False

    def validate_step(self, step_name):
        data, files = self.get_form_data(step_name)
        form_obj = self.get_form(step_name, data, files)
        form_obj.step_name = step_name
        form_obj.is_valid()
        return form_obj

    def validate_steps(self, step_names=None):
        if step_names is None:
            step_names = self.get_step_names()
        for step_name in step_names:
            yield self.validate_step(step_name)

    @classmethod
    def delete_old_files(cls, **kwargs):
        wiz = cls()
        expired = timezone.now() - timedelta(**kwargs)
        file_storage = wiz.get_file_storage()
        try:
            files = file_storage.listdir('')[(-1)]
        except OSError:
            return

        for filename in files:
            access_time = file_storage.accessed_time(filename)
            if access_time < expired:
                file_storage.delete(filename)


class SingleObjectViewMixin(object):
    url_object_key = 'object_id'
    url_object_type = 'int'
    queryset_object_key = 'pk'
    context_object_key = 'object'

    def get_context_object_key(self, obj):
        key = self.context_object_key or obj._meta.model_name
        return key

    def get_queryset_object_key(self):
        return self.queryset_object_key

    def get_queryset(self):
        return self.queryset

    def get_form_instance(self, form_key):
        return self.object

    def get_object(self):
        key = self.get_queryset_object_key()
        kwargs = {key: self.kwargs[self.url_object_key]}
        try:
            return self.get_queryset().get(**kwargs)
        except ObjectDoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        ctx = super(SingleObjectViewMixin, self).get_context_data(**kwargs)
        ctx[self.get_context_object_key(self.object)] = self.object
        return ctx

    @classmethod
    def create_url_regex(cls):
        key, kind = cls.url_object_key, cls.url_object_type
        return '%s:%s/%s/' % (key, kind, cls.meta.url_verb)


class MultipleObjectViewMixin(object):
    context_object_key = 'object_list'

    def get_target(self):
        return self.queryset

    def get_queryset(self):
        return self.queryset

    def get_context_object_key(self, object_list):
        key = self.context_object_key
        if not key:
            key = '%s_list' % object_list._meta.model_name
        return key


class GingerDetailView(SingleObjectViewMixin, GingerTemplateView):
    pass


class GingerEditView(SingleObjectViewMixin, GingerFormView):

    def get_success_url(self, form):
        return self.success_url or form.instance.get_absolute_url()


class GingerEditDoneView(SingleObjectViewMixin, GingerFormDoneView):

    def get_success_url(self, form):
        return self.success_url or form.instance.get_absolute_url()


class GingerEditWizardView(SingleObjectViewMixin, GingerWizardView):
    pass


class GingerDeleteView(SingleObjectViewMixin, GingerFormView):
    pass


class GingerNewView(GingerFormView):

    def get_success_url(self, form):
        return self.success_url or form.instance.get_absolute_url()


class GingerNewDoneView(GingerFormDoneView):

    def get_success_url(self, form):
        return self.success_url or form.instance.get_absolute_url()


class GingerNewWizardView(GingerWizardView):
    pass


class GingerListView(MultipleObjectViewMixin, GingerTemplateView):
    per_page = 20
    page_parameter_name = 'page'
    page_limit = 10
    paginate = True
    context_page_key = 'page_object'

    def paginate_queryset(self, queryset):
        return paginate(queryset, self.request, parameter_name=self.page_parameter_name, per_page=self.per_page, page_limit=self.page_limit)

    def get_context_data(self, **kwargs):
        ctx = super(GingerListView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        if self.paginate:
            queryset = self.paginate_queryset(queryset)
        ctx[self.get_context_object_key(queryset)] = queryset
        ctx[self.context_page_key] = queryset
        return ctx


class PostFormMixin(object):

    def get(self, request, *args, **kwargs):
        raise BadRequest()

    def get_referrer_url(self):
        return self.request.META['HTTP_REFERER']


class GingerObjectCreateView(GingerFormView):

    def get(self, request, *args, **kwargs):
        self.object = None
        return super(GingerObjectCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return self.delete(request, *args, **kwargs)


class GingerObjectDetailView(GingerTemplateView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(GingerDetailView, self).get(request, *args, **kwargs)


class GingerObjectDeleteView(GingerFormView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(GingerDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.process_submit()


class GingerObjectEditView(GingerFormView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(GingerDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.delete(request, *args, **kwargs)


class GingerObjectListFilterView(GingerSearchView):
    pass


class GingerObjectListEditView(GingerFormView):
    pass