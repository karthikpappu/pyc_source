# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\cocos2020\cocos\layer\base_layers.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 4869 bytes
"""Layer class and subclasses.

Layers are typically thought as event handlers and / or as containers that help
to organize the scene visuals or logic.

The transform_anchor is set by default to the window's center, which most of the
time provides the desired behavior on rotation and scale.

By default a layer will not listen to events, his `is_event_handler` must be set
to True before the layer enters the stage to enable the automatic registering as
event handler.
"""
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import cocos.director as director
from cocos import cocosnode
from cocos import scene
__all__ = [
 'Layer', 'MultiplexLayer']

class Layer(cocosnode.CocosNode):
    __doc__ = 'A CocosNode that can automatically register to listen to director.window events'
    is_event_handler = False

    def __init__(self):
        super(Layer, self).__init__()
        self.scheduled_layer = False
        x, y = director.get_window_size()
        self.transform_anchor_x = x // 2
        self.transform_anchor_y = y // 2

    def on_enter(self):
        super(Layer, self).on_enter()
        if self.is_event_handler:
            director.window.push_handlers(self)

    def on_exit(self):
        super(Layer, self).on_exit()
        if self.is_event_handler:
            director.window.remove_handlers(self)


class MultiplexLayer(Layer):
    __doc__ = 'A Composite layer that only enables one layer at a time.\n\n    This is useful, for example, when you have 3 or 4 menus, but you want to\n    show one at the time.\n\n    After instantiation the enabled layer is layers[0]\n\n    Arguments:\n        *layers : iterable with the layers to be managed.\n    '

    def __init__(self, *layers):
        super(MultiplexLayer, self).__init__()
        self.layers = layers
        self.enabled_layer = 0
        self.add(self.layers[self.enabled_layer])

    def switch_to(self, layer_number):
        """Switches to another of the layers managed by this instance.

        Arguments:
            layer_number (int) :
                **Must** be a number between 0 and the (number of layers - 1).
                The running layer will receive an ``on_exit()`` call, and the
                new layer will receive an ``on_enter()`` call.

        Raises:
            Exception: layer_number was out of bound.
        """
        if layer_number < 0 or layer_number >= len(self.layers):
            raise Exception('Multiplexlayer: Invalid layer number')
        self.remove(self.layers[self.enabled_layer])
        self.enabled_layer = layer_number
        self.add(self.layers[self.enabled_layer])