# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_tiles_autotest.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1645 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1.1, s, t 2.1, s, t 3.1, s, t 4.1, s, t 5.1, s, t 6.1, s, q'
tags = 'CallFunc, tiles'
import pyglet
pyglet.resource.path.append(pyglet.resource.get_script_home())
pyglet.resource.reindex()
import cocos
from cocos import tiles, layer
from cocos.actions import CallFunc, ScaleTo, Delay
import cocos.director as director

class TestScene(cocos.scene.Scene):

    def __init__(self):
        super(TestScene, self).__init__()
        scroller = layer.ScrollingManager()
        scrollable = tiles.load('road-map.xml')['map0']
        scroller.add(scrollable)
        self.add(scroller)
        template_action = CallFunc(scroller.set_focus, 0, 0) + Delay(1) + CallFunc(scroller.set_focus, 768, 0) + Delay(1) + CallFunc(scroller.set_focus, 768, 768) + Delay(1) + CallFunc(scroller.set_focus, 1500, 768) + Delay(1) + ScaleTo(0.75, 1) + CallFunc(scrollable.set_debug, True) + Delay(1) + CallFunc(director.window.set_size, 800, 600)
        scroller.do(template_action)


def main():
    director.init(width=600, height=300, autoscale=False, resizable=True)
    main_scene = TestScene()
    director.run(main_scene)


if __name__ == '__main__':
    main()