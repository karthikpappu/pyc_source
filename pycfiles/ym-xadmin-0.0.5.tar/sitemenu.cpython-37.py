# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\python\hhwork\extra_apps\xadmin\plugins\sitemenu.py
# Compiled at: 2019-04-17 23:57:58
# Size of source mod 2**32: 622 bytes
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, CommAdminView
BUILDIN_STYLES = {'default':'xadmin/includes/sitemenu_default.html', 
 'accordion':'xadmin/includes/sitemenu_accordion.html'}

class SiteMenuStylePlugin(BaseAdminPlugin):
    menu_style = None

    def init_request(self, *args, **kwargs):
        return bool(self.menu_style) and self.menu_style in BUILDIN_STYLES

    def get_context(self, context):
        context['menu_template'] = BUILDIN_STYLES[self.menu_style]
        return context


site.register_plugin(SiteMenuStylePlugin, CommAdminView)