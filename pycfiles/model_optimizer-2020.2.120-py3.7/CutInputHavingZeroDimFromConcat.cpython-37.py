# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/CutInputHavingZeroDimFromConcat.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 3024 bytes
"""
 Copyright (c) 2019-2020 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
from mo.graph.graph import Graph
from mo.middle.replacement import MiddleReplacementPattern
from mo.ops.concat import Concat

class CutInputHavingZeroDimFromConcat(MiddleReplacementPattern):
    __doc__ = '\n    This transformation deletes inputs of Concat having zeros in their shapes, if not all inputs have such shapes.\n    '
    enabled = True

    def pattern(self):
        return dict(nodes=[
         (
          'concat', dict(type='Concat'))],
          edges=[])

    def replace_pattern(self, graph: Graph, match: dict):
        concat_node = match['concat']
        sources_of_ports = [concat_node.in_port(i).get_connection().get_source() for i in concat_node.in_ports()]
        sources_of_ports = [s for s in sources_of_ports if s is not None]
        input_nodes = [s.node for s in sources_of_ports]
        if not all((n.has_valid('type') for n in input_nodes)):
            return
        else:
            saved_ports = []
            disconnected_ports = []
            for port_num, node in enumerate(input_nodes):
                if node.soft_get('type') == 'Const' and len(node.shape) > 1 and any((i == 0 for i in node.shape)):
                    disconnected_ports.append(port_num)
                else:
                    saved_ports.append(port_num)

            return saved_ports and disconnected_ports or None
        if len(saved_ports) == 1:
            before_concat = concat_node.in_port(saved_ports[0]).get_connection().get_source()
            concat_node.out_port(0).get_connection().set_source(before_concat)
            return
        new_concat_attrs = concat_node.attrs().copy()
        new_concat_attrs['name'] = concat_node.name + '/Concat_'
        new_concat_attrs['in_ports_count'] = len(saved_ports)
        new_concat_node = Concat(graph, attrs=new_concat_attrs).create_node()
        for new_port_num, old_port_num in enumerate(saved_ports):
            concat_node.in_port(old_port_num).get_connection().set_destination(new_concat_node.in_port(new_port_num))

        for p in disconnected_ports:
            concat_node.in_port(p).disconnect()

        concat_node.out_port(0).get_connection().set_source(new_concat_node.out_port(0))