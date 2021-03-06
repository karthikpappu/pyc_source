# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\faoustin\Downloads\ocglances\ocglances\config.py
# Compiled at: 2017-02-13 10:46:28
# Size of source mod 2**32: 10153 bytes
"""Manage the configuration file."""
import os, sys, multiprocessing
from io import open
from ocglances.compat import ConfigParser, NoOptionError
from ocglances.globals import BSD, LINUX, MACOS, SUNOS, WINDOWS
from ocglances.logger import logger

def user_config_dir():
    r"""Return the per-user config dir (full path).

    - Linux, *BSD, SunOS: ~/.config/glances
    - macOS: ~/Library/Application Support/glances
    - Windows: %APPDATA%\glances
    """
    if WINDOWS:
        path = os.environ.get('APPDATA')
    else:
        if MACOS:
            path = os.path.expanduser('~/Library/Application Support')
        else:
            path = os.environ.get('XDG_CONFIG_HOME') or os.path.expanduser('~/.config')
    path = os.path.join(path, 'glances')
    return path


def user_cache_dir():
    r"""Return the per-user cache dir (full path).

    - Linux, *BSD, SunOS: ~/.cache/glances
    - macOS: ~/Library/Caches/glances
    - Windows: %LOCALAPPDATA%\glances\cache
    """
    if WINDOWS:
        path = os.path.join(os.environ.get('LOCALAPPDATA'), 'glances', 'cache')
    else:
        if MACOS:
            path = os.path.expanduser('~/Library/Caches/glances')
        else:
            path = os.path.join(os.environ.get('XDG_CACHE_HOME') or os.path.expanduser('~/.cache'), 'glances')
    return path


def system_config_dir():
    r"""Return the system-wide config dir (full path).

    - Linux, SunOS: /etc/glances
    - *BSD, macOS: /usr/local/etc/glances
    - Windows: %APPDATA%\glances
    """
    if LINUX or SUNOS:
        path = '/etc'
    else:
        if BSD or MACOS:
            path = '/usr/local/etc'
        else:
            path = os.environ.get('APPDATA')
    path = os.path.join(path, 'glances')
    return path


class Config(object):
    __doc__ = 'This class is used to access/read config file, if it exists.\n\n    :param config_dir: the path to search for config file\n    :type config_dir: str or None\n    '

    def __init__(self, config_dir=None):
        self.config_dir = config_dir
        self.config_filename = 'glances.conf'
        self._loaded_config_file = None
        self.parser = ConfigParser()
        self.read()

    def config_file_paths(self):
        r"""Get a list of config file paths.

        The list is built taking into account of the OS, priority and location.

        * custom path: /path/to/glances
        * Linux, SunOS: ~/.config/glances, /etc/glances
        * *BSD: ~/.config/glances, /usr/local/etc/glances
        * macOS: ~/Library/Application Support/glances, /usr/local/etc/glances
        * Windows: %APPDATA%\glances

        The config file will be searched in the following order of priority:
            * /path/to/file (via -C flag)
            * user's home directory (per-user settings)
            * system-wide directory (system-wide settings)
        """
        paths = []
        if self.config_dir:
            paths.append(self.config_dir)
        paths.append(os.path.join(user_config_dir(), self.config_filename))
        paths.append(os.path.join(system_config_dir(), self.config_filename))
        return paths

    def read(self):
        """Read the config file, if it exists. Using defaults otherwise."""
        for config_file in self.config_file_paths():
            if os.path.exists(config_file):
                try:
                    with open(config_file, encoding='utf-8') as (f):
                        self.parser.read_file(f)
                        self.parser.read(f)
                    logger.info("Read configuration file '{}'".format(config_file))
                except UnicodeDecodeError as err:
                    logger.error("Cannot decode configuration file '{}': {}".format(config_file, err))
                    sys.exit(1)

                self._loaded_config_file = config_file
                break

        if not self.parser.has_section('quicklook'):
            self.parser.add_section('quicklook')
        self.set_default_cwc('quicklook', 'cpu')
        self.set_default_cwc('quicklook', 'mem')
        self.set_default_cwc('quicklook', 'swap')
        if not self.parser.has_section('cpu'):
            self.parser.add_section('cpu')
        self.set_default_cwc('cpu', 'user')
        self.set_default_cwc('cpu', 'system')
        self.set_default_cwc('cpu', 'steal')
        iowait_bottleneck = 1.0 / multiprocessing.cpu_count() * 100.0
        self.set_default_cwc('cpu', 'iowait', [
         str(iowait_bottleneck - iowait_bottleneck * 0.2),
         str(iowait_bottleneck - iowait_bottleneck * 0.1),
         str(iowait_bottleneck)])
        ctx_switches_bottleneck = 56000 / multiprocessing.cpu_count()
        self.set_default_cwc('cpu', 'ctx_switches', [
         str(ctx_switches_bottleneck - ctx_switches_bottleneck * 0.2),
         str(ctx_switches_bottleneck - ctx_switches_bottleneck * 0.1),
         str(ctx_switches_bottleneck)])
        if not self.parser.has_section('percpu'):
            self.parser.add_section('percpu')
        self.set_default_cwc('percpu', 'user')
        self.set_default_cwc('percpu', 'system')
        if not self.parser.has_section('load'):
            self.parser.add_section('load')
        self.set_default_cwc('load', cwc=['0.7', '1.0', '5.0'])
        if not self.parser.has_section('mem'):
            self.parser.add_section('mem')
        self.set_default_cwc('mem')
        if not self.parser.has_section('memswap'):
            self.parser.add_section('memswap')
        self.set_default_cwc('memswap')
        if not self.parser.has_section('network'):
            self.parser.add_section('network')
        self.set_default_cwc('network', 'rx')
        self.set_default_cwc('network', 'tx')
        if not self.parser.has_section('fs'):
            self.parser.add_section('fs')
        self.set_default_cwc('fs')
        if not self.parser.has_section('sensors'):
            self.parser.add_section('sensors')
        self.set_default_cwc('sensors', 'temperature_core', cwc=['60', '70', '80'])
        self.set_default_cwc('sensors', 'temperature_hdd', cwc=['45', '52', '60'])
        self.set_default_cwc('sensors', 'battery', cwc=['80', '90', '95'])
        if not self.parser.has_section('processlist'):
            self.parser.add_section('processlist')
        self.set_default_cwc('processlist', 'cpu')
        self.set_default_cwc('processlist', 'mem')

    @property
    def loaded_config_file(self):
        """Return the loaded configuration file."""
        return self._loaded_config_file

    def as_dict(self):
        """Return the configuration as a dict"""
        dictionary = {}
        for section in self.parser.sections():
            dictionary[section] = {}
            for option in self.parser.options(section):
                dictionary[section][option] = self.parser.get(section, option)

        return dictionary

    def sections(self):
        """Return a list of all sections."""
        return self.parser.sections()

    def items(self, section):
        """Return the items list of a section."""
        return self.parser.items(section)

    def has_section(self, section):
        """Return info about the existence of a section."""
        return self.parser.has_section(section)

    def set_default_cwc(self, section, option_header=None, cwc=[
 '50', '70', '90']):
        """Set default values for careful, warning and critical."""
        if option_header is None:
            header = ''
        else:
            header = option_header + '_'
        self.set_default(section, header + 'careful', cwc[0])
        self.set_default(section, header + 'warning', cwc[1])
        self.set_default(section, header + 'critical', cwc[2])

    def set_default(self, section, option, default):
        """If the option did not exist, create a default value."""
        if not self.parser.has_option(section, option):
            self.parser.set(section, option, default)

    def get_value(self, section, option, default=None):
        """Get the value of an option, if it exists."""
        try:
            return self.parser.get(section, option)
        except NoOptionError:
            return default

    def get_int_value(self, section, option, default=0):
        """Get the int value of an option, if it exists."""
        try:
            return self.parser.getint(section, option)
        except NoOptionError:
            return int(default)

    def get_float_value(self, section, option, default=0.0):
        """Get the float value of an option, if it exists."""
        try:
            return self.parser.getfloat(section, option)
        except NoOptionError:
            return float(default)