# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/Actors/RandomPlayer.py
# Compiled at: 2016-08-02 10:00:55
# Size of source mod 2**32: 237 bytes
from . import RandomActor
from ..GameBase import Player

class RandomPlayer(RandomActor, Player):
    """RandomPlayer"""

    def __str__(self):
        return 'RandomPlayer'