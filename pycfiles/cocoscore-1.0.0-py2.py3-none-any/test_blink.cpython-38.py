# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_blink.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1461 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 2.1, s, t 2.6, s, t 3.1, s, t 5.1, s, t 5.6, s, t 6.1, s, t 8.1, s, q'
tags = 'Blink'
import cocos
import cocos.director as director
from cocos.actions import Blink, Delay
from cocos.sprite import Sprite
import pyglet

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        template_action = Delay(2) + Blink(3, 3)
        self.sprite = Sprite('grossini.png', (x // 2, y // 2))
        self.add(self.sprite)
        self.sprite.do(template_action)
        self.sprite2 = Sprite('grossinis_sister1.png', (x // 2 + 50, y // 2 + 50))
        self.sprite2.scale = 0.5
        self.sprite2.visible = False
        self.add(self.sprite2)
        self.sprite2.do(Delay(3) + template_action)


description = '\nGrossini starts visible, blinks three times and stay visible;\nSheila, which starts invisible, will blink three times and stay invisible'

def main():
    print(description)
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()