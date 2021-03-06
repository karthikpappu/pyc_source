# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/argos/Workspace/mamba-framework/mamba-server/mamba_server/utils/component.py
# Compiled at: 2020-05-10 10:21:24
# Size of source mod 2**32: 2741 bytes
"""Component handling utility functions"""
from PySide2.QtWidgets import QMenu
from mamba_server.exceptions import ComponentSettingsException
from mamba_server.exceptions import ComponentConfigException

def generate_component_configuration(settings=None, config_file=None, local_config=None):
    """Returns a dictionary with the component configuration.

    Local configurations passed via launch file have precedence over
    configuration file settings.

    The configuration dictionary is composed of the local configuration, then
    the configurations from file that are not in local, and then the settings
    that are neither in file nor in local but have default values.

    Args:
        settings (dict, optional): The dictionary with the description of the
                                   component settings.
        config_file (dict, optional): The dictionary of the component settings
                                      retrieved from component.config.json.
        local_config (dict, optional): The dictionary of the component
                                       settings passed via launch file.

    Returns:
        dict: The validated component configuration parameters.

    Raises:
        ComponentConfigException: If a required setting is not present in
                                  local nor in file parameters.
        ComponentSettingsException: If a setting is missing the 'required'
                                    field or the 'default' field if it is not
                                    a required parameter.

    """
    settings = settings or {}
    config_file = config_file or {}
    local_config = local_config or {}
    composed_config = dict(list(config_file.items()) + list(local_config.items()))
    component_name = composed_config['name'] if 'name' in composed_config else ''
    for key, value in settings.items():
        if key not in composed_config:
            if 'required' not in value:
                raise ComponentSettingsException('Setting "{}" is missing required field "required"'.format(key))
            else:
                if value['required']:
                    raise ComponentConfigException('Component "{}" configuration is missing parameter "{}"'.format(component_name, key))
                if not value['required']:
                    if 'default' not in value:
                        raise ComponentSettingsException('Setting "{}" is missing required field "default"'.format(key))
            composed_config[key] = value['default']

    return composed_config