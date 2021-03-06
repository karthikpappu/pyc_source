# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fantomas/dev/buildout-versions-checker-py3/bvc/scripts/check_buildout_updates.py
# Compiled at: 2020-03-06 05:52:43
# Size of source mod 2**32: 5970 bytes
"""Command line for Buildout Versions Checker"""
import logging, sys
from argparse import Action
from argparse import ArgumentError
from argparse import ArgumentParser
from argparse import _copy_items
from bvc.checker import VersionsChecker
from bvc.configparser import VersionsConfigParser
from bvc.indentation import perfect_indentation
import bvc.logger as logger

class StoreSpecifiers(Action):

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None)
        items = _copy_items(items)
        try:
            key, value = values.split(':')
        except ValueError:
            raise ArgumentError(self, 'key:value syntax not followed')
        else:
            key = key.strip()
            value = value.strip()
            if not (key and value):
                raise ArgumentError(self, 'key or value are empty')
            items.update({key: value})
            setattr(namespace, self.dest, items)


def cmdline(argv=sys.argv[1:]):
    parser = ArgumentParser(description='Check availables updates from a version section of a buildout script')
    parser.add_argument('source',
      default='versions.cfg',
      nargs='?',
      help='The file where versions are pinned (default: versions.cfg)')
    version_group = parser.add_argument_group('Allowed versions')
    version_group.add_argument('--pre',
      action='store_true',
      dest='prereleases',
      default=False,
      help='Allow pre-releases and development versions (by default only stable versions are found)')
    version_group.add_argument('-s',
      '--specifier', action=StoreSpecifiers,
      dest='specifiers',
      default={},
      help='Describe what versions of a package are acceptable. Example "package:>=1.0,!=1.3.4.*,< 2.0" (can be used multiple times)')
    filter_group = parser.add_argument_group('Filtering')
    filter_group.add_argument('-i',
      '--include', action='append',
      dest='includes',
      default=[],
      help='Include package when checking updates (can be used multiple times)')
    filter_group.add_argument('-e',
      '--exclude', action='append',
      dest='excludes',
      default=[],
      help='Exclude package when checking updates (can be used multiple times)')
    file_group = parser.add_argument_group('File')
    file_group.add_argument('-w',
      '--write', action='store_true',
      dest='write',
      default=False,
      help='Write the updates in the source file')
    file_group.add_argument('--indent',
      dest='indentation',
      type=int,
      default=(-1),
      help='Spaces used when indenting "key = value" (default: auto)')
    file_group.add_argument('--sorting',
      dest='sorting',
      default='',
      choices=[
     'alpha', 'ascii', 'length'],
      help='Sorting algorithm used on the keys when writing source file (default: None)')
    network_group = parser.add_argument_group('Network')
    network_group.add_argument('--service-url',
      dest='service_url',
      default='https://pypi.python.org/pypi',
      help='The service to use for checking the packages (default: https://pypi.python.org/pypi)')
    network_group.add_argument('--timeout',
      dest='timeout',
      type=int,
      default=10,
      help='Timeout for each request (default: 10s)')
    network_group.add_argument('-t',
      '--threads', dest='threads',
      type=int,
      default=10,
      help='Threads used for checking the versions in parallel')
    verbosity_group = parser.add_argument_group('Verbosity')
    verbosity_group.add_argument('-v',
      action='count',
      dest='verbosity',
      default=1,
      help='Increase verbosity (specify multiple times for more)')
    verbosity_group.add_argument('-q',
      action='count',
      dest='quietly',
      default=0,
      help='Decrease verbosity (specify multiple times for more)')
    if isinstance(argv, str):
        argv = argv.split()
    options = parser.parse_args(argv)
    verbose_logs = {0:100, 
     1:logging.WARNING, 
     2:logging.INFO, 
     3:logging.DEBUG}
    verbosity = min(3, max(0, options.verbosity - options.quietly))
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(verbose_logs[verbosity])
    logger.addHandler(console)
    source = options.source
    try:
        checker = VersionsChecker(source, options.specifiers, options.prereleases, options.includes, options.excludes, options.service_url, options.timeout, options.threads)
    except Exception as e:
        try:
            sys.exit(str(e))
        finally:
            e = None
            del e

    else:
        if not checker.updates:
            sys.exit(0)
        indentation = options.indentation
        if indentation < 0:
            indentation = perfect_indentation(checker.updates.keys())
        logger.warning('[versions]')
    for package, version in checker.updates.items():
        logger.warning('%s= %s %s', package.ljust(indentation), version, ('#  %s' % checker.versions[package]).rjust(15))
    else:
        if options.write:
            config = VersionsConfigParser(indentation=(options.indentation),
              sorting=(options.sorting))
            config.read(source)
            if not config.has_section('versions'):
                config.add_section('versions')
            for package, version in checker.updates.items():
                config.set('versions', package, version)
            else:
                config.write(source)
                logger.info('- %s updated.', source)

        sys.exit(0)