# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_hpc/test_hpc.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = ' run with\n\npython setup.py install; nosetests -v --nocapture  tests/cm_hpc/test_hpc.py:Test_hpc.test_001\n\npython setup.py install; nosetests -v --nocapture tests/cm_hpc/test_hpc.py\n\nor\n\nnosetests -v tests/test_hpc.py\n\n'
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner

class Test_hpc:
    """
        This class tests the HpcCommand
    """
    data = dotdict({'cluster': 'comet'})

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c='-')
        print command
        parameter = command.split(' ')
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print result
        return str(result)

    def tearDown(self):
        pass

    def setup(self):
        HEADING('set default cluster')
        result = self.run('cm default cluster={cluster}')
        assert ('{cluster}').format(**self.data) in result

    def test_001(self):
        HEADING('test hpc info')
        result = self.run('cm hpc info --cluster={cluster}')
        assert ('{cluster}').format(**self.data) in result

    def test_002(self):
        HEADING('test hpc queue ')
        result = self.run('cm hpc queue --cluster={cluster}')
        assert ('{cluster}').format(**self.data) in result

    def test_003(self):
        HEADING(' test hpc status  ')
        result = self.run('cm hpc status --cluster={cluster}')
        assert ('{cluster}').format(**self.data) in result