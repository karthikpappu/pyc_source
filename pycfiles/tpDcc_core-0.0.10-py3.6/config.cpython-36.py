# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/core/config.py
# Compiled at: 2020-04-24 23:10:11
# Size of source mod 2**32: 3608 bytes
"""
Module that contains implementation for settings manager
"""
from __future__ import print_function, division, absolute_import
import tpDcc as tp

class ConfigAttribute(dict, object):
    __doc__ = '\n    Class that allows access nested dictionaries using Python attribute access\n    https://stackoverflow.com/questions/38034377/object-like-attribute-access-for-nested-dictionary\n    '

    def __init__(self, *args, **kwargs):
        (super(ConfigAttribute, self).__init__)(*args, **kwargs)
        self.__dict__ = self

    @staticmethod
    def from_nested_dict(data):
        """
        Constructs a nested YAMLConfigurationAttribute from nested dictionaries
        :param data: dict
        :return: YAMLConfigurationAttribute
        """
        if not isinstance(data, dict):
            return data
        else:
            return ConfigAttribute({key:ConfigAttribute.from_nested_dict(data[key]) for key in data})


class YAMLConfigurationParser(object):

    def __init__(self, config_data):
        super(YAMLConfigurationParser, self).__init__()
        self._config_data = config_data
        self._parsed_data = dict()

    def parse(self):
        self._parsed_data = self._config_data
        return ConfigAttribute.from_nested_dict(self._parsed_data)


class DccConfig(object):

    def __init__(self, config_name, environment, data):
        super(DccConfig, self).__init__()
        self._config_name = config_name
        self._environment = environment
        self._parsed_data = data

    @property
    def data(self):
        return self._parsed_data

    @data.setter
    def data(self, value):
        self._parsed_data = value

    def get_path(self):
        if not self._parsed_data:
            return
        else:
            return self._parsed_data.get('config', {}).get('path', None)

    def get(self, attr_section, attr_name=None, default=None):
        """
        Returns an attribute of the configuration
        :param attr_name: str
        :param attr_section: str
        :param default: object
        :return:
        """
        if not self._parsed_data:
            tp.logger.warning('Configuration "{}" is empty for "{}"'.format(self._config_name, self._environment))
            return default
        else:
            if attr_section:
                if attr_name:
                    orig_section = attr_section
                    attr_section = self._parsed_data.get(attr_section, dict())
                    if not attr_section:
                        tp.logger.warning('Configuration "{}" has no attribute "{}" in section "{}" for "{}"'.format(self._config_name, attr_name, orig_section, self._environment))
                        return default
                    else:
                        attr_value = attr_section.get(attr_name, None)
                        if attr_value is None:
                            tp.logger.warning('Configuration "{}" has no attribute "{}" in section "{}" for "{}"'.format(self._config_name, attr_name, attr_section, self._environment))
                            return default
                        return attr_value
                attr_to_use = attr_section
                if attr_name:
                    if not default:
                        default = attr_name
            else:
                if not attr_section:
                    attr_to_use = attr_name
                attr_value = self._parsed_data.get(attr_to_use, None)
                if attr_value is None:
                    tp.logger.warning('Configuration "{}" has no attribute "{}" for "{}"'.format(self._config_name, attr_to_use, self._environment))
                    return default
            return attr_value