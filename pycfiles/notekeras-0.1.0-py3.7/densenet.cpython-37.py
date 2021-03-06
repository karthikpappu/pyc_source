# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/model/retinanet/models/densenet.py
# Compiled at: 2020-04-26 08:16:42
# Size of source mod 2**32: 3768 bytes
import tensorflow.keras.backend as K
from tensorflow import keras
from tensorflow.keras.applications import densenet
from tensorflow.keras.utils import get_file
from notekeras.model.retinanet.core import Backbone
from .retinanet import RetinaNetModel
from utils.image import preprocess_image
allowed_backbones = {'densenet121':(
  [
   6, 12, 24, 16], densenet.DenseNet121), 
 'densenet169':(
  [
   6, 12, 32, 32], densenet.DenseNet169), 
 'densenet201':(
  [
   6, 12, 48, 32], densenet.DenseNet201)}

class DenseNetBackbone(Backbone):
    __doc__ = ' Describes backbone information and provides utility functions.\n    '

    def retinanet(self, *args, **kwargs):
        """ Returns a retinanet model using the correct backbone.
        """
        return densenet_retinanet(args, backbone=self.backbone, **kwargs)

    def download_imagenet(self):
        """ Download pre-trained weights for the specified backbone name.
        This name is in the format {backbone}_weights_tf_dim_ordering_tf_kernels_notop
        where backbone is the densenet + number of layers (e.g. densenet121).
        For more info check the explanation from the keras densenet script itself:
            https://github.com/keras-team/keras/blob/master/keras/applications/densenet.py
        """
        origin = 'https://github.com/fchollet/deep-learning-models/releases/download/v0.8/'
        file_name = '{}_weights_tf_dim_ordering_tf_kernels_notop.h5'
        if K.image_data_format() == 'channels_first':
            raise ValueError('Weights for "channels_first" format are not available.')
        weights_url = origin + file_name.format(self.backbone)
        return get_file((file_name.format(self.backbone)), weights_url, cache_subdir='models')

    def validate(self):
        """ Checks whether the backbone string is correct.
        """
        backbone = self.backbone.split('_')[0]
        if backbone not in allowed_backbones:
            raise ValueError("Backbone ('{}') not in allowed backbones ({}).".format(backbone, allowed_backbones.keys()))

    def preprocess_image(self, inputs):
        """ Takes as input an image and prepares it for being passed through the network.
        """
        return preprocess_image(inputs, mode='tf')


def densenet_retinanet(num_classes, backbone='densenet121', inputs=None, modifier=None, **kwargs):
    """ Constructs a retinanet model using a densenet backbone.

    Args
        num_classes: Number of classes to predict.
        backbone: Which backbone to use (one of ('densenet121', 'densenet169', 'densenet201')).
        inputs: The inputs to the network (defaults to a Tensor of shape (None, None, 3)).
        modifier: A function handler which can modify the backbone before using it in retinanet (this can be used to freeze backbone layers for example).

    Returns
        RetinaNet model with a DenseNet backbone.
    """
    if inputs is None:
        inputs = keras.layers.Input((None, None, 3))
    blocks, creator = allowed_backbones[backbone]
    model = creator(input_tensor=inputs, include_top=False, pooling=None, weights=None)
    layer_outputs = [model.get_layer(name=('conv{}_block{}_concat'.format(idx + 2, block_num))).output for idx, block_num in enumerate(blocks)]
    model = keras.models.Model(inputs=inputs, outputs=(layer_outputs[1:]), name=(model.name))
    if modifier:
        model = modifier(model)
    model = RetinaNetModel(inputs=inputs, num_classes=num_classes, backbone_layers=model.outputs, **kwargs)
    return model