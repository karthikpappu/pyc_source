# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /code/trebuchet/trebuchet/parser.py
# Compiled at: 2013-11-20 09:08:17
import os

class Configuration:

    def __init__(self, **entries):
        self.__dict__.update(entries)


def parse_version(args):
    """
    Parse the arguments and extract the version as a dictionary
    """
    versions = {}
    if args.get('--app-version'):
        versions['app'] = args.get('--app-version')
    if args.get('--env-version'):
        versions['env'] = args.get('--env-version')
    if args.get('--service-version'):
        versions['service'] = args.get('--service-version')
    if args.get('--static-version'):
        versions['static_files'] = args.get('--static-version')
    return versions


def parse_project(args):
    """
    Parse the arguments and return a Configuration object for the project.
    """
    dico = {}
    dico['config_file'] = os.path.abspath(os.path.expanduser(args['<config_file>']))
    dico['full_path'] = os.path.dirname(dico['config_file'])
    return Configuration(**dico)


def parse_prepare(args):
    """
    Parse the arguments and return a Configuration object for the preparation (before packaging).
    """
    dico = {}
    dico['build_path'] = args.get('--build')
    dico['architecture'] = args.get('--arch')
    dico['pip_options'] = args.get('--pip-options')
    dico['extra_description'] = args.get('--extra-description')
    return Configuration(**dico)


def parse_package(args):
    """
    """
    dico = {}
    dico['web_callback_url'] = args.get('--web-callback')
    dico['debs_path'] = args.get('--output') if args.get('--output') else os.getcwd()
    return Configuration(**dico)