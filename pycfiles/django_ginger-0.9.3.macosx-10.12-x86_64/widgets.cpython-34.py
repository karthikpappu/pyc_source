# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/forms/widgets.py
# Compiled at: 2015-11-27 03:35:40
# Size of source mod 2**32: 2491 bytes
from django import forms
from django.utils.encoding import force_text
from ginger import html
import itertools
__all__ = [
 'ChoiceWidgetMixin', 'DateInput', 'DateRangeWidget', 'TimeInput', 'DateTimeInput',
 'ComboBox', 'ComboBoxMultiple', 'TaggedInput', 'SwitchInput', 'HTMLEditor',
 'MarkdownEditor', 'NumberRangeWidget']

class ChoiceWidgetMixin(object):
    input_type = 'radio'

    def render_from_field(self, field):
        return field.as_widget(widget=self)

    def render_subwidget_wrapper(self, content):
        classes = []
        return html.li(class_=classes)[content]

    def render_subwidget(self, code, label, selected, attrs):
        return [
         html.input(type=self.input_type, checked=selected, value=code, **attrs),
         html.label(for_=attrs.get('id'))[label]]

    def render_wrapper(self, content, attrs):
        return html.ul(**attrs)[content].render()

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        attrs = self.build_attrs(attrs, name=name)
        children = []
        id_ = attrs.get('id')
        for i, (code, label) in enumerate(itertools.chain(self.choices, choices)):
            selected = html.is_selected_choice(value, code)
            child_attrs = attrs.copy()
            child_attrs.pop('class', None)
            if id_:
                child_attrs['id'] = '%s-%s' % (id_, i)
            child = self.render_subwidget(code, label, selected, child_attrs)
            children.append(self.render_subwidget_wrapper(child))

        return self.render_wrapper(''.join(force_text(child) for child in children), attrs)


class EmptyWidget(forms.HiddenInput):
    __doc__ = '\n    No html is produced. This is used for PageField\n    '

    def render(self, name, value, attrs=None):
        return ''


class ComboBox(forms.Select):
    pass


class ComboBoxMultiple(forms.SelectMultiple):
    pass


class TaggedInput(forms.TextInput):
    pass


class SwitchInput(forms.CheckboxInput):
    pass


class HTMLEditor(forms.Textarea):
    pass


class MarkdownEditor(forms.Textarea):
    pass


class DateRangeWidget(forms.MultiWidget):
    pass


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'
    extra_attrs = {'class': 'datetimepicker'}


class NumberRangeWidget(forms.NumberInput):
    pass