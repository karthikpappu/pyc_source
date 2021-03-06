# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/back/SpecialNodesFinalization.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 13989 bytes
"""
 Copyright (C) 2018-2020 Intel Corporation

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
import logging as log
from collections import defaultdict
from copy import copy
import numpy as np
from extensions.back.pass_separator import BackFinish
from extensions.ops.split import Split
from extensions.ops.tensor_iterator import TensorIterator, get_internal_node_by_layer_id
from mo.back.replacement import BackReplacementPattern
from mo.front.tf.graph_utils import create_op_node_with_second_input
from mo.graph.graph import Graph
from mo.ops.const import Const
from mo.utils.error import Error
from mo.utils.utils import refer_to_faq_msg

class RemoveConstOps(BackReplacementPattern):
    enabled = False

    def run_after(self):
        return [
         BackFinish]

    def run_before(self):
        return []

    def find_and_replace_pattern(self, graph: Graph):
        for node in graph.get_op_nodes(type='Const'):
            graph.remove_edge(node.id, node.out_node().id)
            graph.remove_node(node.id)


class CreateConstNodesReplacement(BackReplacementPattern):
    enabled = False

    def run_before(self):
        return []

    def run_after(self):
        return [
         RemoveConstOps]

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'data', dict(kind='data'))],
          edges=[])

    @staticmethod
    def _check_bin_attrs(node):
        """Check that at least one output edge from node without 'bin' attribute."""
        out_edges = node.out_edges()
        bin_in_out_ports = ['bin' in edge for edge in out_edges]
        out_node = [node.has('op') and node.op == 'Result' for node in node.out_nodes()]
        return np.any(out_node) or not np.all(bin_in_out_ports)

    @staticmethod
    def _check_that_node_from_body(node):
        """Check that all output edges from node have 'internal_port_id'
        (that shows that this node is from TI body)"""
        n_ports = len(node.out_edges())
        internal_port_in_out_ports = ['internal_port_id' in edge for edge in node.out_edges()]
        return np.any(internal_port_in_out_ports) and n_ports

    def replace_pattern(self, graph: Graph, match: dict):
        """
            Adds layers with type 'Const' that produce blob from 'bin' file. The pass finds data nodes with one output which
            doesn't have edge with 'bin' attribute (or with two outputs and at least one output havent 'bin' attr)
            and generate Const op node before the node and data node before the Const node. The data node before 'Const'
            node is needed because the op node dumps input tensors to bin file.
        """
        node = match['data']
        if len(node.in_nodes()) > 0:
            return
        if self._check_bin_attrs(node):
            if node.has_valid('value'):
                const_node_name = graph.unique_id(node.id + '_const')
                log.debug("Added Const node '{}'".format(const_node_name))
                const_node = Const(graph, {'name':const_node_name,  'value':node.value,  'force_shape':node.soft_get('force_shape', None), 
                 'override_output_shape':node.has_valid('force_shape'), 
                 'force_type':node.soft_get('force_type', None), 
                 'correct_data_type':node.soft_get('correct_data_type', None)}).create_node()
                const_node.add_input_port(0)
                graph.add_edges_from([(const_node_name, node.id, {'out': 0})])
                node_copy = node.copy_node()
                const_node.type_infer(const_node)
                graph.add_edges_from([(node_copy.id, const_node_name, {'in':0,  'bin':'custom'})])
            else:
                if not self._check_that_node_from_body(node):
                    log.debug('node = {}'.format(node.graph.node[node.id]))
                    raise Error('Discovered data node without inputs and value, node.name = {}, consumer.name = {}. ' + refer_to_faq_msg(23), node.soft_get('name'), node.out_node().soft_get('name') if len(node.out_nodes()) else '<no consumer>')


class RemoveOutputOps(BackReplacementPattern):
    enabled = False

    def run_after(self):
        return [
         CreateConstNodesReplacement]

    def run_before(self):
        return []

    def find_and_replace_pattern(self, graph: Graph):
        for node in list(graph.get_op_nodes(op='Result')):
            if len(node.in_nodes()) > 0:
                assert len(node.in_nodes()) == 1
            graph.remove_node(node.id)


class NormalizeTI(BackReplacementPattern):
    __doc__ = '\n    This transformation is used while generating IR of lower than 10 version\n\n    Changes linking mechanism of TensorIterator outer graph with inner graph\n        from linking outer graph node ports with inner Parameter and Result operations\n        to linking outer graph node ports with functional operations and their input/output ports\n\n    1. Updating `input_port_map`, `output_port_map` and `back_edges` maps\n    2. Removing Parameter/Input operation nodes\n\n    NOTE: Result operation will be removed by a separate transformation\n    '
    enabled = False

    @staticmethod
    def maps_uniqueization(ti):
        assert ti.has_valid('input_port_map')
        assert ti.has_valid('output_port_map')
        assert ti.has_valid('back_edges')
        ti.input_port_map = [dict(unique_r) for unique_r in set([tuple(rec.items()) for rec in ti.input_port_map])]
        ti.output_port_map = [dict(unique_r) for unique_r in set([tuple(rec.items()) for rec in ti.output_port_map])]
        ti.back_edges = [dict(unique_rec) for unique_rec in set([tuple(rec.items()) for rec in ti.back_edges])]

    @staticmethod
    def normalize_ti(ti):
        assert ti.has_valid('input_port_map')
        assert ti.has_valid('output_port_map')
        assert ti.has_valid('back_edges')
        body = ti.body
        for record in ti.input_port_map:
            assert 'internal_layer_id' in record
            assert 'internal_port_id' not in record
            assert 'external_port_id' in record
            internal_layer_id = copy(record['internal_layer_id'])
            parameter = get_internal_node_by_layer_id(ti, internal_layer_id)
            dst = parameter.out_port(0).get_destination()
            in_port_idx = dst.idx
            internal_node = dst.node
            internal_port_id = internal_node.in_edge(in_port_idx)['internal_port_id']
            record['internal_layer_id'] = internal_node.internal_layer_id
            record['internal_port_id'] = internal_port_id
            TensorIterator.update_back_edge_map(ti=ti, direction='to', old_layer_id=internal_layer_id, old_port_id=None, new_layer_id=(internal_node.internal_layer_id),
              new_port_id=internal_port_id)

        for record in ti.output_port_map:
            assert 'internal_layer_id' in record
            assert 'internal_port_id' not in record
            assert 'external_port_id' in record
            internal_layer_id = copy(record['internal_layer_id'])
            result = get_internal_node_by_layer_id(ti, internal_layer_id)
            out_port_idx = result.in_port(0).get_source().idx
            internal_node = result.in_port(0).get_source().node
            internal_port_id = internal_node.out_edge(out_port_idx)['internal_port_id']
            record['internal_layer_id'] = internal_node.internal_layer_id
            record['internal_port_id'] = internal_port_id
            TensorIterator.update_back_edge_map(ti=ti, direction='from', old_layer_id=internal_layer_id, old_port_id=None,
              new_layer_id=(internal_node.internal_layer_id),
              new_port_id=internal_port_id)

        for record in ti.back_edges:
            assert 'from_layer' in record
            assert 'to_layer' in record
            internal_layer_id = record['from_layer']
            result = get_internal_node_by_layer_id(ti, internal_layer_id)
            if result.soft_get('type') == 'Result':
                assert 'from_port' not in record
                out_port_idx = result.in_port(0).get_source().idx
                internal_node = result.in_port(0).get_source().node
                internal_port_id = internal_node.out_edge(out_port_idx)['internal_port_id']
                TensorIterator.update_back_edge_map(ti=ti, direction='from', old_layer_id=internal_layer_id, old_port_id=None,
                  new_layer_id=(internal_node.internal_layer_id),
                  new_port_id=internal_port_id)

        body.remove_nodes_from([n.id for n in body.get_op_nodes(type='Input')])
        body.remove_nodes_from([n.id for n in body.get_op_nodes(type='Parameter')])

    @staticmethod
    def external_nodes_normalization(ti):
        """
        TensorIterator external ports may have several internal layer connections.

        Current transformation does the following:
            - normalizes port maps (eliminating duplicated records)
            - replicates external input/output port for each internal Parameter/Result it is connected to
            - updates input and output port maps according to previous step replications
        """

        def update_external_port_id(ti, port_type, old_external_port_id, new_external_port_id, internal_layer_id):
            assert port_type in ('in', 'out')
            port_map = ti.input_port_map if port_type == 'in' else ti.output_port_map
            for record in port_map:
                if record['external_port_id'] == old_external_port_id and record['internal_layer_id'] == internal_layer_id:
                    record['external_port_id'] = new_external_port_id

        NormalizeTI.maps_uniqueization(ti)
        body = ti.body
        external_input_ports = defaultdict(list)
        for record in ti.input_port_map:
            assert 'external_port_id' in record
            external_input_ports[record['external_port_id']].append(record)

        for external_port_id, record_list in external_input_ports.items():
            if len(record_list) == 1:
                continue
            real_external_port_id = TensorIterator.special_port_to_real_port(ti, external_port_id, 'in')
            source = ti.in_port(real_external_port_id).get_source()
            for record in record_list[1:]:
                assert 'internal_layer_id' in record
                new_real_input_port_id = max(map(int, ti.in_ports().keys())) + 1
                new_external_port_id = max([int(d['external_port_id']) for d in list(ti.in_edges().values()) + list(ti.out_edges().values())]) + 1
                ti.add_input_port(new_real_input_port_id)
                source.connect(ti.in_port(new_real_input_port_id))
                ti.in_edge(new_real_input_port_id)['external_port_id'] = new_external_port_id
                update_external_port_id(ti, 'in', external_port_id, new_external_port_id, record['internal_layer_id'])

        external_output_ports = defaultdict(list)
        for record in ti.output_port_map:
            assert 'external_port_id' in record
            external_output_ports[record['external_port_id']].append(record)

        for external_port_id, record_list in external_output_ports.items():
            if len(record_list) == 1:
                continue
            real_external_port_id = TensorIterator.special_port_to_real_port(ti, external_port_id, 'out')
            dsts = ti.out_port(real_external_port_id).get_destinations()
            for record in record_list[1:]:
                assert 'internal_layer_id' in record
                new_real_output_port_id = max(map(int, ti.out_ports().keys())) + 1
                new_external_port_id = max([int(d['external_port_id']) for d in list(ti.in_edges().values()) + list(ti.out_edges().values())]) + 1
                ti.add_output_port(new_real_output_port_id)
                for dst in dsts:
                    ti.out_port(new_real_output_port_id).connect(dst)

                update_external_port_id(ti, 'out', external_port_id, new_external_port_id, record['internal_layer_id'])

        body.clean_up()

    def find_and_replace_pattern(self, graph: Graph):
        for ti in graph.get_op_nodes(type='TensorIterator'):
            if not graph.graph['cmd_params'].generate_experimental_IR_V10:
                self.normalize_ti(ti)
            else:
                self.external_nodes_normalization(ti)
            if len([record for record in ti.input_port_map if record.get('axis') is not None]) == 0:
                for record in ti.output_port_map:
                    if record.get('axis') is not None:
                        record['start'] = 0
                        real_output_port = TensorIterator.special_port_to_real_port(ti, record['external_port_id'], 'out')
                        output_shape = ti.out_port(real_output_port).data.get_shape()
                        assert output_shape is not None
                        record['end'] = output_shape[record['axis']]