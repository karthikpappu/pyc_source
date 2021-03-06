# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emencia/django/links/models.py
# Compiled at: 2010-01-14 11:17:33
"""Models for emencia.django.links"""
from datetime import datetime
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from django.conf import settings

class LinkPublishedManager(models.Manager):
    """Link published manager"""

    def get_query_set(self):
        now = datetime.now()
        return super(LinkPublishedManager, self).get_query_set().filter(publication_start__lte=now, publication_end__gt=now, site=Site.objects.get_current(), visibility=True).order_by('ordering', '-creation')


class Category(models.Model):
    """Category Model"""
    title = models.CharField(_('title'), max_length=150)
    slug = models.SlugField(_('slug'), help_text=_('Used for the URLs'))
    description = models.TextField(_('description'), blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('title', )


class Link(models.Model):
    """Link Model"""
    title = models.CharField(_('title'), max_length=150, default=None)
    language = models.CharField(_('language'), max_length=2, choices=settings.LANGUAGES, default='fr')
    url = models.URLField(_('url'), default=None)
    description = models.TextField(_('description'), blank=True)
    category = models.ManyToManyField(Category, verbose_name=_('category'), null=True)
    visibility = models.BooleanField(_('visibility'), default=True)
    ordering = models.IntegerField(_('ordering'), default=100)
    creation = models.DateTimeField(_('creation date'), auto_now_add=True)
    publication_start = models.DateTimeField(_('publication start'), default=datetime.now)
    publication_end = models.DateTimeField(_('publication end'), default=datetime(2042, 3, 15))
    site = models.ForeignKey(Site, verbose_name=_('site'))
    objects = models.Manager()
    published = LinkPublishedManager()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')
        ordering = ('title', )