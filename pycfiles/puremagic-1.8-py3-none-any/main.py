# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alex/envs/purelyjs/lib/python2.7/site-packages/purelyjs/main.py
# Compiled at: 2014-05-22 14:55:25
import optparse, os, sys
from .config import parse_config
from .testrunner import TestRunner
CONFIG_FILE = 'purelyjs.ini'

def main():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interpreter', action='append', help='Path to js interpreter to run on')
    parser.add_option('-k', action='store', dest='test_name_filter', help='Only select tests matching this regular expression')
    parser.add_option('-l', '--collect-only', action='store_true', help='Only list selected tests, do not execute')
    parser.add_option('--lib', action='append', help='Add library module to test run')
    parser.add_option('--test', action='append', help='Add test module to test run')
    parser.add_option('--keep-modules', action='store_true', help='Keep test modules after run')
    parser.add_option('-v', '--verbose', action='store_true')
    options, args = parser.parse_args()
    collect_only = options.collect_only
    interpreters = []
    keep_modules = options.keep_modules
    libs = []
    test_name_filter = options.test_name_filter
    tests = []
    verbose = options.verbose
    if os.path.exists(CONFIG_FILE):
        interpreters, libs, tests = parse_config(CONFIG_FILE)
    if options.interpreter:
        interpreters = options.interpreter
    if options.lib:
        libs = options.lib
    if options.test:
        tests = options.test
    runner = TestRunner(collect_only=collect_only, interpreters=interpreters, keep_modules=keep_modules, libs=libs, test_name_filter=test_name_filter, tests=tests, verbose=verbose)
    if runner.run() is False:
        sys.exit(1)


if __name__ == '__main__':
    main()