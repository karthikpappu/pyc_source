# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/mxnet/psroi_pooling_ext.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 1514 bytes
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
from extensions.ops.psroipooling import PSROIPoolingOp
from mo.front.extractor import FrontExtractorOp
from mo.front.mxnet.extractors.utils import get_mxnet_layer_attrs

class PSROIPoolingFrontExtractor(FrontExtractorOp):
    op = '_contrib_PSROIPooling'
    enabled = True

    @classmethod
    def extract(cls, node):
        attrs = get_mxnet_layer_attrs(node.symbol_dict)
        spatial_scale = attrs.float('spatial_scale', None)
        pooled_size = attrs.int('pooled_size', None)
        output_dim = attrs.int('output_dim', None)
        group_size = attrs.int('group_size', 0)
        if group_size == 0:
            group_size = pooled_size
        data = {'spatial_scale':spatial_scale, 
         'output_dim':output_dim, 
         'group_size':group_size}
        PSROIPoolingOp.update_node_stat(node, data)
        return cls.enabled