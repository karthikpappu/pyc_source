# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cary/__main__.py
# Compiled at: 2015-08-06 11:53:39
# Size of source mod 2**32: 1595 bytes
import sys, logging
from importlib.machinery import SourceFileLoader
import argparse
from cary.caryapp import CaryApp

def configure_cary(app, config):
    app.allowed_addresses = config.ALLOW_FROM_ADDRESSES
    app.smtp_host = config.SMTP_HOST
    app.return_address = config.SMTP_RETURN_ADDRESS
    app.should_clean_up = config.SHOULD_CLEAN_UP
    app.should_respond = config.SHOULD_RESPOND
    app.workspace = config.WORKSPACE_DIR
    for name, (cmd_class, cmd_config) in config.COMMANDS.items():
        cmd = cmd_class()
        cmd.set_config(cmd_config, WORKSPACE_DIR=config.WORKSPACE_DIR, FROM_ADDRESS=config.FROM_ADDRESS)
        app.add_command(name, cmd)


def setup_logging(config):
    logging.basicConfig(filename=config.LOG_FILE, level=config.LOG_LEVEL, format=config.LOG_FORMAT)
    logging.info('Log opened')


def main():
    parser = argparse.ArgumentParser(description='process email message as an offline assistant')
    parser.add_argument('--settings', type=str, help='name of the local settings module', default='local_conf.py')
    args = parser.parse_args()
    config = SourceFileLoader('local_conf', args.settings).load_module()
    setup_logging(config)
    app = CaryApp()
    try:
        configure_cary(app, config)
        msg = sys.stdin.read()
        app.process_message(msg)
    except:
        logging.exception('Serious error on initialization/processing')


if __name__ == '__main__':
    main()