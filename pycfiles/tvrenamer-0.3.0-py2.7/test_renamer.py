# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/tests/core/test_renamer.py
# Compiled at: 2015-11-08 18:30:19
import os, mock
from testtools import matchers
from tvrenamer.core import renamer
from tvrenamer.tests import base

class RenamerTest(base.BaseTest):

    def test_execute(self):
        with mock.patch.object(os.path, 'isfile', return_value=True):
            self.assertIsNone(renamer.execute('/tmp/test_file.txt', 'Test_file.txt'))
        tempfile = self.create_tempfiles([('test_file', 'test data')])[0]
        new_file = os.path.join(os.path.dirname(tempfile), 'other_file.conf')
        renamer.execute(tempfile, new_file)
        self.assertThat(new_file, matchers.FileExists())
        self.assertThat(tempfile, matchers.Not(matchers.FileExists()))
        tempfiles = self.create_tempfiles([('test_file', 'test data'),
         ('other_file', 'test data')])
        self.CONF.set_override('overwrite_file_enabled', True)
        renamer.execute(tempfiles[0], tempfiles[1])
        self.assertThat(tempfiles[1], matchers.FileExists())
        self.assertThat(tempfiles[0], matchers.Not(matchers.FileExists()))
        tempfile = self.create_tempfiles([('my_file', 'test data')])[0]
        new_file = os.path.join(os.path.dirname(tempfile), 'alt_file.conf')
        self.CONF.set_override('dryrun', True)
        renamer.execute(tempfile, new_file)
        self.assertThat(tempfile, matchers.FileExists())
        self.assertThat(new_file, matchers.Not(matchers.FileExists()))