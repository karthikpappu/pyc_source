# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: G:\python\hhwork\extra_apps\xadmin\apps.py
# Compiled at: 2019-01-06 19:47:39
# Size of source mod 2**32: 409 bytes
from django.apps import AppConfig
from django.core import checks
from django.utils.translation import ugettext_lazy as _
import xadmin

class XAdminConfig(AppConfig):
    __doc__ = 'Simple AppConfig which does not do automatic discovery.'
    name = 'xadmin'
    verbose_name = _('Administration')

    def ready(self):
        self.module.autodiscover()
        setattr(xadmin, 'site', xadmin.site)