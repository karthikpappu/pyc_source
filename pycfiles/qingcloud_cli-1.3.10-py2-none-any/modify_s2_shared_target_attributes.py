# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/modify_s2_shared_target_attributes.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyS2SharedTargetAttributesAction(BaseAction):
    action = 'ModifyS2SharedTargetAttributes'
    command = 'modify-s2-shared-target-attributes'
    usage = '%(prog)s -s <shared_target> -o <operation> [-p <parameters> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--shared-target', dest='shared_target', action='store', type=str, default=None, help='the ID of shared target.')
        parser.add_argument('-o', '--operation', dest='operation', action='store', type=str, default=None, help='valid values includes add, modify, delete, set.')
        parser.add_argument('-p', '--parameters', dest='parameters', action='store', type=str, default=None, help='please refer https://docs.qingcloud.com/api/s2/describle_s2_default_parameters.html')
        parser.add_argument('-i', '--initiator-names', dest='initiator_names', action='store', type=str, default=None, help='client IQN.')
        parser.add_argument('-S', '--s2-group', dest='s2_group', action='store', type=str, default=None, help='the ID of permission group.')
        parser.add_argument('-n', '--export-name', dest='export_name', action='store', type=str, default=None, help='the name of shared target, available in vnas.')
        return

    @classmethod
    def build_directive(cls, options):
        for key in ['shared_target', 'operation']:
            if not hasattr(options, key):
                print 'error: [%s] should be specified.' % key
                return None

        directive = {'shared_target': options.shared_target, 'operation': options.operation, 
           'parameters': explode_array(options.parameters), 
           'initiator_names': explode_array(options.initiator_names), 
           's2_group': options.s2_group, 
           'export_name': options.export_name}
        return directive