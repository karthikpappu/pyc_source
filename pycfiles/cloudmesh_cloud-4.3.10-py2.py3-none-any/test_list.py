# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_cloud/test_list.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = ' run with\n\npython setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_list.py:Test_list.test_001\n\nnosetests -v --nocapture tests/test_list.py\n\nor\n\nnosetests -v tests/test_list.py\n\n'
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default

class Test_list:
    data = dotdict({'cloud': Default.cloud, 
       'format': 'json', 
       'user': 'fake', 
       'wrong_cloud': 'no_cloud', 
       'key': 'my_default_key', 
       'value': 'my_default_value'})

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

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        HEADING('testing cm list --cloud cloud default')
        result = self.run('cm default {key}={value}')
        result = self.run('cm default list')
        assert self.data.key in result
        result = self.run('cm list default')
        assert self.data.value in result
        result = self.run('cm default delete {key}')
        assert 'ok.' in result

    def test_002(self):
        HEADING('testing cm list --format json default')
        result = self.run('cm default {key}={value}')
        assert 'ok.' in result
        result = self.run('cm list --format={format} default')
        assert self.data.value in result
        result = self.run('cm default delete {key}')
        assert 'ok.' in result

    def test_003(self):
        HEADING('testing cm list')
        banner('cm list --cloud={wrong_cloud} --user={user} vm')
        result = self.run('cm list --cloud={wrong_cloud} --user={user} vm')
        assert 'No' in result