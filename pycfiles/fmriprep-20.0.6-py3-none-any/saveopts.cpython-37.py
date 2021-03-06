# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/setuptools/setuptools/command/saveopts.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 658 bytes
from setuptools.command.setopt import edit_config, option_base

class saveopts(option_base):
    __doc__ = 'Save command-line options to a file'
    description = 'save supplied options to setup.cfg or other config file'

    def run(self):
        dist = self.distribution
        settings = {}
        for cmd in dist.command_options:
            if cmd == 'saveopts':
                continue
            for opt, (src, val) in dist.get_option_dict(cmd).items():
                if src == 'command line':
                    settings.setdefault(cmd, {})[opt] = val

        edit_config(self.filename, settings, self.dry_run)