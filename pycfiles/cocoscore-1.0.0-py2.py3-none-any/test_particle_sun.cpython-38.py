# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_particle_sun.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1358 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 'f 10 0.033, s, f 20 0.033, s, f 30 0.033, s, f 30 0.033, s, q'
tags = 'particles, Sun'
import pyglet, cocos
import cocos.director as director
from cocos.actions import *
from cocos.layer import *
from cocos.particle_systems import *
from cocos.particle import *

class L(Layer):
    is_event_handler = True

    def __init__(self):
        super(L, self).__init__()
        p = Sun()
        p.position = (320, 240)
        self.add(p)
        p.position_type = ParticleSystem.POSITION_FREE
        self.sun = p

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        x, y = director.get_virtual_coordinates(x, y)
        x, y = self.sun.position
        self.sun.position = (x + dx, y + dy)


def main():
    director.init(resizable=True)
    main_scene = cocos.scene.Scene()
    main_scene.add(L())
    director.run(main_scene)


if __name__ == '__main__':
    main()