# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/tests/api_v2/test_docker.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 1317 bytes
import unittest
from bookshelf.api_v2 import docker
from fabric.api import sudo
from bookshelf.tests.api_v2.vagrant_based_tests import with_ephemeral_vagrant_box

class VagrantBasedTests(unittest.TestCase):

    @with_ephemeral_vagrant_box(verbose=True, images=[
     'ubuntu/trusty64', 'ubuntu/vivid64'])
    def test_docker_module(self, *args, **kwargs):
        docker.create_docker_group()
        self.assertTrue('docker:' in sudo('cat /etc/group'))
        docker.install_docker()
        self.assertTrue('Docker version ' in sudo('docker --version'))
        docker.cache_docker_image_locally('alpine')
        self.assertTrue('alpine ' in sudo('docker images'))
        self.assertTrue(docker.does_image_exist('alpine'))
        self.assertFalse(docker.does_image_exist('fake'))
        output = sudo('docker run -d ericjperry/busybox-sleep')
        container_id = output.split('\n')[(-1)]
        self.assertTrue(docker.does_container_exist(container_id))
        self.assertFalse(docker.does_container_exist('fake'))


if __name__ == '__main__':
    unittest.main(verbosity=4, failfast=True)