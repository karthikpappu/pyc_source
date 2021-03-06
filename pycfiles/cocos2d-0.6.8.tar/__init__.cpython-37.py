# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\cocos\__init__.py
# Compiled at: 2020-01-21 23:28:16
# Size of source mod 2**32: 5351 bytes
"""a framework for building 2D games, demos, and other graphical/interactive applications.

Main Features
-------------

    * Flow control: Manage the flow control between different scenes in an easy way
    * Sprites: Fast and easy sprites
    * Actions: Just tell sprites what you want them to do. Composable actions like move, rotate, scale and much more
    * Effects: Effects like waves, twirl, lens and much more
    * Tiled Maps: Support for rectangular and hexagonal tiled maps
    * Collision: Basic pure python support for collisions
    * Transitions: Move from scene to scene with style
    * Menus: Built in classes to create menus
    * Text Rendering: Label and HTMLLabel with action support
    * Documentation: Programming Guide + API Reference + Video Tutorials + Lots of simple tests showing how to use it
    * Built-in Python Interpreter: For debugging purposes
    * BSD License: Just use it
    * Pyglet Based: No external dependencies
    * OpenGL Based: Hardware Acceleration

http://python.cocos2d.org
"""
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
__version__ = '0.6.8'
__author__ = 'cocos2d team'
version = __version__
import sys, os, pyglet
pyglet.resource.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources'))
pyglet.resource.reindex()
parts = pyglet.version.split('.')
p_major, p_med, p_step = parts
bad_pyglet_version = True
if p_major != '1':
    print('This cocos version needs pyglet >= 1.4.10 and < 2.0')
else:
    if p_med not in ('4', '5'):
        print('This cocos version needs pyglet >= 1.4.10 or 1.5.x')
    else:
        if p_med == '4':
            if int(p_step) < 10:
                print('This cocos version needs pyglet >= 1.4.10 or 1.5.x')
            else:
                bad_pyglet_version = False
        else:
            if bad_pyglet_version:
                raise Exception('\n*** bad pyglet version, found version %s ***\n' % pyglet.version)
            try:
                unittesting = os.environ['cocos_utest']
            except KeyError:
                unittesting = False

        del os
        del pyglet
        if sys.platform == 'win32':
            major, minor = sys.version_info[0:2]
            if not (major == 2 or major) == 3 or minor < 4:
                import imp
                try:
                    dummy, sdl_lib_path, dummy = imp.find_module('pygame')
                    del dummy
                except ImportError:
                    sdl_lib_path = None

            else:
                pass
            import importlib
            try:
                spec = importlib.util.find_spec('pygame')
                sdl_lib_path = spec.submodule_search_locations[0]
            except Exception:
                sdl_lib_path = None

        if not unittesting:
            from cocos import cocosnode
            from cocos import actions
            from cocos import director
            from cocos import layer
            from cocos import menu
            from cocos import sprite
            from cocos import path
            from cocos import scene
            from cocos import grid
            from cocos import text
            from cocos import camera
            from cocos import draw
            from cocos import skeleton
            from cocos import rect
            from cocos import tiles