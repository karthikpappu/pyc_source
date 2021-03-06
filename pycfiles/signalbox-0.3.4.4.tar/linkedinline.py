# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/utilities/linkedinline.py
# Compiled at: 2014-08-27 19:26:12
from django.core.urlresolvers import reverse
from django.contrib import admin

def admin_edit_url(self, indirect_pk_field=''):
    """
    Returns an admin url; to be called from classes used with linkedinlines.

    If used directly in an inline then the model method would look like this:

        def admin_edit_url(self):
                return admin_edit_url(self)

    Whereas if, for example, a question were used indirectly in a page using an
    extra 'through' model, it would look like this:

        def admin_edit_url(self):
            return admin_edit_url(self, indirect_pk_field='question')

    """
    actual_obj = getattr(self, indirect_pk_field, self)
    class_name = actual_obj._meta.object_name.lower()
    app_label = actual_obj._meta.app_label
    return reverse('admin:%s_%s_change' % (app_label, class_name), args=(actual_obj.pk,))


class LinkedInline(admin.options.InlineModelAdmin):
    template = 'admin/tabular.html'