# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrana/players/pygletplayer.py
# Compiled at: 2011-07-09 22:56:18
import pyglet
from feather import Plugin

class PygletPlayer(Plugin):
    listeners = set(['songloaded', 'pause', 'skipsong', 'skipalbum'])
    messengers = set(['songstart', 'songpause', 'songend', 'songresume'])
    name = 'PygletPlayer'

    def pre_run(self):
        pyglet.options['audio'] = ('alsa', 'directsound', 'openal', 'silent')
        pyglet.options['debug_media'] = True
        pyglet.app.run()

    def songloaded(self, payload):
        try:
            song = pyglet.media.load(payload)
        except pyglet.media.MediaException:
            print 'unsupported file %s' % payload
        else:
            self.playing = True
            if self.player:
                self.player.queue(payload)
                self.player.next()
            else:
                self.player = song.play()
                self.player.volume = 1.0
                self.player.set_handler('on_eos', self.on_eos)
            self.send('songstart', payload)

    def pause(self, payload=None):
        if self.playing:
            self.player.pause()
            self.playing = False
            self.send('songpause')
        else:
            self.player.play()
            self.playing = True
            self.send('songresume')

    def skipsong(self, payload=None):
        self.player.pause()

    def skipalbum(self, payload=None):
        self.player.pause()

    def on_eos(self):
        self.send('songend')