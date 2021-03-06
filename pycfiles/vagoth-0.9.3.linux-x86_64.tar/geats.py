# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/virt/drivers/geats.py
# Compiled at: 2013-02-09 13:15:10
from ..utils.mc_json_rpc import mcollective_call
from ..exceptions import DriverException

class GeatsMcollective(object):
    """
    Driver to talk to Geats using mcollective.  It uses the
    mcollective_call() function from utils.mc_json_rpc to
    launch ruby to make the call.
    """

    def __init__(self, manager, local_config):
        self.config = local_config

    def _call(self, action, node=None, timeout=60, **kwargs):
        if node:
            node_name = node.node_id
            return mcollective_call('geats', action, timeout=timeout, identity=node_name, **kwargs)
        else:
            return mcollective_call('geats', action, timeout=timeout, **kwargs)

    def _call_single(self, action, node, vm, timeout=60, **kwargs):
        if node is None:
            raise TypeError, 'node argument is required'
        if vm is None:
            raise TypeError, 'vm argument is required'
        node_name = node.node_id
        vm_name = vm.node_id
        responses = mcollective_call('geats', action, timeout=timeout, identity=node_name, vm_name=vm_name, **kwargs)
        for res in responses:
            return (res['statuscode'], res['statusmsg'], res['data'])

        return (None, None, None)

    def _call_single_exc(self, action, node, vm, timeout=60, **kwargs):
        status, statusmsg, data = self._call_single(action, node, vm, timeout, **kwargs)
        if status is None:
            raise DriverException('No response received from %s' % (node,))
        if status != 0:
            raise DriverException(statusmsg)
        return data

    def _call_boolean(self, action, node, vm, timeout=60, **kwargs):
        status, statusmsg, data = self._call_single(action, node, vm, timeout, **kwargs)
        if data:
            return True
        else:
            if status == 0:
                return True
            if status is None:
                raise DriverException('No response received from %s' % (node,))
            else:
                raise DriverException(str(statusmsg))
            return

    def provision(self, node, vm):
        """Request a node to define & provision a VM"""
        return self._call_single_exc('provision', node, vm, definition=vm.definition)

    def define(self, node, vm):
        """Request node to define a VM"""
        return self._call_single_exc('define', node, vm, definition=vm.definition)

    def undefine(self, node, vm):
        """Request node to undefine a VM"""
        return self._call_boolean('undefine', node, vm)

    def deprovision(self, node, vm):
        """Request node to undefine & deprovision a VM"""
        return self._call_boolean('deprovision', node, vm)

    def start(self, node, vm):
        """Request node to start the VM"""
        return self._call_boolean('start', node, vm, timeout=10)

    def reboot(self, node, vm):
        """Request node to reboot the VM"""
        return self._call_boolean('reboot', node, vm, timeout=10)

    def stop(self, node, vm):
        """Request node to stop (forcefully) the VM"""
        return self._call_boolean('stop', node, vm, timeout=10)

    def shutdown(self, node, vm):
        """Request node to shutdown (nicely) the VM"""
        return self._call_boolean('shutdown', node, vm, timeout=10)

    def info(self, node, vm):
        """Request information about the given VM from the node"""
        info = self._call_single_exc('info', node, vm, timeout=5)
        if info:
            info['node'] = unicode(node.node_id)
        return info

    def status(self, node=None):
        """Request information about all VMs from the node"""
        res = self._call('status', node, timeout=5)
        if len(res) == 0:
            raise DriverException('No results received for %s' % node)
        nodes = []
        for node in res:
            if node['statuscode'] == 0:
                for vm in node['data']['vms'].values():
                    vm['_parent'] = node['sender']
                    vm['_name'] = vm['definition']['name']
                    vm['_type'] = 'vm'
                    nodes.append(vm)

                hv = node['data'].get('status', {})
                hv['_parent'] = None
                hv['_name'] = node['sender']
                hv['_type'] = 'hv'
                nodes.append(hv)

        return nodes

    def migrate(self, node, vm, destination_node):
        """Request the node to migrate the given VM to the destination node"""
        return NotImplemented