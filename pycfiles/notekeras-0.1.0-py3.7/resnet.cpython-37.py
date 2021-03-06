# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/model/resnet.py
# Compiled at: 2020-04-19 07:19:55
# Size of source mod 2**32: 28611 bytes
"""VGGFace models for Keras.

# Notes:
- Resnet50 and VGG16  are modified architectures from Keras Application folder. [Keras](https://keras.io)

- Squeeze and excitation block is taken from  [Squeeze and Excitation Networks in
 Keras](https://github.com/titu1994/keras-squeeze-excite-network) and modified.

https://github.com/rcmalli/keras-vggface
"""
import warnings, numpy as np
from keras_applications.imagenet_utils import _obtain_input_shape
import tensorflow.keras as K
from tensorflow.keras import layers
from tensorflow.keras.layers import Flatten, Dense, Input, GlobalAveragePooling2D
from tensorflow.keras.layers import GlobalMaxPooling2D, Activation, Conv2D, ZeroPadding2D
from tensorflow.keras.layers import MaxPooling2D, BatchNormalization, AveragePooling2D, Reshape, multiply
from tensorflow.keras.models import Model
from tensorflow.keras.utils import get_file, get_source_inputs
from tensorflow_core.python.keras.utils import layer_utils
from notekeras.component import Component
from notekeras.utils import compose
VGGFACE_DIR = 'models/vggface'
V1_LABELS_PATH = 'https://github.com/rcmalli/keras-vggface/releases/download/v2.0/rcmalli_vggface_labels_v1.npy'
V2_LABELS_PATH = 'https://github.com/rcmalli/keras-vggface/releases/download/v2.0/rcmalli_vggface_labels_v2.npy'
VGG16_WEIGHTS_PATH = 'https://github.com/rcmalli/keras-vggface/releases/download/v2.0/rcmalli_vggface_tf_vgg16.h5'
VGG16_WEIGHTS_PATH_NO_TOP = 'https://github.com/rcmalli/keras-vggface/releases/download/v2.0/rcmalli_vggface_tf_notop_vgg16.h5'
SENET50_WEIGHTS_PATH = 'https://github.com/rcmalli/keras-vggface/releases/download/v2.0/rcmalli_vggface_tf_senet50.h5'
SENET50_WEIGHTS_PATH_NO_TOP = 'https://github.com/rcmalli/keras-vggface/releases/download/v2.0/rcmalli_vggface_tf_notop_senet50.h5'

class ResNetIdentityBlock(Component):

    def __init__(self, kernel_size, filters, stage, block, bias=True, *args, **kwargs):
        self.kernel_size = kernel_size
        self.filters = filters
        self.stage = stage
        self.block = block
        self.bias = bias
        self.conv1 = self.normalize1 = self.activity1 = None
        self.conv2 = self.normalize2 = self.activity2 = None
        self.conv3 = self.normalize3 = self.activity3 = None
        (super(ResNetIdentityBlock, self).__init__)(*args, **kwargs)

    def build(self, input_shape):
        filters1, filters2, filters3 = self.filters
        if K.image_data_format() == 'channels_last':
            bn_axis = 3
        else:
            bn_axis = 1
        conv_name_base = 'res{}{}_branch'.format(self.stage, self.block)
        bn_name_base = 'bn{}{}_branch'.format(self.stage, self.block)
        self.conv1 = Conv2D(filters1, (1, 1), kernel_initializer='he_normal', name=(conv_name_base + '2a'))
        self.normalize1 = BatchNormalization(axis=bn_axis, name=(bn_name_base + '2a'))
        self.activity1 = Activation('relu')
        self.conv2 = Conv2D(filters2, (self.kernel_size), padding='same', kernel_initializer='he_normal', name=(conv_name_base + '2b'))
        self.normalize2 = BatchNormalization(axis=bn_axis, name=(bn_name_base + '2b'))
        self.activity2 = Activation('relu')
        self.conv3 = Conv2D(filters3, (1, 1), kernel_initializer='he_normal', name=(conv_name_base + '2c'))
        self.normalize3 = BatchNormalization(axis=bn_axis, name=(bn_name_base + '2c'))
        self.activity3 = Activation('relu')

    def call(self, inputs, training=None, mask=None):
        x = compose(self.conv1, self.normalize1, self.activity1)(inputs)
        x = compose(self.conv2, self.normalize2, self.activity2)(x)
        x = compose(self.conv3, self.normalize3)(x)
        x = layers.add([x, inputs])
        x = self.activity3(x)
        return x


class ResNetConvBlock(Component):

    def __init__(self, kernel_size, filters, stage, block, strides=(2, 2), bias=True, *args, **kwargs):
        self.kernel_size = kernel_size
        self.filters = filters
        self.stage = stage
        self.block = block
        self.strides = strides
        self.bias = bias
        self.conv1 = self.normalize1 = self.activity1 = None
        self.conv2 = self.normalize2 = self.activity2 = None
        self.conv3 = self.normalize3 = None
        self.conv4 = self.normalize4 = self.activity4 = None
        (super(ResNetConvBlock, self).__init__)(*args, **kwargs)

    def build(self, input_shape):
        filters1, filters2, filters3 = self.filters
        if K.image_data_format() == 'channels_last':
            bn_axis = 3
        else:
            bn_axis = 1
        conv_name_base = 'res{}{}_branch'.format(self.stage, self.block)
        bn_name_base = 'bn{}{}_branch'.format(self.stage, self.block)
        self.conv1 = Conv2D(filters1, (1, 1), strides=(self.strides), kernel_initializer='he_normal', name=(conv_name_base + '2a'))
        self.normalize1 = BatchNormalization(axis=bn_axis, name=(bn_name_base + '2a'))
        self.activity1 = Activation('relu')
        self.conv2 = Conv2D(filters2, (self.kernel_size), padding='same', kernel_initializer='he_normal', name=(conv_name_base + '2b'))
        self.normalize2 = BatchNormalization(axis=bn_axis, name=(bn_name_base + '2b'))
        self.activity2 = Activation('relu')
        self.conv3 = Conv2D(filters3, (1, 1), kernel_initializer='he_normal', name=(conv_name_base + '2c'))
        self.normalize3 = BatchNormalization(axis=bn_axis, name=(bn_name_base + '2c'))
        self.conv4 = Conv2D(filters3, (1, 1), strides=(self.strides), kernel_initializer='he_normal', name=(conv_name_base + '1'))
        self.normalize4 = BatchNormalization(axis=bn_axis, name=(bn_name_base + '1'))
        self.activity4 = Activation('relu')
        self.layers.extend([self.conv1, self.normalize1, self.activity1])
        self.layers.extend([self.conv2, self.normalize2, self.activity2])
        self.layers.extend([self.conv3, self.normalize3])
        self.layers.extend([self.conv4, self.normalize4, self.activity4])

    def call(self, inputs, training=None, mask=None):
        x = compose(self.conv1, self.normalize1, self.activity1)(inputs)
        x = compose(self.conv2, self.normalize2, self.activity2)(x)
        x = compose(self.conv3, self.normalize3)(x)
        y = compose(self.conv4, self.normalize4)(inputs)
        z = layers.add([x, y])
        z = self.activity4(z)
        return z


class ResNet50Component(Component):

    def __init__(self):
        super(ResNet50Component, self).__init__()

    def build(self, input_shape):
        pass

    def call(self, inputs, training=None, mask=None):
        if K.image_data_format() == 'channels_last':
            bn_axis = 3
        else:
            bn_axis = 1
        x = ZeroPadding2D(padding=(3, 3), name='conv1_pad')(inputs)
        x = Conv2D(64, (7, 7), strides=(2, 2), padding='valid', kernel_initializer='he_normal', name='conv1')(x)
        x = BatchNormalization(axis=bn_axis, name='bn_conv1')(x)
        x = Activation('relu')(x)
        x = ZeroPadding2D(padding=(1, 1), name='pool1_pad')(x)
        x = MaxPooling2D((3, 3), strides=(2, 2))(x)
        x = ResNetConvBlock(3, [64, 64, 256], stage=2, block='a', strides=(1, 1), layer_depth=1)(x)
        x = ResNetIdentityBlock(3, [64, 64, 256], stage=2, block='b')(x)
        x = ResNetIdentityBlock(3, [64, 64, 256], stage=2, block='c')(x)
        x = ResNetConvBlock(3, [128, 128, 512], stage=3, block='a')(x)
        x = ResNetIdentityBlock(3, [128, 128, 512], stage=3, block='b')(x)
        x = ResNetIdentityBlock(3, [128, 128, 512], stage=3, block='c')(x)
        x = ResNetIdentityBlock(3, [128, 128, 512], stage=3, block='d')(x)
        x = ResNetConvBlock(3, [256, 256, 1024], stage=4, block='a')(x)
        x = ResNetIdentityBlock(3, [256, 256, 1024], stage=4, block='b')(x)
        x = ResNetIdentityBlock(3, [256, 256, 1024], stage=4, block='c')(x)
        x = ResNetIdentityBlock(3, [256, 256, 1024], stage=4, block='d')(x)
        x = ResNetIdentityBlock(3, [256, 256, 1024], stage=4, block='e')(x)
        x = ResNetIdentityBlock(3, [256, 256, 1024], stage=4, block='f')(x)
        x = ResNetConvBlock(3, [512, 512, 2048], stage=5, block='a')(x)
        x = ResNetIdentityBlock(3, [512, 512, 2048], stage=5, block='b')(x)
        x = ResNetIdentityBlock(3, [512, 512, 2048], stage=5, block='c')(x)
        return x


class ResNet50Model(Model):

    def __init__(self, include_top=True, input_tensor=None, input_shape=None, pooling=None, classes=8631):
        super(ResNet50Model, self).__init__()
        self.include_top = include_top
        input_shape = _obtain_input_shape(input_shape, default_size=224, min_size=32, data_format=(K.image_data_format()), require_flatten=include_top)
        if input_tensor is None:
            img_input = Input(shape=input_shape)
        else:
            if not K.is_keras_tensor(input_tensor):
                img_input = Input(tensor=input_tensor, shape=input_shape)
            else:
                img_input = input_tensor
        x = ResNet50Component(include_top=include_top)(img_input)
        x = Flatten()(x)
        if pooling == 'avg':
            x = GlobalAveragePooling2D()(x)
        else:
            if pooling == 'max':
                x = GlobalMaxPooling2D()(x)
            elif input_tensor is not None:
                inputs = get_source_inputs(input_tensor)
            else:
                inputs = img_input
            super(ResNet50Model, self).__init__(inputs, x, name='vggface_resnet50')

    def load_weight(self):
        RESNET50_WEIGHTS_PATH_NO_TOP = 'https://github.com/fchollet/deep-learning-models/releases/download/v0.2/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'
        weights_path = get_file('resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5', RESNET50_WEIGHTS_PATH_NO_TOP, cache_subdir='models')
        self.load_weights(weights_path, by_name=True)
        if K.image_data_format() == 'channels_first':
            if K.backend() == 'tensorflow':
                warnings.warn('You are using the TensorFlow backend, yet you are using the Theano image data format convention (`image_data_format="channels_first"`). For best performance, set `image_data_format="channels_last"` in your Keras config at ~/.keras/keras.json.')


def preprocess_input(x, data_format=None, version=1):
    x_temp = np.copy(x)
    if data_format is None:
        data_format = K.image_data_format()
    elif not data_format in {'channels_last', 'channels_first'}:
        raise AssertionError
    elif version == 1:
        if data_format == 'channels_first':
            x_temp = x_temp[:, ::-1, ...]
            x_temp[:, 0, :, :] -= 93.594
            x_temp[:, 1, :, :] -= 104.7624
            x_temp[:, 2, :, :] -= 129.1863
        else:
            x_temp = x_temp[..., ::-1]
            x_temp[(Ellipsis, 0)] -= 93.594
            x_temp[(Ellipsis, 1)] -= 104.7624
            x_temp[(Ellipsis, 2)] -= 129.1863
    else:
        if version == 2:
            if data_format == 'channels_first':
                x_temp = x_temp[:, ::-1, ...]
                x_temp[:, 0, :, :] -= 91.4953
                x_temp[:, 1, :, :] -= 103.8827
                x_temp[:, 2, :, :] -= 131.0912
            else:
                x_temp = x_temp[..., ::-1]
                x_temp[(Ellipsis, 0)] -= 91.4953
                x_temp[(Ellipsis, 1)] -= 103.8827
                x_temp[(Ellipsis, 2)] -= 131.0912
        else:
            raise NotImplementedError
    return x_temp


def decode_predictions(preds, top=5):
    LABELS = None
    if len(preds.shape) == 2:
        if preds.shape[1] == 2622:
            fpath = get_file('rcmalli_vggface_labels_v1.npy', V1_LABELS_PATH, cache_subdir=VGGFACE_DIR)
            LABELS = np.load(fpath)
        elif preds.shape[1] == 8631:
            fpath = get_file('rcmalli_vggface_labels_v2.npy', V2_LABELS_PATH, cache_subdir=VGGFACE_DIR)
            LABELS = np.load(fpath)
        else:
            raise ValueError('`decode_predictions` expects a batch of predictions (i.e. a 2D array of shape (samples, 2622)) for V1 or (samples, 8631) for V2.Found array with shape: ' + str(preds.shape))
    else:
        raise ValueError('`decode_predictions` expects a batch of predictions (i.e. a 2D array of shape (samples, 2622)) for V1 or (samples, 8631) for V2.Found array with shape: ' + str(preds.shape))
    results = []
    for pred in preds:
        top_indices = pred.argsort()[-top:][::-1]
        result = [[str(LABELS[i].encode('utf8')), pred[i]] for i in top_indices]
        result.sort(key=(lambda x: x[1]), reverse=True)
        results.append(result)

    return results


def VGG16(include_top=True, weights='vggface', input_tensor=None, input_shape=None, pooling=None, classes=2622):
    input_shape = _obtain_input_shape(input_shape, default_size=224,
      min_size=48,
      data_format=(K.image_data_format()),
      require_flatten=include_top)
    if input_tensor is None:
        img_input = Input(shape=input_shape)
    else:
        if not K.is_keras_tensor(input_tensor):
            img_input = Input(tensor=input_tensor, shape=input_shape)
        else:
            img_input = input_tensor
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='conv1_1')(img_input)
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='conv1_2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='pool1')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='conv2_1')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='conv2_2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='pool2')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='conv3_1')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='conv3_2')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='conv3_3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='pool3')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='conv4_1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='conv4_2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='conv4_3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='pool4')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='conv5_1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='conv5_2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='conv5_3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='pool5')(x)
    if include_top:
        x = Flatten(name='flatten')(x)
        x = Dense(4096, name='fc6')(x)
        x = Activation('relu', name='fc6/relu')(x)
        x = Dense(4096, name='fc7')(x)
        x = Activation('relu', name='fc7/relu')(x)
        x = Dense(classes, name='fc8')(x)
        x = Activation('softmax', name='fc8/softmax')(x)
    else:
        if pooling == 'avg':
            x = GlobalAveragePooling2D()(x)
        else:
            if pooling == 'max':
                x = GlobalMaxPooling2D()(x)
            elif input_tensor is not None:
                inputs = get_source_inputs(input_tensor)
            else:
                inputs = img_input
            model = Model(inputs, x, name='vggface_vgg16')
            if weights == 'vggface':
                if include_top:
                    weights_path = get_file('rcmalli_vggface_tf_vgg16.h5', VGG16_WEIGHTS_PATH, cache_subdir=VGGFACE_DIR)
                else:
                    weights_path = get_file('rcmalli_vggface_tf_notop_vgg16.h5', VGG16_WEIGHTS_PATH_NO_TOP, cache_subdir=VGGFACE_DIR)
                model.load_weights(weights_path, by_name=True)
                if K.backend() == 'theano':
                    layer_utils.convert_all_kernels_in_model(model)
                if K.image_data_format() == 'channels_first':
                    if include_top:
                        maxpool = model.get_layer(name='pool5')
                        shape = maxpool.output_shape[1:]
                        dense = model.get_layer(name='fc6')
                        layer_utils.convert_dense_weights_data_format(dense, shape, 'channels_first')
                    if K.backend() == 'tensorflow':
                        warnings.warn('You are using the TensorFlow backend, yet you are using the Theano image data format convention (`image_data_format="channels_first"`). For best performance, set `image_data_format="channels_last"` in your Keras config at ~/.keras/keras.json.')
            return model


def senet_se_block(input_tensor, stage, block, compress_rate=16, bias=False):
    conv1_down_name = 'conv' + str(stage) + '_' + str(block) + '_1x1_down'
    conv1_up_name = 'conv' + str(stage) + '_' + str(block) + '_1x1_up'
    num_channels = int(input_tensor.shape[(-1)])
    bottle_neck = int(num_channels // compress_rate)
    se = GlobalAveragePooling2D()(input_tensor)
    se = Reshape((1, 1, num_channels))(se)
    se = Conv2D(bottle_neck, (1, 1), use_bias=bias, name=conv1_down_name)(se)
    se = Activation('relu')(se)
    se = Conv2D(num_channels, (1, 1), use_bias=bias, name=conv1_up_name)(se)
    se = Activation('sigmoid')(se)
    x = input_tensor
    x = multiply([x, se])
    return x


def senet_conv_block(input_tensor, kernel_size, filters, stage, block, bias=False, strides=(2, 2)):
    filters1, filters2, filters3 = filters
    if K.image_data_format() == 'channels_last':
        bn_axis = 3
    else:
        bn_axis = 1
    bn_eps = 0.0001
    conv1_reduce_name = 'conv' + str(stage) + '_' + str(block) + '_1x1_reduce'
    conv1_increase_name = 'conv' + str(stage) + '_' + str(block) + '_1x1_increase'
    conv1_proj_name = 'conv' + str(stage) + '_' + str(block) + '_1x1_proj'
    conv3_name = 'conv' + str(stage) + '_' + str(block) + '_3x3'
    x = Conv2D(filters1, (1, 1), use_bias=bias, strides=strides, name=conv1_reduce_name)(input_tensor)
    x = BatchNormalization(axis=bn_axis, name=(conv1_reduce_name + '/bn'), epsilon=bn_eps)(x)
    x = Activation('relu')(x)
    x = Conv2D(filters2, kernel_size, padding='same', use_bias=bias, name=conv3_name)(x)
    x = BatchNormalization(axis=bn_axis, name=(conv3_name + '/bn'), epsilon=bn_eps)(x)
    x = Activation('relu')(x)
    x = Conv2D(filters3, (1, 1), name=conv1_increase_name, use_bias=bias)(x)
    x = BatchNormalization(axis=bn_axis, name=(conv1_increase_name + '/bn'), epsilon=bn_eps)(x)
    se = senet_se_block(x, stage=stage, block=block, bias=True)
    shortcut = Conv2D(filters3, (1, 1), use_bias=bias, strides=strides, name=conv1_proj_name)(input_tensor)
    shortcut = BatchNormalization(axis=bn_axis, name=(conv1_proj_name + '/bn'), epsilon=bn_eps)(shortcut)
    m = layers.add([se, shortcut])
    m = Activation('relu')(m)
    return m


def senet_identity_block(input_tensor, kernel_size, filters, stage, block, bias=False):
    filters1, filters2, filters3 = filters
    if K.image_data_format() == 'channels_last':
        bn_axis = 3
    else:
        bn_axis = 1
    bn_eps = 0.0001
    conv1_reduce_name = 'conv' + str(stage) + '_' + str(block) + '_1x1_reduce'
    conv1_increase_name = 'conv' + str(stage) + '_' + str(block) + '_1x1_increase'
    conv3_name = 'conv' + str(stage) + '_' + str(block) + '_3x3'
    x = Conv2D(filters1, (1, 1), use_bias=bias, name=conv1_reduce_name)(input_tensor)
    x = BatchNormalization(axis=bn_axis, name=(conv1_reduce_name + '/bn'), epsilon=bn_eps)(x)
    x = Activation('relu')(x)
    x = Conv2D(filters2, kernel_size, padding='same', use_bias=bias, name=conv3_name)(x)
    x = BatchNormalization(axis=bn_axis, name=(conv3_name + '/bn'), epsilon=bn_eps)(x)
    x = Activation('relu')(x)
    x = Conv2D(filters3, (1, 1), name=conv1_increase_name, use_bias=bias)(x)
    x = BatchNormalization(axis=bn_axis, name=(conv1_increase_name + '/bn'), epsilon=bn_eps)(x)
    se = senet_se_block(x, stage=stage, block=block, bias=True)
    m = layers.add([se, input_tensor])
    m = Activation('relu')(m)
    return m


def SENET50(include_top=True, weights='vggface', input_tensor=None, input_shape=None, pooling=None, classes=8631):
    input_shape = _obtain_input_shape(input_shape, default_size=224, min_size=197, data_format=(K.image_data_format()), require_flatten=include_top,
      weights=weights)
    if input_tensor is None:
        img_input = Input(shape=input_shape)
    else:
        if not K.is_keras_tensor(input_tensor):
            img_input = Input(tensor=input_tensor, shape=input_shape)
        else:
            img_input = input_tensor
    if K.image_data_format() == 'channels_last':
        bn_axis = 3
    else:
        bn_axis = 1
    bn_eps = 0.0001
    x = Conv2D(64,
      (7, 7), use_bias=False, strides=(2, 2), padding='same', name='conv1/7x7_s2')(img_input)
    x = BatchNormalization(axis=bn_axis, name='conv1/7x7_s2/bn', epsilon=bn_eps)(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((3, 3), strides=(2, 2))(x)
    x = senet_conv_block(x, 3, [64, 64, 256], stage=2, block=1, strides=(1, 1))
    x = senet_identity_block(x, 3, [64, 64, 256], stage=2, block=2)
    x = senet_identity_block(x, 3, [64, 64, 256], stage=2, block=3)
    x = senet_conv_block(x, 3, [128, 128, 512], stage=3, block=1)
    x = senet_identity_block(x, 3, [128, 128, 512], stage=3, block=2)
    x = senet_identity_block(x, 3, [128, 128, 512], stage=3, block=3)
    x = senet_identity_block(x, 3, [128, 128, 512], stage=3, block=4)
    x = senet_conv_block(x, 3, [256, 256, 1024], stage=4, block=1)
    x = senet_identity_block(x, 3, [256, 256, 1024], stage=4, block=2)
    x = senet_identity_block(x, 3, [256, 256, 1024], stage=4, block=3)
    x = senet_identity_block(x, 3, [256, 256, 1024], stage=4, block=4)
    x = senet_identity_block(x, 3, [256, 256, 1024], stage=4, block=5)
    x = senet_identity_block(x, 3, [256, 256, 1024], stage=4, block=6)
    x = senet_conv_block(x, 3, [512, 512, 2048], stage=5, block=1)
    x = senet_identity_block(x, 3, [512, 512, 2048], stage=5, block=2)
    x = senet_identity_block(x, 3, [512, 512, 2048], stage=5, block=3)
    x = AveragePooling2D((7, 7), name='avg_pool')(x)
    if include_top:
        x = Flatten()(x)
        x = Dense(classes, activation='softmax', name='classifier')(x)
    else:
        if pooling == 'avg':
            x = GlobalAveragePooling2D()(x)
        else:
            if pooling == 'max':
                x = GlobalMaxPooling2D()(x)
            else:
                if input_tensor is not None:
                    inputs = get_source_inputs(input_tensor)
                else:
                    inputs = img_input
                model = Model(inputs, x, name='vggface_senet50')
                if weights == 'vggface':
                    if include_top:
                        weights_path = get_file('rcmalli_vggface_tf_senet50.h5', SENET50_WEIGHTS_PATH, cache_subdir=VGGFACE_DIR)
                    else:
                        weights_path = get_file('rcmalli_vggface_tf_notop_senet50.h5', SENET50_WEIGHTS_PATH_NO_TOP, cache_subdir=VGGFACE_DIR)
                    model.load_weights(weights_path)
                    if K.image_data_format() == 'channels_first' and K.backend() == 'tensorflow':
                        warnings.warn('You are using the TensorFlow backend, yet you are using the Theano image data format convention (`image_data_format="channels_first"`). For best performance, set `image_data_format="channels_last"` in your Keras config at ~/.keras/keras.json.')
                elif weights is not None:
                    model.load_weights(weights)
            return model


def VGGFace(include_top=True, model='vgg16', weights='vggface', input_tensor=None, input_shape=None, pooling=None, classes=None):
    """Instantiates the VGGFace architectures.
    Optionally loads weights pre-trained
    on VGGFace datasets. Note that when using TensorFlow,
    for best performance you should set
    `image_data_format="channels_last"` in your Keras config
    at ~/.keras/keras.json.
    The model and the weights are compatible with both
    TensorFlow and Theano. The data format
    convention used by the model is the one
    specified in your Keras config file.
    # Arguments
        include_top: whether to include the 3 fully-connected
            layers at the top of the network.
        weights: one of `None` (random initialization)
            or "vggface" (pre-training on VGGFACE datasets).
        input_tensor: optional Keras tensor (i.e. output of `layers.Input()`)
            to use as image input for the model.
        model: selects the one of the available architectures
            vgg16, resnet50 or senet50 default is vgg16.
        input_shape: optional shape tuple, only to be specified
            if `include_top` is False (otherwise the input shape
            has to be `(224, 224, 3)` (with `channels_last` data format)
            or `(3, 224, 244)` (with `channels_first` data format).
            It should have exactly 3 inputs channels,
            and width and height should be no smaller than 48.
            E.g. `(200, 200, 3)` would be one valid value.
        pooling: Optional pooling mode for feature extraction
            when `include_top` is `False`.
            - `None` means that the output of the model will be
                the 4D tensor output of the
                last convolutional layer.
            - `avg` means that global average pooling
                will be applied to the output of the
                last convolutional layer, and thus
                the output of the model will be a 2D tensor.
            - `max` means that global max pooling will
                be applied.
        classes: optional number of classes to classify images
            into, only to be specified if `include_top` is True, and
            if no `weights` argument is specified.
    # Returns
        A Keras model instance.
    # Raises
        ValueError: in case of invalid argument for `weights`,
            or invalid input shape.
    """
    if model == 'vgg16':
        if classes is None:
            classes = 2622
        if weights == 'vggface':
            if include_top:
                if classes != 2622:
                    raise ValueError('If using `weights` as vggface original with `include_top` as true, `classes` should be 2622')
        return VGG16(include_top=include_top, input_tensor=input_tensor, input_shape=input_shape, pooling=pooling, weights=weights,
          classes=classes)
    if model == 'resnet50':
        if classes is None:
            classes = 8631
        if weights == 'vggface':
            if include_top:
                if classes != 8631:
                    raise ValueError('`weights` as vggface original with `include_top` as true, `classes` should be 8631')
        model = ResNet50Model(include_top=include_top, input_tensor=input_tensor, input_shape=input_shape, pooling=pooling,
          classes=classes)
        model.load_weight()
        return model
    if model == 'senet50':
        if classes is None:
            classes = 8631
        if weights == 'vggface':
            if include_top:
                if classes != 8631:
                    raise ValueError('If using `weights` as vggface original with `include_top`  as true, `classes` should be 8631')
        return SENET50(include_top=include_top, input_tensor=input_tensor, input_shape=input_shape, pooling=pooling, weights=weights,
          classes=classes)