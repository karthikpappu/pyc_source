# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jsick/.virtualenvs/paperweight/lib/python2.7/site-packages/preprint/main.py
# Compiled at: 2015-01-11 21:10:10
import logging, sys
from cliff.app import App
from cliff.commandmanager import CommandManager
from .config import Configurations
VERSION = '0.3'

class PreprintApp(App):
    log = logging.getLogger(__name__)
    confs = Configurations()

    def __init__(self):
        super(PreprintApp, self).__init__(description='Tools for writing latex papers', version=VERSION, command_manager=CommandManager('preprint.commands'))

    def initialize_app(self, argv):
        self.log.debug('initialize_app')

    def build_option_parser(self, *args):
        parser = super(PreprintApp, self).build_option_parser(*args)
        parser.add_argument('--master', default=self.confs.config('master'), help='Name of master tex file')
        return parser

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = PreprintApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))