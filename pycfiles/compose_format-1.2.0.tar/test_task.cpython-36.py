# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_task.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 976 bytes
import shlex
from unittest import mock
from compose_flow.commands import Workflow
from tests import BaseTestCase

@mock.patch('compose_flow.commands.subcommands.env.get_backend')
@mock.patch('compose_flow.commands.subcommands.env.os')
@mock.patch('compose_flow.commands.subcommands.profile.Profile.write')
class TaskTestCase(BaseTestCase):

    @mock.patch('compose_flow.commands.subcommands.env.Env.rw_env', new=True)
    @mock.patch('compose_flow.commands.subcommands.env.utils')
    def test_config_updated(self, *mocks):
        """
        Ensures that the config is updated in order to run tasks on the latest locally built image
        """
        utils_mock = mocks[0]
        utils_mock.get_tag_version.return_value = '0.0.1-test'
        utils_mock.render.side_effect = lambda x, **kwargs: x
        command = shlex.split('-e test task foo')
        workflow = Workflow(argv=command)
        self.assertEqual(True, 'DOCKER_IMAGE' in workflow.environment.data)