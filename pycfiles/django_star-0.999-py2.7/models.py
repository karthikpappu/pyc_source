# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/star/models.py
# Compiled at: 2011-10-07 22:01:57
__author__ = 'giginet <giginet.net@gmail.com>'
__version__ = '1.0.0'
__date__ = '2011/9/20'
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext_lazy as _

class StarManager(models.Manager):

    def get_for_object(self, obj):
        """Return stars related to the 'obj.'"""
        ct = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=ct, object_id=obj.pk)

    def add_for_object(self, obj, author, comment=None, tag=None):
        """Add a star to 'obj' and return Star instance."""
        ct = ContentType.objects.get_for_model(obj)
        star = self.create(author=author, comment=comment, content_type=ct, object_id=obj.pk, tag=tag)
        return star

    def cleanup_object(self, obj):
        """remove all related stars from 'obj'."""
        stars = self.get_for_object(obj)
        for star in stars:
            star.remove()


class Star(models.Model):
    """model for star"""
    content_type = models.ForeignKey(ContentType, verbose_name='Content Type', related_name='content_type_set_for_%(class)s')
    object_id = models.PositiveIntegerField('Object ID')
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')
    author = models.ForeignKey(User, verbose_name=_('author'))
    comment = models.CharField(_('comment'), max_length=512, null=True, blank=True)
    tag = models.CharField(_('tag'), max_length=32, null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now=True)
    objects = StarManager()

    class Meta:
        ordering = ('created_at', )
        verbose_name = _('star')
        verbose_name_plural = _('stars')

    def __unicode__(self):
        return self.content_object.__unicode__()