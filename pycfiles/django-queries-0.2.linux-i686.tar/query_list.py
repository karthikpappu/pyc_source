# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/queries/templatetags/query_list.py
# Compiled at: 2010-05-22 03:04:48
from django.conf import settings
from queries.views.main import ALL_VAR, EMPTY_CHANGELIST_VALUE
from queries.views.main import ORDER_VAR, ORDER_TYPE_VAR, PAGE_VAR, SEARCH_VAR
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import dateformat
from django.utils.html import escape, conditional_escape
from django.utils.text import capfirst
from django.utils.safestring import mark_safe
from django.utils.translation import get_date_formats, get_partial_date_formats, ugettext as _
from django.utils.encoding import smart_unicode, smart_str, force_unicode
from django.template import Library
import datetime
register = Library()
DOT = '.'

def paginator_number(cl, i):
    if i == DOT:
        return '... '
    else:
        if i == cl.page_num:
            return mark_safe('<span class="this-page">%d</span> ' % (i + 1))
        return mark_safe('<a href="%s"%s>%d</a> ' % (escape(cl.get_query_string({PAGE_VAR: i})), i == cl.paginator.num_pages - 1 and ' class="end"' or '', i + 1))


paginator_number = register.simple_tag(paginator_number)

def pagination(cl):
    paginator, page_num = cl.paginator, cl.page_num
    pagination_required = (not cl.show_all or not cl.can_show_all) and cl.multi_page
    if not pagination_required:
        page_range = []
    else:
        ON_EACH_SIDE = 3
        ON_ENDS = 2
        if paginator.num_pages <= 10:
            page_range = range(paginator.num_pages)
        else:
            page_range = []
            if page_num > ON_EACH_SIDE + ON_ENDS:
                page_range.extend(range(0, ON_EACH_SIDE - 1))
                page_range.append(DOT)
                page_range.extend(range(page_num - ON_EACH_SIDE, page_num + 1))
            else:
                page_range.extend(range(0, page_num + 1))
            if page_num < paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1:
                page_range.extend(range(page_num + 1, page_num + ON_EACH_SIDE + 1))
                page_range.append(DOT)
                page_range.extend(range(paginator.num_pages - ON_ENDS, paginator.num_pages))
            else:
                page_range.extend(range(page_num + 1, paginator.num_pages))
    need_show_all_link = cl.can_show_all and not cl.show_all and cl.multi_page
    return {'cl': cl, 
       'pagination_required': pagination_required, 
       'show_all_url': need_show_all_link and cl.get_query_string({ALL_VAR: ''}), 
       'page_range': page_range, 
       'ALL_VAR': ALL_VAR, 
       '1': 1}


pagination = register.inclusion_tag('query/pagination.html')(pagination)

def result_headers(cl):
    lookup_opts = cl.lookup_opts
    for (i, field_name) in enumerate(cl.list_display):
        attr = None
        try:
            f = lookup_opts.get_field(field_name)
            query_order_field = None
        except models.FieldDoesNotExist:
            if field_name == '__unicode__':
                header = force_unicode(lookup_opts.verbose_name)
            elif field_name == '__str__':
                header = smart_str(lookup_opts.verbose_name)
            else:
                if callable(field_name):
                    attr = field_name
                else:
                    try:
                        attr = getattr(cl.model_query, field_name)
                    except AttributeError:
                        try:
                            attr = getattr(cl.model, field_name)
                        except AttributeError:
                            raise AttributeError, "'%s' model or '%s' objects have no attribute '%s'" % (
                             lookup_opts.object_name, cl.model_query.__class__, field_name)

                    try:
                        header = attr.short_description
                    except AttributeError:
                        if callable(field_name):
                            header = field_name.__name__
                        else:
                            header = field_name
                        header = header.replace('_', ' ')

                query_order_field = getattr(attr, 'query_order_field', None)
            if not query_order_field:
                yield {'text': header}
                continue
        else:
            header = f.verbose_name

        th_classes = []
        new_order_type = 'asc'
        if field_name == cl.order_field or query_order_field == cl.order_field:
            th_classes.append('sorted %sending' % cl.order_type.lower())
            new_order_type = {'asc': 'desc', 'desc': 'asc'}[cl.order_type.lower()]
        yield {'text': header, 'sortable': True, 
           'url': cl.get_query_string({ORDER_VAR: i, ORDER_TYPE_VAR: new_order_type}), 
           'class_attrib': mark_safe(th_classes and ' class="%s"' % (' ').join(th_classes) or '')}

    return


def _boolean_icon(field_val):
    BOOLEAN_MAPPING = {True: 'yes', False: 'no', None: 'unknown'}
    return mark_safe('<img src="%simg/query/icon-%s.gif" alt="%s" />' % (settings.ADMIN_MEDIA_PREFIX, BOOLEAN_MAPPING[field_val], field_val))


def items_for_result(cl, result, form):
    first = True
    pk = cl.lookup_opts.pk.attname
    for field_name in cl.list_display:
        row_class = ''
        try:
            f = cl.lookup_opts.get_field(field_name)
        except models.FieldDoesNotExist:
            try:
                if callable(field_name):
                    attr = field_name
                    value = attr(result)
                elif hasattr(cl.model_query, field_name) and not field_name == '__str__' and not field_name == '__unicode__':
                    attr = getattr(cl.model_query, field_name)
                    value = attr(result)
                else:
                    attr = getattr(result, field_name)
                    if callable(attr):
                        value = attr()
                    else:
                        value = attr
                allow_tags = getattr(attr, 'allow_tags', False)
                boolean = getattr(attr, 'boolean', False)
                if boolean:
                    allow_tags = True
                    result_repr = _boolean_icon(value)
                else:
                    result_repr = smart_unicode(value)
            except (AttributeError, ObjectDoesNotExist):
                result_repr = EMPTY_CHANGELIST_VALUE
            else:
                if not allow_tags:
                    result_repr = escape(result_repr)
                else:
                    result_repr = mark_safe(result_repr)
        else:
            field_val = getattr(result, f.attname)
            if isinstance(f.rel, models.ManyToOneRel):
                if field_val is not None:
                    result_repr = escape(getattr(result, f.name))
                else:
                    result_repr = EMPTY_CHANGELIST_VALUE
            elif isinstance(f, models.DateField) or isinstance(f, models.TimeField):
                if field_val:
                    (date_format, datetime_format, time_format) = get_date_formats()
                    if isinstance(f, models.DateTimeField):
                        result_repr = capfirst(dateformat.format(field_val, datetime_format))
                    elif isinstance(f, models.TimeField):
                        result_repr = capfirst(dateformat.time_format(field_val, time_format))
                    else:
                        result_repr = capfirst(dateformat.format(field_val, date_format))
                else:
                    result_repr = EMPTY_CHANGELIST_VALUE
                row_class = ' class="nowrap"'
            elif isinstance(f, models.BooleanField) or isinstance(f, models.NullBooleanField):
                result_repr = _boolean_icon(field_val)
            elif isinstance(f, models.DecimalField):
                if field_val is not None:
                    result_repr = '%%.%sf' % f.decimal_places % field_val
                else:
                    result_repr = EMPTY_CHANGELIST_VALUE
            elif f.flatchoices:
                result_repr = dict(f.flatchoices).get(field_val, EMPTY_CHANGELIST_VALUE)
            else:
                result_repr = escape(field_val)

        if force_unicode(result_repr) == '':
            result_repr = mark_safe('&nbsp;')
        if first and not cl.list_display_links or field_name in cl.list_display_links:
            table_tag = {True: 'th', False: 'td'}[first]
            first = False
            url = cl.url_for_result(result)
            if cl.to_field:
                attr = str(cl.to_field)
            else:
                attr = pk
            value = result.serializable_value(attr)
            result_id = repr(force_unicode(value))[1:]
            yield mark_safe('<%s%s><a href="%s"%s>%s</a></%s>' % (
             table_tag, row_class, url, cl.is_popup and ' onclick="opener.dismissRelatedLookupPopup(window, %s); return false;"' % result_id or '', conditional_escape(result_repr), table_tag))
        else:
            if form and field_name in form.fields:
                bf = form[field_name]
                result_repr = mark_safe(force_unicode(bf.errors) + force_unicode(bf))
            else:
                result_repr = conditional_escape(result_repr)
            yield mark_safe('<td%s>%s</td>' % (row_class, result_repr))

    if form:
        yield mark_safe(force_unicode(form[cl.model._meta.pk.name]))
    return


def results(cl):
    if cl.formset:
        for (res, form) in zip(cl.result_list, cl.formset.forms):
            yield list(items_for_result(cl, res, form))

    else:
        for res in cl.result_list:
            yield list(items_for_result(cl, res, None))

        return


def result_list(cl):
    return {'cl': cl, 'result_headers': list(result_headers(cl)), 
       'results': list(results(cl))}


result_list = register.inclusion_tag('query/change_list_results.html')(result_list)

def date_hierarchy(cl):
    if cl.date_hierarchy:
        field_name = cl.date_hierarchy
        year_field = '%s__year' % field_name
        month_field = '%s__month' % field_name
        day_field = '%s__day' % field_name
        field_generic = '%s__' % field_name
        year_lookup = cl.params.get(year_field)
        month_lookup = cl.params.get(month_field)
        day_lookup = cl.params.get(day_field)
        (year_month_format, month_day_format) = get_partial_date_formats()
        link = lambda d: cl.get_query_string(d, [field_generic])
        if year_lookup and month_lookup and day_lookup:
            day = datetime.date(int(year_lookup), int(month_lookup), int(day_lookup))
            return {'show': True, 
               'back': {'link': link({year_field: year_lookup, month_field: month_lookup}), 
                        'title': dateformat.format(day, year_month_format)}, 
               'choices': [{'title': dateformat.format(day, month_day_format)}]}
        if year_lookup and month_lookup:
            days = cl.query_set.filter(**{year_field: year_lookup, month_field: month_lookup}).dates(field_name, 'day')
            return {'show': True, 
               'back': {'link': link({year_field: year_lookup}), 
                        'title': year_lookup}, 
               'choices': [ {'link': link({year_field: year_lookup, month_field: month_lookup, day_field: day.day}), 'title': dateformat.format(day, month_day_format)} for day in days
                        ]}
        if year_lookup:
            months = cl.query_set.filter(**{year_field: year_lookup}).dates(field_name, 'month')
            return {'show': True, 
               'back': {'link': link({}), 
                        'title': _('All dates')}, 
               'choices': [ {'link': link({year_field: year_lookup, month_field: month.month}), 'title': dateformat.format(month, year_month_format)} for month in months
                        ]}
        years = cl.query_set.dates(field_name, 'year')
        return {'show': True, 
           'choices': [ {'link': link({year_field: year.year}), 'title': year.year} for year in years
                    ]}


date_hierarchy = register.inclusion_tag('query/date_hierarchy.html')(date_hierarchy)

def search_form(cl):
    return {'cl': cl, 
       'show_result_count': cl.result_count != cl.full_result_count, 
       'search_var': SEARCH_VAR}


search_form = register.inclusion_tag('query/search_form.html')(search_form)

def query_list_filter(cl, spec):
    return {'title': spec.title(), 'choices': list(spec.choices(cl))}


query_list_filter = register.inclusion_tag('query/filter.html')(query_list_filter)

def query_actions(context):
    """
    Track the number of times the action field has been rendered on the page,
    so we know which value to use.
    """
    context['action_index'] = context.get('action_index', -1) + 1
    return context


query_actions = register.inclusion_tag('query/actions.html', takes_context=True)(query_actions)