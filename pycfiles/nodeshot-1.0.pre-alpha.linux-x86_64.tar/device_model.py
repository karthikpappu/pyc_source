# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/hardware/models/device_model.py
# Compiled at: 2014-05-08 09:17:48
from django.db import models
from django.utils.translation import ugettext_lazy as _
from nodeshot.core.base.models import BaseDate
from . import ImageMixin, Manufacturer

class DeviceModel(BaseDate, ImageMixin):
    """
    Device Type Model
    Eg.: Nanostation M5, Rocket M2, ecc.
    """
    manufacturer = models.ForeignKey(Manufacturer)
    name = models.CharField(_('name'), max_length=50, unique=True)
    image = models.ImageField(_('image'), upload_to='devices/images/', blank=True)
    datasheet = models.FileField(_('datasheet'), upload_to='devices/datasheets/', blank=True)
    cpu = models.CharField(_('CPU'), max_length=255, blank=True)
    ram = models.IntegerField(_('RAM'), blank=True, help_text=_('bytes'))

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'hardware'
        db_table = 'hardware_device_model'
        verbose_name = _('Device Model')
        verbose_name_plural = _('Device Models')