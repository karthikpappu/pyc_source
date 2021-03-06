# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/sphboard/boardforms.py
# Compiled at: 2012-03-17 12:42:14
from django import forms
from django.utils.translation import ugettext_lazy as _
from sphene.sphboard.models import Category
from sphene.community.middleware import get_current_group, get_current_user

class SelectCategoryWidget(forms.Widget):

    def __init__(self, *args, **kwargs):
        super(SelectCategoryWidget, self).__init__(*args, **kwargs)

    def _print_category_option(self, output, categories, depth=0):
        for category in categories:
            output.append('<option value="%s">%s%s</option>' % (category.id, '&nbsp;' * (depth * 5), category.name))
            self._print_category_option(output, category.get_children(), depth + 1)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        output = ['<select%s><option value="">%s</option>' % (forms.util.flatatt(final_attrs), _('-- Select Category --'))]
        group = get_current_group()
        categories = Category.objects.filter(group=group, parent__isnull=True)
        self._print_category_option(output, categories)
        output.append('</select>')
        return ('\n').join(output)


class SelectCategoryField(forms.Field):
    """
    A field which requires a valid category (id) as input.
    The cleaned value is an instance of the Category model.

    (There is currently no way to check for permissions.)
    """
    widget = SelectCategoryWidget

    def __init__(self, *args, **kwargs):
        super(SelectCategoryField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(SelectCategoryField, self).clean(value)
        if value in forms.fields.EMPTY_VALUES:
            return None
        else:
            category = Category.objects.get(pk=value, group=get_current_group())
            value = category
            return value