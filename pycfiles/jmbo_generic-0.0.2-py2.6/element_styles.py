# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/generic/templatetags/element_styles.py
# Compiled at: 2011-09-27 08:43:58
from django.template.loader import render_to_string
from jmbo import models
from generic import views

class Promo(object):
    template_name = 'generic/inclusion_tags/element_promo.html'

    def __init__(self, element):
        self.element = element

    def get_queryset(self):
        queryset = self.element.content.all()
        if not queryset:
            queryset = models.ModelBase.permitted.all()
            if self.element.category:
                queryset = queryset.filter(categories=self.element.category)
        return queryset[:self.element.count]

    def get_url_callable(self, *args, **kwargs):
        return views.CategoryURL(category=self.element.category)

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['object_list'] = self.get_queryset()
        context['element'] = self.element
        context['url_callable'] = self.get_url_callable()
        return context

    def render(self, context):
        return render_to_string(self.template_name, self.get_context_data(context))


class Listing(Promo):
    template_name = 'generic/inclusion_tags/element_listing.html'