# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0006_vm_network_isolated.py
# Compiled at: 2016-06-16 16:03:55
"""
Copyright (c) 2014 Maciej Nabozny

This file is part of CloudOver project.

CloudOver is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import settings
from pycore import Cloud
import time
api = None
cloud = None
image = None
template = None
vm = None
network_isolated = None
isolated_lease = None

def setup_module(module):
    global api
    global cloud
    global image
    global network_isolated
    global template
    cloud = Cloud(settings.address, settings.login, settings.password)
    api = cloud.get_api()
    templates = api.template_list()
    template = templates[0]
    images = api.image_list()
    for img in images:
        if img.name == 'default image' and img.state == 'ok':
            image = img

    if image == None:
        raise Exception('image not found')
    networks = api.network_list()
    for n in networks:
        if n.name == 'Test isolated network':
            network_isolated = n

    if network_isolated == None:
        raise Exception('network not found')
    return


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_vm_create_isolated():
    global vm
    vm = api.vm_create('Isolated network test', 'vm description', template, image)
    count = 0
    for lease in network_isolated.lease_list():
        if lease.vm_id == None:
            lease.attach(vm)
            vm.start()
            return

    raise Exception('no lease available in routed network')
    return


def test_wait_vm():
    for i in xrange(120):
        v = api.vm_by_id(vm.id)
        if v.state == 'running':
            return
        if v.state == 'failed':
            raise Exception('image failed')
        else:
            time.sleep(1)

    raise Exception('vm create timeout')


def test_vm_cleanup():
    vm.poweroff()
    vm.cleanup()


def test_wait_closed():
    for i in xrange(60):
        v = api.vm_by_id(vm.id)
        if v.state == 'closed':
            return
        if v.state == 'failed':
            raise Exception('image failed')
        else:
            time.sleep(1)

    raise Exception('vm close timeout')


def test_lease_detached():
    global isolated_lease
    lease = api.lease_by_id(isolated_lease.id)
    if lease.vm_id != None:
        raise Exception('lease was not detached')
    return