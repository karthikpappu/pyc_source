# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-admin/ovp_admin/templatetags/ovp_admin_template_tags.py
# Compiled at: 2017-01-10 11:12:37
# Size of source mod 2**32: 6969 bytes
from django.contrib.admin import site
from django.apps import apps
from django.utils.text import capfirst
from django.core.urlresolvers import reverse, NoReverseMatch
from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.conf import settings
from django import template
from django import VERSION as DJANGO_VERSION
try:
    from functools import reduce
except ImportError:
    pass

register = template.Library()
MAX_LENGTH_BOOTSTRAP_COLUMN = 12

def css_classes_for_field(field, custom_classes):
    orig_class = field.field.widget.attrs.get('class', '')
    required = 'required' if field.field.required else ''
    classes = field.css_classes(' '.join([orig_class, custom_classes, required]))
    return classes


@register.filter()
def get_label(field, custom_classes=''):
    classes = css_classes_for_field(field, custom_classes)
    return field.label_tag(attrs={'class': classes}, label_suffix='')


@register.filter()
def add_class(field, custom_classes=''):
    classes = css_classes_for_field(field, custom_classes)
    try:
        field.field.widget.widget.attrs.update({'class': classes})
    except:
        field.field.widget.attrs.update({'class': classes})

    return field


@register.filter()
def widget_type(field):
    if isinstance(field, dict):
        return 'adminreadonlyfield'
        try:
            widget_type = field.field.widget.widget.__class__.__name__.lower()
        except:
            widget_type = field.field.widget.__class__.__name__.lower()

        return widget_type


@register.filter()
def placeholder(field, placeholder=''):
    field.field.widget.attrs.update({'placeholder': placeholder})
    return field


def sidebar_menu_setting():
    return getattr(settings, 'OVP_ADMIN_SIDEBAR_MENU', False)


@register.assignment_tag
def display_sidebar_menu(has_filters=False):
    if has_filters:
        return True
    return sidebar_menu_setting()


@register.assignment_tag
def jquery_vendor_path():
    if DJANGO_VERSION < (1, 9):
        return 'ovp_admin/js/jquery.js'
    return 'admin/js/vendor/jquery/jquery.js'


@register.assignment_tag
def datetime_widget_css_path():
    if DJANGO_VERSION < (1, 9):
        return ''
    return 'admin/css/datetime_widget.css'


@register.inclusion_tag('ovp_admin/sidebar_menu.html', takes_context=True)
def render_menu_app_list(context):
    show_global_menu = sidebar_menu_setting()
    if not show_global_menu:
        return {'app_list': ''}
    if DJANGO_VERSION < (1, 8):
        dependencie = 'django.core.context_processors.request'
        processors = settings.TEMPLATE_CONTEXT_PROCESSORS
        dependency_str = 'settings.TEMPLATE_CONTEXT_PROCESSORS'
    else:
        dependencie = 'django.template.context_processors.request'
        implemented_engines = getattr(settings, 'OVP_ADMIN_ENGINES', [
         'django.template.backends.django.DjangoTemplates'])
        dependency_str = "the 'context_processors' 'OPTION' of one of the " + 'following engines: %s' % implemented_engines
        filtered_engines = [engine for engine in settings.TEMPLATES if engine['BACKEND'] in implemented_engines]
        if len(filtered_engines) == 0:
            raise ImproperlyConfigured('ovp_admin: No compatible template engine found' + 'ovp_admin requires one of the following engines: %s' % implemented_engines)
        processors = reduce(lambda x, y: x.extend(y), [engine.get('OPTIONS', {}).get('context_processors', []) for engine in filtered_engines])
    if dependencie not in processors:
        raise ImproperlyConfigured("ovp_admin: in order to use the 'sidebar menu' requires" + " the '%s' to be added to %s" % (
         dependencie, dependency_str))
    app_dict = {}
    user = context.get('user')
    for model, model_admin in site._registry.items():
        app_label = model._meta.app_label
        has_module_perms = user.has_module_perms(app_label)
        if has_module_perms:
            pass
        perms = model_admin.get_model_perms(context.get('request'))
        if True in perms.values():
            info = (
             app_label, model._meta.model_name)
            model_dict = {'name': capfirst(model._meta.verbose_name_plural), 
             'object_name': model._meta.object_name, 
             'perms': perms, 
             'show_on_menu': False}
            if hasattr(model_admin, 'display_on_main_menu'):
                model_dict['show_on_menu'] = model_admin.display_on_main_menu
            if perms.get('change', False):
                try:
                    model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=site.name)
                except NoReverseMatch:
                    pass

                if perms.get('add', False):
                    try:
                        model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=site.name)
                    except NoReverseMatch:
                        pass

                    if app_label in app_dict:
                        app_dict[app_label]['models'].append(model_dict)
                    else:
                        app_dict[app_label] = {'name': apps.get_app_config(app_label).verbose_name, 
                         'app_label': app_label, 
                         'app_url': reverse('admin:app_list', kwargs={'app_label': app_label}, current_app=site.name), 
                         
                         'has_module_perms': has_module_perms, 
                         'models': [model_dict]}

    app_list = list(six.itervalues(app_dict))
    app_list.sort(key=lambda x: x['name'].lower())
    for app in app_list:
        app['models'].sort(key=lambda x: x['name'])

    return {'app_list': app_list, 'current_url': context.get('request').path}


@register.filter()
def class_for_field_boxes(line):
    size_column = MAX_LENGTH_BOOTSTRAP_COLUMN // len(line.fields)
    return 'col-sm-{0}'.format(size_column or 1)