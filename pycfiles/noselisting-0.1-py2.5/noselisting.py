# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/noselisting.py
# Compiled at: 2008-03-09 14:36:37
import os, nose.plugins

class TestListingPlugin(nose.plugins.Plugin):
    """Only list test names, don't actually run any tests."""

    class _StopThisTest(Exception):
        pass

    def options(self, parser, env=os.environ):
        env_opt = 'NOSE_LIST_TEST_NAMES'
        parser.add_option('--list-test-names', action='store_true', dest=self.enableOpt, default=env.get(env_opt), help='Enable plugin %s: %s [%s]' % (
         self.__class__.__name__, self.help(), env_opt))
        parser.add_option('--list-long-test-names', action='store_true', dest='list_long_test_names', default=False, help='Like --list-test-names, but use long names that can be used as arguments to nosetests')

    def configure(self, options, conf):
        nose.plugins.Plugin.configure(self, options, conf)
        self._list_long_test_names = options.list_long_test_names
        if self._list_long_test_names:
            self.enabled = True

    def setOutputStream(self, stream):
        self.stream = stream

    def _name_from_address(self, address):
        (filename, module, call) = address
        if filename is not None:
            if filename[-4:] in ('.pyc', '.pyo'):
                filename = filename[:-1]
            head = filename
        else:
            head = module
        if call is not None:
            return '%s:%s' % (head, call)
        return head

    def _test_name(self, test):
        if self._list_long_test_names:
            return self._name_from_address(test.address())
        else:
            return test.shortDescription() or str(test)

    def beforeTest(self, test):
        self.stream.writeln(self._test_name(test))
        raise TestListingPlugin._StopThisTest()

    def handleError(self, test, err):
        if issubclass(err[0], TestListingPlugin._StopThisTest):
            return True