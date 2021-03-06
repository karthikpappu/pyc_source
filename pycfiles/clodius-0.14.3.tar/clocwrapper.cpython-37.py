# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/clocwrapper.py
# Compiled at: 2019-12-05 21:56:41
# Size of source mod 2**32: 2801 bytes
import os, subprocess, sys
from clocwalk.libs.core.data import logger

class ClocWrapper(object):

    def __init__(self, search_path=('cloc', '/usr/bin/cloc', '/usr/local/bin/cloc')):
        """

        :param search_path:
        :returns: nothing

        """
        self.search_path = ''
        self._scan_result = {}
        self._last_output = ''
        self.version = ''
        self._args = ''
        self._result = ''
        self._result = ''
        self.cloc_path = ''
        for path in search_path:
            try:
                if not sys.platform.startswith('freebsd'):
                    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
                        p = subprocess.Popen([
                         path, '--version'],
                          bufsize=10000,
                          stdout=(subprocess.PIPE),
                          close_fds=True)
                else:
                    p = subprocess.Popen([
                     path, '--version'],
                      bufsize=10000,
                      stdout=(subprocess.PIPE))
            except OSError:
                pass
            else:
                self.cloc_path = path
                break
        else:
            raise Exception('cloc program was not found in path. PATH is : {0}'.format(os.getenv('PATH')))

        self._last_output = bytes.decode(p.communicate()[0])
        self.version = self._last_output

    @property
    def get_last_output(self):
        """
        :returns:
        """
        return self._last_output

    @property
    def cloc_version(self):
        """
        :returns:
        """
        return self.version

    @property
    def command_line(self):
        """
        """
        return self._args

    @property
    def result(self):
        """
        """
        return self._result

    def start(self, **kwargs):
        """
        :param kwargs:

        :returns:
        """
        _args = kwargs.get('args', None)
        assert _args is not list, 'args must be a list!'
        code_dir = kwargs.get('code_dir', None)
        args = [self.cloc_path, '--json', '-'] + _args + [code_dir]
        logger.debug('Scan parameters: "{0}"'.format(' '.join(args)))
        self._args = ' '.join(args)
        p = subprocess.Popen(args,
          bufsize=100000,
          stdin=(subprocess.PIPE),
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        self._last_output, _err = p.communicate()
        self._result = bytes.decode(self._last_output)
        _err = bytes.decode(_err)
        return (
         self._result, _err)