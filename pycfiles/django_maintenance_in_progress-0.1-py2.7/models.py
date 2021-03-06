# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/vanilla/maintenance_in_progress/models.py
# Compiled at: 2014-11-11 03:11:26
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db import models
from django.dispatch import receiver

class SingletonManager(models.Manager):

    def get_query_set(self):
        """Return the first preferences object. If it does not exist then
        create it."""
        queryset = super(SingletonManager, self).get_query_set()
        try:
            queryset.get()
        except Preferences.DoesNotExist:
            obj = Preferences()
            obj.save()
            queryset.get()

        return queryset


class Preferences(models.Model):
    objects = SingletonManager()
    in_progress = models.BooleanField(default=False, help_text=_('Flag that indicates whether maintenance is in progress'))
    file_marker = models.CharField(max_length=512, null=True, blank=True, help_text=_('Path to a file that indicates maintenance is in progress.'))

    class Meta:
        verbose_name_plural = _('Preferences')

    def __unicode__(self):
        return _('Preferences')

    def save(self, *args, **kwargs):
        self.id = 1
        super(Preferences, self).save(*args, **kwargs)