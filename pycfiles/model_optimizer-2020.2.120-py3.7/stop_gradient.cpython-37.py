# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/stop_gradient.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 1242 bytes
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
from mo.front.common.partial_infer.elemental import copy_shape_infer
from mo.graph.graph import Graph
from mo.ops.op import Op
from mo.front.common.partial_infer.utils import mark_input_bins

class StopGradientOp(Op):
    op = 'StopGradient'
    enabled = True

    def __init__(self, graph, attrs):
        super().__init__(graph, {'type':__class__.op, 
         'op':__class__.op, 
         'identity':True, 
         'in_ports_count':1, 
         'out_ports_count':1, 
         'infer':StopGradientOp.shape_infer}, attrs)

    @staticmethod
    def shape_infer(node):
        copy_shape_infer(node)