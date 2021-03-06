# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\full_screen_example.py
# Compiled at: 2020-03-29 18:05:16
# Size of source mod 2**32: 3929 bytes
"""
Use sprites to scroll around a large screen.

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.full_screen_example
"""
import arcadeplus, os
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Full Screen Example'
VIEWPORT_MARGIN = 40
MOVEMENT_SPEED = 5

class MyGame(arcadeplus.Window):
    __doc__ = ' Main application class. '

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)
        self.example_image = arcadeplus.load_texture(':resources:images/tiles/boxCrate_double.png')

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        left, screen_width, bottom, screen_height = self.get_viewport()
        text_size = 18
        arcadeplus.draw_text('Press F to toggle between full screen and windowed mode, unstretched.', (screen_width // 2),
          (screen_height // 2 - 20), (arcadeplus.color.WHITE),
          text_size, anchor_x='center')
        arcadeplus.draw_text('Press S to toggle between full screen and windowed mode, stretched.', (screen_width // 2),
          (screen_height // 2 + 20), (arcadeplus.color.WHITE),
          text_size, anchor_x='center')
        for x in range(64, 800, 128):
            y = 64
            width = 128
            height = 128
            arcadeplus.draw_texture_rectangle(x, y, width, height, self.example_image)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcadeplus.key.F:
            self.set_fullscreen(not self.fullscreen)
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)
        if key == arcadeplus.key.S:
            self.set_fullscreen(not self.fullscreen)
            self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)


def main():
    """ Main method """
    MyGame()
    arcadeplus.run()


if __name__ == '__main__':
    main()