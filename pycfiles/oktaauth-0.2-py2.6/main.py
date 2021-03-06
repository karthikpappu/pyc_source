# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oktaauth/main.py
# Compiled at: 2016-02-08 11:14:19
"""Program entry point"""
from __future__ import print_function
import argparse, sys, getpass, logging
from oktaauth import models
from oktaauth import metadata
log = logging.getLogger('oktaauth')

def configurelogging():
    log.setLevel(logging.DEBUG)
    stderrlog = logging.StreamHandler()
    stderrlog.setFormatter(logging.Formatter('%(message)s'))
    log.addHandler(stderrlog)


def main(argv):
    configurelogging()
    author_strings = []
    for (name, email) in zip(metadata.authors, metadata.emails):
        author_strings.append(('Author: {0} <{1}>').format(name, email))

    epilog = ('\n{project} {version}\n\n{authors}\nURL: <{url}>\n').format(project=metadata.project, version=metadata.version, authors=('\n').join(author_strings), url=metadata.url)
    arg_parser = argparse.ArgumentParser(prog=argv[0], formatter_class=argparse.RawDescriptionHelpFormatter, description=metadata.description, epilog=epilog)
    arg_parser.add_argument('-V', '--version', action='version', version=('{0} {1}').format(metadata.project, metadata.version))
    arg_parser.add_argument('-s', '--server', type=str, help='Okta server', required=True)
    arg_parser.add_argument('-u', '--username', type=str, help='Username', required=True)
    arg_parser.add_argument('-t', '--apptype', type=str, help='Application type', required=True)
    arg_parser.add_argument('-i', '--appid', type=str, help='Application id', required=True)
    config = arg_parser.parse_args(args=argv[1:])
    log.info(epilog)
    log.debug('Server: %s' % config.server)
    log.debug('Username: %s' % config.username)
    log.debug('Application type: %s' % config.apptype)
    log.debug('Application ID: %s' % config.appid)
    password = getpass.getpass()
    passcode = getpass.getpass('Passcode: ')
    okta = models.OktaSamlAuth(config.server, config.apptype, config.appid, config.username, password, passcode)
    try:
        try:
            print(okta.auth())
            return 0
        except Exception, e:
            log.error('Error authorising with okta: %s' % e)
            return 1

    finally:
        del password
        del passcode


def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv))


if __name__ == '__main__':
    entry_point()