# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_schedule_interval.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1437 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1.1, s, t 2.1, s, t 3.1, s, q'
tags = 'schedule_interval, position'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
import pyglet, random
from math import sin, cos

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        self.sprite = Sprite('grossini.png')
        self.add(self.sprite)
        w, h = director.get_window_size()
        self.coords_from_corner = [(0, 0), (0, h), (w, h), (w, 0)]
        self.corner = 0
        self.schedule_interval(self.change_sprite_pos, 1)
        self.change_sprite_pos(0.0)
        self.schedule(lambda x: 0)

    def change_sprite_pos(self, dt):
        self.sprite.position = self.coords_from_corner[self.corner]
        self.corner = (self.corner + 1) % len(self.coords_from_corner)


description = '\nGrossini sprite will change position each second, showing at the screen corners\n'

def main():
    print(description)
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()