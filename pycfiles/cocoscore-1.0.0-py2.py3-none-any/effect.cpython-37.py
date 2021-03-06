# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\cocos\audio\effect.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2789 bytes
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
from cocos import audio
try:
    from cocos.audio.pygame.mixer import Sound
except ImportError:
    audio._working = False

from . import actions

class Effect(object):
    """Effect"""

    def __init__(self, filename):
        """Initialize the effect

        :Parameters:
            `filename` : fullpath
                path of a WAV or Ogg audio file
        """
        if audio._working:
            self.sound = Sound(filename)
        else:
            self.sound = None
        self.action = actions.PlayAction(self.sound)

    def play(self):
        if audio._working:
            self.sound.play()