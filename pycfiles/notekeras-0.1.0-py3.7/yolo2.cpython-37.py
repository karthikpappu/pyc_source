# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/component/yolo2.py
# Compiled at: 2020-04-02 13:24:52
# Size of source mod 2**32: 10129 bytes
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D, Add, ZeroPadding2D, UpSampling2D, Concatenate
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.regularizers import l2
from notekeras.component import Component
from notekeras.utils import compose
__all__ = [
 'DarknetConv2D', 'DarkConv', 'DarkConvSet', 'ResBlockBody', 'YoloModel']

class DarknetConv2D(Conv2D):

    def __init__(self, *args, **kwargs):
        darknet_conv_kwargs = {'kernel_regularizer':l2(0.0005), 
         'padding':'valid' if kwargs.get('strides') == (2, 2) else 'same'}
        darknet_conv_kwargs.update(kwargs)
        (super(DarknetConv2D, self).__init__)(*args, **darknet_conv_kwargs)


class DarkConv(Component):

    def __init__(self, count, size, strides=(1, 1), *args, **kwargs):
        self.count = count
        self.size = size
        self.strides = strides
        self.conv = self.norm = self.relu = None
        (super(DarkConv, self).__init__)(*args, **kwargs)

    def build(self, input_shape):
        self.conv = DarknetConv2D((self.count), (self.size),
          use_bias=False,
          name=('{}-conv'.format(self.name)),
          strides=(self.strides))
        self.norm = BatchNormalization(name=('{}-norm'.format(self.name)))
        self.relu = LeakyReLU(alpha=0.1, name=('{}-relu'.format(self.name)))

    def call(self, inputs, **kwargs):
        output = self.conv(inputs)
        output = self.norm(output)
        output = self.relu(output)
        return output

    def compute_output_shape(self, input_shape):
        return self.conv.compute_output_shape(input_shape)

    def _build(self, inputs):
        output = DarknetConv2D((self.count), (self.size),
          use_bias=False,
          name=('{}-conv'.format(self.name)),
          strides=(self.strides))(inputs)
        output = BatchNormalization(name=('{}-norm'.format(self.name)))(output)
        output = LeakyReLU(alpha=0.1, name=('{}-relu'.format(self.name)))(output)
        return output


class DarkConvSet(Component):

    def __init__(self, num_filters, *args, **kwargs):
        self.num_filters = num_filters
        self.conv_list = None
        (super(DarkConvSet, self).__init__)(*args, **kwargs)

    def build(self, input_shape):
        self.conv_list = [
         DarkConv((self.num_filters), (1, 1), name=('{}_1'.format(self.name))),
         DarkConv((self.num_filters * 2), (3, 3), name=('{}_2'.format(self.name))),
         DarkConv((self.num_filters), (1, 1), name=('{}_3'.format(self.name))),
         DarkConv((self.num_filters * 2), (3, 3), name=('{}_4'.format(self.name))),
         DarkConv((self.num_filters), (1, 1), name=('{}_5'.format(self.name)))]

    def call(self, inputs, **kwargs):
        return compose(*self.conv_list)(inputs)

    def _build(self, inputs):
        res = compose(DarkConv((self.num_filters), (1, 1), name=('{}_1'.format(self.name))), DarkConv((self.num_filters * 2), (3,
                                                                                                                               3), name=('{}_2'.format(self.name))), DarkConv((self.num_filters), (1,
                                                                                                                                                                                                   1), name=('{}_3'.format(self.name))), DarkConv((self.num_filters * 2), (3,
                                                                                                                                                                                                                                                                           3), name=('{}_4'.format(self.name))), DarkConv((self.num_filters), (1,
                                                                                                                                                                                                                                                                                                                                               1), name=('{}_5'.format(self.name))))(inputs)
        return res


class ResBlockBody(Component):

    def __init__(self, num_filters, num_blocks, name='ResBlockBody', *args, **kwargs):
        super(ResBlockBody, self).__init__(name=name)
        self.num_filters = num_filters
        self.num_blocks = num_blocks
        self.zero = None
        self.conv = None
        self.block_layers = None
        (super(ResBlockBody, self).__init__)(args, name=name, **kwargs)

    def build(self, input_shape):
        self.zero = ZeroPadding2D(((1, 0), (1, 0)))
        self.conv = DarkConv((self.num_filters), (3, 3), strides=(2, 2), layer_depth=(self.layer_depth - 1))
        self.block_layers = []
        for i in range(self.num_blocks):
            self.block_layers.append([
             DarkConv((self.num_filters // 2), (1, 1), layer_depth=(self.layer_depth - 1)),
             DarkConv((self.num_filters), (3, 3), layer_depth=(self.layer_depth - 1)),
             Add()])

    def call(self, inputs, **kwargs):
        x = compose(self.zero, self.conv)(inputs)
        for block in self.block_layers:
            conv1, conv2, add = block
            y = compose(conv1, conv2)(x)
            x = add([x, y])

        return x

    def _build(self, inputs):
        x = ZeroPadding2D(((1, 0), (1, 0)))(inputs)
        x = DarkConv((self.num_filters), (3, 3), strides=(2, 2), layer_depth=(self.layer_depth - 1))(x)
        for i in range(self.num_blocks):
            y = DarkConv((self.num_filters // 2), (1, 1), layer_depth=(self.layer_depth - 1))(x)
            y = DarkConv((self.num_filters), (3, 3), layer_depth=(self.layer_depth - 1))(y)
            x = Add()([x, y])

        return x


class YoloModel(Component):

    def __init__(self, num_anchors, num_classes, name='Yolo', anchors=None, *args, **kwargs):
        self.num_anchors = num_anchors
        self.num_classes = num_classes
        self.anchors = anchors
        self.layer0 = self.block1 = self.block2 = self.block3 = self.block4 = self.block5 = None
        self.make_list = self.samps = self.concat = None
        (super(YoloModel, self).__init__)(args, name=name, **kwargs)

    def build(self, input_shape):
        self.layer0 = DarkConv(32, (3, 3), name=('{}_DarkConv'.format(self.name)), layer_depth=(self.layer_depth - 2))
        self.block1 = ResBlockBody(64, 1, name=('{}_ResBlock_1'.format(self.name)), layer_depth=(self.layer_depth - 1))
        self.block2 = ResBlockBody(128, 2, name=('{}_ResBlock_2'.format(self.name)), layer_depth=(self.layer_depth - 1))
        self.block3 = ResBlockBody(256, 8, name=('{}_ResBlock_3'.format(self.name)), layer_depth=(self.layer_depth - 1))
        self.block4 = ResBlockBody(512, 8, name=('{}_ResBlock_4'.format(self.name)), layer_depth=(self.layer_depth - 1))
        self.block5 = ResBlockBody(1024, 4, name=('{}_ResBlock_5'.format(self.name)), layer_depth=(self.layer_depth - 1))
        out_filters = self.num_anchors * (self.num_classes + 5)
        self.make_list = [[DarkConvSet(num_filters, layer_depth=(self.layer_depth - 1)), DarkConv((num_filters * 2), (3, 3), layer_depth=(self.layer_depth - 1)), DarknetConv2D(out_filters, (1, 1), name=('yolo_conv2d_{}'.format(num_filters)))] for num_filters in (512,
                                                                                                                                                                                                                                                                       256,
                                                                                                                                                                                                                                                                       128)]
        self.samps = [
         [
          DarkConv(256, (1, 1), layer_depth=(self.layer_depth - 2), name=('{}__DarkConv_1'.format(self.name))),
          UpSampling2D(2)],
         [
          DarkConv(128, (1, 1), layer_depth=(self.layer_depth - 2), name=('{}__DarkConv_2'.format(self.name))),
          UpSampling2D(2)]]
        self.concat = [
         Concatenate(), Concatenate()]

    def call(self, inputs, **kwargs):
        out0 = self.layer0(inputs)
        out1 = self.block1(out0)
        out2 = self.block2(out1)
        out3 = self.block3(out2)
        out4 = self.block4(out3)
        out5 = self.block5(out4)
        x = self.make_list[0][0](out5)
        y1 = compose(*self.make_list[0][1:])(x)
        x = compose(*self.samps[0])(x)
        x = self.concat[0]([x, out4])
        x = self.make_list[1][0](x)
        y2 = compose(*self.make_list[1][1:])(x)
        x = compose(*self.samps[1])(x)
        x = self.concat[1]([x, out3])
        x = self.make_list[2][0](x)
        y3 = compose(*self.make_list[2][1:])(x)
        return (
         y1, y2, y3)