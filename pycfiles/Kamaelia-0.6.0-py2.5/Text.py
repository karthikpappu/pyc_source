# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/UI/Pygame/Text.py
# Compiled at: 2008-10-19 12:19:52
"""
============================================
Pygame components for text input and display
============================================

TextDisplayer displays any data it receives on a Pygame surface. Every new piece
of data is displayed on its own line, and lines wrap automatically.

Textbox displays user input while the user types, and sends its string buffer
to its 'outbox' when it receives a '
'.

Example Usage
-------------

To take user input in Textbox and display it in TextDisplayer::

    Pipeline(Textbox(size = (800, 300),
                     position = (0,0)),
             TextDisplayer(size = (800, 300),
                           position = (0,340))
             ).run()

How does it work? 
-----------------
TextDisplayer requests a display from the Pygame Display service and requests
that Pygame Display send all keypresses to it. Every time TextDisplayer receives
a keypress, it updates its string buffer and the display. 

If it receives a newline, or if text must wrap, it moves the existing text
upwards and blits the new line onto the bottom. 

Known issues
------------
The line wrapping length is specified by the width of the display divided by the
width of the letter 'a' in the displayed font, so lines may wrap too far off the
edge of the screen if the user types very narrow text (i.e. just spaces with no
other charachters), or too far inside the edge of the screen (usually).
"""
import pygame, time
from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.UI.Pygame.KeyEvent import KeyEvent
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished, WaitComplete
from pygame.locals import *

class TextDisplayer(component):
    """    TextDisplayer(...) -> new TextDisplayer Pygame component.

    Keyword arguments:

    - size             -- (w, h) size of the TextDisplayer surface, in pixels.
                          Default (500, 300).
    - text_height      -- font size. Default 18.
    - bgcolour         -- tuple containing RGB values for the background color.
                          Default is a pale yellow.
    - fgcolour         -- tuple containing RGB values for the text color.
                          Default is black.
    - position         -- tuple containing x,y coordinates of the surface's
                          upper left corner in relation to the Pygame
                          window. Default (0,0)
    """
    Inboxes = {'inbox': 'for incoming lines of text', '_surface': 'for PygameDisplay to send surfaces to', 
       '_quitevents': 'user-generated quit events', 
       'control': 'shutdown handling'}
    Outboxes = {'outbox': 'not used', '_pygame': 'for sending requests to PygameDisplay', 
       'signal': 'propagates out shutdown signals'}
    size = (500, 300)
    text_height = 18
    bgcolour = (255, 255, 200)
    fgcolour = (0, 0, 0)
    position = (0, 0)

    def __init__(self, **argd):
        """Initialises"""
        super(TextDisplayer, self).__init__(**argd)
        self.screen_width = self.size[0]
        self.screen_height = self.size[1]
        self.background_color = self.bgcolour
        self.text_color = self.fgcolour
        self.done = False

    def initPygame(self, **argd):
        """requests a display surface from the PygameDisplay service, fills
        the color in, and copies it"""
        displayservice = PygameDisplay.getDisplayService()
        self.link((self, '_pygame'), displayservice)
        self.send(argd, '_pygame')
        while not self.dataReady('_surface'):
            yield 1

        self.screen = self.recv('_surface')
        self.screen.fill(self.background_color)
        self.scratch = self.screen.copy()
        self.send({'REDRAW': True, 'surface': self.screen}, '_pygame')
        yield 1
        h = self.screen_height
        w = self.screen_width
        th = self.text_height
        self.font = pygame.font.Font(None, th)
        self.linelen = w / self.font.size('a')[0]
        self.keepRect = pygame.Rect((0, th), (w, h - th))
        self.scrollingRect = pygame.Rect((0, 0), (w, h - th))
        self.writeRect = pygame.Rect((0, h - th), (w, th))
        return

    def main(self):
        """Main loop"""
        yield WaitComplete(self.initPygame(DISPLAYREQUEST=True, size=(
         self.screen_width, self.screen_height), callback=(
         self, '_surface'), position=self.position))
        while not self.needShutdown():
            yield 1
            if self.dataReady('inbox'):
                line = str(self.recv('inbox'))
                self.update(line)
            while not self.anyReady():
                self.pause()
                yield 1

    def update(self, text):
        """Updates text to the bottom of the screen while scrolling old text
        upwards. Delegates most of the work to updateLine"""
        while len(text) > self.linelen:
            cutoff = text.rfind(' ', 0, self.linelen)
            if cutoff == -1:
                cutoff = self.linelen
            self.updateLine(text[0:cutoff])
            text = text[cutoff + 1:]

        self.updateLine(text)

    def updateLine(self, line):
        """Updates one line of text to bottom of screen, scrolling old text upwards."""
        line = line.replace('\r', ' ')
        line = line.replace('\n', ' ')
        lineSurf = self.font.render(line, True, self.text_color)
        self.screen.fill(self.background_color)
        self.screen.blit(self.scratch, self.scrollingRect, self.keepRect)
        self.screen.blit(lineSurf, self.writeRect)
        self.scratch.fill(self.background_color)
        self.scratch.blit(self.screen, self.screen.get_rect())
        self.send({'REDRAW': True, 'surface': self.screen}, '_pygame')

    def needShutdown(self):
        """Checks for control messages"""
        while self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.done = True

        if self.dataReady('_quitevents'):
            self.done = True
        if self.done:
            self.send(shutdownMicroprocess(), 'signal')
            return True


class Textbox(TextDisplayer):
    """    Textbox(...) -> New Pygame Textbox component

    Keyword Arguments:
    
    - Textbox inherits its keyword arguments from TextDisplayer. Please see
      TextDisplayer docs.

    Reads keyboard input and updates it on the screen. Flushes string buffer and
    sends it to outbox when a newline is encountered.
    """
    Inboxes = {'inbox': 'for incoming lines of text', '_surface': 'for PygameDisplay to send surfaces to', 
       '_quitevents': 'user-generated quit events', 
       '_events': 'key events', 
       'control': 'shutdown handling'}
    Outboxes = {'outbox': 'not used', '_pygame': 'for sending requests to PygameDisplay', 
       'signal': 'propagates out shutdown signals'}
    initial_string_buffer = ''

    def setText(self, text):
        """erases the screen and updates it with text"""
        self.screen.fill(self.background_color)
        self.scratch.fill(self.background_color)
        self.update(text)

    def main(self):
        """        Requests a surface from PygameDisplay and registers to listen for events
        Then enters the main loop, which checks for Pygame events and updates
        them to the screen.
        """
        yield WaitComplete(self.initPygame(DISPLAYREQUEST=True, size=(
         self.screen_width, self.screen_height), callback=(
         self, '_surface'), position=self.position, events=(
         self, '_events')))
        self.send({'ADDLISTENEVENT': pygame.KEYDOWN, 'surface': self.screen}, '_pygame')
        string_buffer = self.initial_string_buffer
        while not self.needShutdown():
            yield 1
            while self.dataReady('_events'):
                for event in self.recv('_events'):
                    char = event.unicode
                    if char == '\n' or char == '\r':
                        self.send(string_buffer)
                        string_buffer = ''
                    elif event.key == K_BACKSPACE:
                        string_buffer = string_buffer[:-1]
                    elif event.key == K_ESCAPE:
                        self.done = True
                    else:
                        string_buffer += char
                    self.setText(string_buffer + '|')

            while not self.anyReady():
                self.pause()
                yield 1


__kamaelia_components__ = (
 TextDisplayer, Textbox)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    import Axon, time
    from Kamaelia.Chassis.Pipeline import Pipeline

    class TimedLineSender(Axon.ThreadedComponent.threadedcomponent):
        text = "                    To be, or not to be: that is the question:\n                    Whether 'tis nobler in the mind to suffer\n                    The slings and arrows of outrageous fortune,\n                    Or to take arms against a sea of troubles,\n                    And by opposing end them? To die: to sleep;\n                    No more; and by a sleep to say we end\n                    The heart-ache and the thousand natural shocks That flesh is heir to, 'tis a consummation Devoutly to be wish'd. To die, to sleep;\n                    To sleep: perchance to dream: ay, there's the rub;\n                    For in that sleep of death what dreams may come\n                    When we have shuffled off this mortal coil,\n                    Must give us pause: there's the respect\n                    That makes calamity of so long life;\n                    "
        strip_leading = True
        debug = True
        delay = 0.5

        def main(self):
            lines = self.text.split('\n')
            for line in lines:
                if self.strip_leading:
                    line = line.lstrip()
                time.sleep(self.delay)
                self.send(line)

            self.send(producerFinished(), 'signal')


    Pipeline(TimedLineSender(), TextDisplayer()).run()