# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chaoyu/workspace/BentoML/bentoml/configuration/configparser.py
# Compiled at: 2019-12-11 18:37:27
# Size of source mod 2**32: 3094 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os, logging
from collections import OrderedDict
from configparser import ConfigParser
from bentoml.exceptions import BentoMLConfigException
logger = logging.getLogger(__name__)

class BentoMLConfigParser(ConfigParser):
    __doc__ = ' BentoML configuration parser\n\n    :param default_config string - serve as default value when conf key not presented in\n        environment var or user local config file\n    '

    def __init__(self, default_config, *args, **kwargs):
        (ConfigParser.__init__)(self, *args, **kwargs)
        if default_config is not None:
            self.read_string(default_config)

    @staticmethod
    def _env_var_name(section, key):
        return 'BENTOML__{}__{}'.format(section.upper(), key.upper())

    def get(self, section, key=None, **kwargs):
        """ A simple hierachical config access, priority order:
            1. environment var
            2. user config file
            3. bentoml default config file
        """
        if key is None:
            key = section
            section = 'core'
        else:
            section = str(section).lower()
            key = str(key).lower()
            env_var = self._env_var_name(section, key)
            if env_var in os.environ:
                return os.environ[env_var]
            if ConfigParser.has_option(self, section, key):
                return (ConfigParser.get)(self, section, key, **kwargs)
        raise BentoMLConfigException("section/key '{}/{}' not found in BentoML config".format(section, key))

    def as_dict(self, display_source=False):
        cfg = {}
        for section in self:
            cfg.setdefault(section, OrderedDict())
            for k, val in self.items(section=section, raw=False):
                if display_source:
                    cfg[section][k] = (
                     val, '<bentoml.cg>')
                else:
                    cfg[section][k] = val

        for ev in os.environ:
            if ev.startswith('BENTOML__'):
                _, section, key = ev.split('__')
                val = os.environ[ev]
                if display_source:
                    val = (
                     val, 'env var')
                cfg.setdefault(section.lower(), OrderedDict()).update({key.lower(): val})

        return cfg

    def __repr__(self):
        return '<BentoML config: {}>'.format(str(self.as_dict()))