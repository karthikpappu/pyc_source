# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/UI/Pygame/MagnaDoodle.py
# Compiled at: 2008-10-19 12:19:52
"""===========================
Simple Pygame drawing board
===========================

A simple drawing board for the pygame display service.

Use your left mouse button to draw to the board and the
right to erase your artwork.

"""
import pygame, Axon
from Axon.Ipc import producerFinished
from Kamaelia.UI.PygameDisplay import PygameDisplay

class MagnaDoodle(Axon.Component.component):
    """   MagnaDoodle(...) -> A new MagnaDoodle component.

   A simple drawing board for the pygame display service.

   (this component and its documentation is heaviliy based on Kamaelia.UI.Pygame.Button)

   Keyword arguments:
   
   - position     -- (x,y) position of top left corner in pixels
   - margin       -- pixels margin between caption and button edge (default=8)
   - bgcolour     -- (r,g,b) fill colour (default=(224,224,224))
   - fgcolour     -- (r,g,b) text colour (default=(0,0,0))
   - transparent  -- draw background transparent if True (default=False)
   - size         -- None or (w,h) in pixels (default=None)
   
   """
    Inboxes = {'inbox': 'Receive events from PygameDisplay', 'control': 'For shutdown messages', 
       'callback': 'Receive callbacks from PygameDisplay'}
    Outboxes = {'outbox': 'not used', 'signal': 'For shutdown messages', 
       'display_signal': 'Outbox used for communicating to the display surface'}

    def __init__(self, caption=None, position=None, margin=8, bgcolour=(124, 124, 124), fgcolour=(0, 0, 0), msg=None, transparent=False, size=(200, 200)):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(MagnaDoodle, self).__init__()
        self.backgroundColour = bgcolour
        self.foregroundColour = fgcolour
        self.margin = margin
        self.oldpos = None
        self.drawing = False
        self.size = size
        self.innerRect = pygame.Rect(10, 10, self.size[0] - 20, self.size[1] - 20)
        if msg is None:
            msg = (
             'CLICK', self.id)
        self.eventMsg = msg
        if transparent:
            transparency = bgcolour
        else:
            transparency = None
        self.disprequest = {'DISPLAYREQUEST': True, 'callback': (self, 'callback'), 'events': (
                    self, 'inbox'), 
           'size': self.size, 
           'transparency': transparency}
        if position is not None:
            self.disprequest['position'] = position
        return

    def waitBox(self, boxname):
        """Generator. yields 1 until data ready on the named inbox."""
        waiting = True
        while waiting:
            if self.dataReady(boxname):
                return
            else:
                yield 1

    def drawBG(self):
        self.display.fill((255, 0, 0))
        self.display.fill(self.backgroundColour, self.innerRect)

    def main(self):
        """Main loop."""
        displayservice = PygameDisplay.getDisplayService()
        self.link((self, 'display_signal'), displayservice)
        self.send(self.disprequest, 'display_signal')
        for _ in self.waitBox('callback'):
            yield 1

        self.display = self.recv('callback')
        self.drawBG()
        self.blitToSurface()
        self.send({'ADDLISTENEVENT': pygame.MOUSEBUTTONDOWN, 'surface': self.display}, 'display_signal')
        self.send({'ADDLISTENEVENT': pygame.MOUSEBUTTONUP, 'surface': self.display}, 'display_signal')
        self.send({'ADDLISTENEVENT': pygame.MOUSEMOTION, 'surface': self.display}, 'display_signal')
        done = False
        while not done:
            while self.dataReady('control'):
                cmsg = self.recv('control')
                if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
                    self.send(cmsg, 'signal')
                    done = True

            while self.dataReady('inbox'):
                for event in self.recv('inbox'):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.drawing = True
                        elif event.button == 3:
                            self.oldpos = None
                            self.drawBG()
                            self.blitToSurface()
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        self.drawing = False
                        self.oldpos = None
                    elif event.type == pygame.MOUSEMOTION:
                        if self.drawing and self.innerRect.collidepoint(*event.pos):
                            if self.oldpos == None:
                                self.oldpos = event.pos
                            else:
                                pygame.draw.line(self.display, (0, 0, 0), self.oldpos, event.pos, 3)
                                self.oldpos = event.pos
                            self.blitToSurface()

            self.pause()
            yield 1

        return

    def blitToSurface(self):
        self.send({'REDRAW': True, 'surface': self.display}, 'display_signal')


__kamaelia_components__ = (
 MagnaDoodle,)
if __name__ == '__main__':
    from Kamaelia.Util.ConsoleEcho import consoleEchoer
    from pygame.locals import *
    Magna = MagnaDoodle().activate()
    Axon.Scheduler.scheduler.run.runThreads()