# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/configmaster/JSONConfigFile.py
# Compiled at: 2015-09-06 05:00:58
import json
from configmaster import exc
from configmaster.ConfigGenerator import GenerateConfigFile, GenerateNetworkedConfigFile
import sys
if sys.version_info < (3, 5):
    JSONDecodeError = ValueError
else:
    JSONDecodeError = json.JSONDecodeError

def json_load_hook(is_net: bool=False):

    def actual_load_hook(cfg, **kwargs):
        """
        This handles automatically opening/creating the JSON configuration files.

        >>> import configmaster.JSONConfigFile
        >>> cfg = configmaster.JSONConfigFile.JSONConfigFile("test.json") # Accepts a string for input

        >>> fd = open("test.json") # Accepts a file descriptor too
        >>> cfg2 = configmaster.JSONConfigFile.JSONConfigFile(fd)

        ConfigMaster objects accepts either a string for the relative path of the INI file to load, or a :io.TextIOBase: object to read from.
        If you pass in a string, the file will automatically be created if it doesn't exist. However, if you do not have permission to write to it, a :PermissionError: will be raised.

        To access config objects programmatically, a config object is exposed via the use of cfg.config.
        These config objects can be accessed via cfg.config.attr, without having to resort to looking up objects in a dict.

        >>> # Sample JSON data is {"abc": [1, 2, 3]}
        ... print(cfg.config.abc) # Prints [1, 2, 3]
        """
        try:
            if not is_net:
                data = json.load(cfg.fd)
            else:
                data = cfg.request.json()
        except JSONDecodeError as e:
            raise exc.LoaderException('Could not decode JSON file: {}'.format(e)) from e

        cfg.config.load_from_dict(data)

    return actual_load_hook


def json_dump_hook(cfg, text: bool=False):
    """
    Dumps all the data into a JSON file.
    """
    data = cfg.config.dump()
    if not text:
        json.dump(data, cfg.fd)
    else:
        return json.dumps(data)


JSONConfigFile = GenerateConfigFile(load_hook=json_load_hook(False), dump_hook=json_dump_hook, json_fix=True)
NetworkedJSONConfigFile = GenerateNetworkedConfigFile(load_hook=json_load_hook(True), normal_class_load_hook=json_load_hook(False), normal_class_dump_hook=json_dump_hook)