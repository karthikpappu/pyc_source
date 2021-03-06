# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjharries/Code/@wizardsoftheweb/py-rofi-bus/py_rofi_bus/components/config.py
# Compiled at: 2018-06-03 14:06:06
# Size of source mod 2**32: 1393 bytes
from os import environ
from os.path import expanduser, join, normpath
from py_rofi_bus.utils import mkdirp

class Config(dict):
    BASE_CONFIG_DIR = join(environ['XDG_CONFIG_HOME'] if 'XDG_CONFIG_HOME' in environ else normpath(join(expanduser('~'), '.config')), 'wotw', 'py-rofi-bus')
    DEFAULTS = {'application':None, 
     'pid_name':'', 
     'load_from':join(BASE_CONFIG_DIR, 'apps-enabled'), 
     'pid_folder':join(BASE_CONFIG_DIR, 'pids')}

    def __init__(self, *args, **kwargs):
        (self.set_with_defaults)(**kwargs)
        self.init_directories()

    def init_directories(self):
        mkdirp(self.config_dir)
        mkdirp(self['load_from'])
        mkdirp(self['pid_folder'])

    def apply_dict_to_self(self, dict_to_apply=None):
        if dict_to_apply:
            for key, value in list(dict_to_apply.items()):
                self[key] = value

    def set_with_defaults(self, **kwargs):
        for arg_dict in [self.DEFAULTS, kwargs]:
            self.apply_dict_to_self(arg_dict)

    @property
    def config_dir(self):
        if 'application' in self:
            if self['application']:
                return join(self.BASE_CONFIG_DIR, self['application'])
        return self.BASE_CONFIG_DIR