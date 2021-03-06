# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\gui.py
# Compiled at: 2020-03-29 18:02:52
# Size of source mod 2**32: 16665 bytes
from typing import Tuple, Dict, Optional, Union
import arcadeplus

class TextButton:
    """TextButton"""

    def __init__(self, center_x, center_y, width, height, text, font_size=18, font_face: Union[(str, Tuple[(str, ...)])]='Arial', font_color=None, face_color=arcadeplus.color.LIGHT_GRAY, highlight_color=arcadeplus.color.WHITE, shadow_color=arcadeplus.color.GRAY, button_height=2, theme=None):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.pressed = False
        self.active = True
        self.button_height = button_height
        self.theme = theme
        self.font_color = font_color
        if self.theme:
            self.normal_texture = self.theme.button_textures['normal']
            self.hover_texture = self.theme.button_textures['hover']
            self.clicked_texture = self.theme.button_textures['clicked']
            self.locked_texture = self.theme.button_textures['locked']
            self.font_size = self.theme.font_size
            self.font_name = self.theme.font_name
            self.font_color = self.theme.font_color
        else:
            self.font_size = font_size
            self.font_face = font_face
            self.face_color = face_color
            self.highlight_color = highlight_color
            self.shadow_color = shadow_color
            self.font_name = font_face
        if self.font_color is None:
            self.font_color = self.face_color

    def draw_color_theme(self):
        arcadeplus.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.face_color)
        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color
        arcadeplus.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2, self.center_x + self.width / 2, self.center_y - self.height / 2, color, self.button_height)
        arcadeplus.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2, self.center_x + self.width / 2, self.center_y + self.height / 2, color, self.button_height)
        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color
        arcadeplus.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2, self.center_x + self.width / 2, self.center_y + self.height / 2, color, self.button_height)
        arcadeplus.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2, self.center_x - self.width / 2, self.center_y + self.height / 2, color, self.button_height)
        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

    def draw_texture_theme(self):
        if self.pressed:
            arcadeplus.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.clicked_texture)
        else:
            arcadeplus.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.normal_texture)

    def draw(self):
        """ Draw the button """
        if self.theme:
            self.draw_texture_theme()
        else:
            self.draw_color_theme()
        arcadeplus.draw_text((self.text), (self.center_x), (self.center_y), (self.font_color),
          font_size=(self.font_size), font_name=(self.font_name),
          width=(self.width),
          align='center',
          anchor_x='center',
          anchor_y='center')

    def on_press(self):
        pass

    def on_release(self):
        pass

    def check_mouse_press(self, x, y):
        if x > self.center_x + self.width / 2:
            return
        if x < self.center_x - self.width / 2:
            return
        if y > self.center_y + self.height / 2:
            return
        if y < self.center_y - self.height / 2:
            return
        self.on_press()

    def check_mouse_release(self, _x, _y):
        if self.pressed:
            self.on_release()


class SubmitButton(TextButton):

    def __init__(self, textbox, on_submit, x, y, width=100, height=40, text='submit', theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.textbox = textbox
        self.on_submit = on_submit

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            self.on_submit()
            self.textbox.text_storage.text = ''
            self.textbox.text_display.text = ''


class DialogueBox:

    def __init__(self, x, y, width, height, color=None, theme=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.active = False
        self.button_list = []
        self.text_list = []
        self.theme = theme
        if self.theme:
            self.texture = self.theme.dialogue_box_texture

    def on_draw(self):
        if self.active:
            if self.theme:
                arcadeplus.draw_texture_rectangle(self.x, self.y, self.width, self.height, self.texture)
            else:
                arcadeplus.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color)
            for button in self.button_list:
                button.draw()

            for text in self.text_list:
                text.draw()

    def on_mouse_press(self, x, y, _button, _modifiers):
        for button in self.button_list:
            button.check_mouse_press(x, y)

    def on_mouse_release(self, x, y, _button, _modifiers):
        for button in self.button_list:
            button.check_mouse_release(x, y)


class TextLabel:

    def __init__(self, text, x, y, color=arcadeplus.color.BLACK, font_size=22, anchor_x='center', anchor_y='center', width: int=0, align='center', font_name=('Calibri', 'Arial'), bold: bool=False, italic: bool=False, rotation=0):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font_size = font_size
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.width = width
        self.align = align
        self.font_name = font_name
        self.bold = bold
        self.italic = italic
        self.rotation = rotation
        self.active = True

    def draw(self):
        arcadeplus.draw_text((self.text), (self.x), (self.y), (self.color), font_size=(self.font_size), anchor_x=(self.anchor_x),
          anchor_y=(self.anchor_y),
          width=(self.width),
          align=(self.align),
          font_name=(self.font_name),
          bold=(self.bold),
          italic=(self.italic),
          rotation=(self.rotation))


class TextDisplay:

    def __init__(self, x, y, width=300, height=40, outline_color=arcadeplus.color.BLACK, shadow_color=arcadeplus.color.WHITE_SMOKE, highlight_color=arcadeplus.color.WHITE, theme=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.outline_color = outline_color
        self.shadow_color = shadow_color
        self.highlight_color = highlight_color
        self.highlighted = False
        self.text = ''
        self.left_text = ''
        self.right_text = ''
        self.symbol = '|'
        self.cursor_index = 0
        self.theme = theme
        if self.theme:
            self.texture = self.theme.text_box_texture
            self.font_size = self.theme.font_size
            self.font_color = self.theme.font_color
            self.font_name = self.theme.font_name
        else:
            self.texture = None
            self.font_size = 24
            self.font_color = arcadeplus.color.BLACK
            self.font_name = ('Calibri', 'Arial')

    def draw_text(self):
        if self.highlighted:
            arcadeplus.draw_text((self.text[:self.cursor_index] + self.symbol + self.text[self.cursor_index:]), (self.x - self.width / 2.1),
              (self.y), (self.font_color), font_size=(self.font_size), anchor_y='center',
              font_name=(self.font_name))
        else:
            arcadeplus.draw_text((self.text), (self.x - self.width / 2.1), (self.y), (self.font_color), font_size=(self.font_size), anchor_y='center',
              font_name=(self.font_name))

    def color_theme_draw(self):
        if self.highlighted:
            arcadeplus.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.highlight_color)
        else:
            arcadeplus.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.shadow_color)
        self.draw_text()
        arcadeplus.draw_rectangle_outline(self.x, self.y, self.width, self.height, self.outline_color, 2)

    def texture_theme_draw(self):
        arcadeplus.draw_texture_rectangle(self.x, self.y, self.width, self.height, self.texture)
        self.draw_text()

    def draw(self):
        if self.texture == '':
            self.color_theme_draw()
        else:
            self.texture_theme_draw()

    def on_press(self):
        self.highlighted = True

    def on_release(self):
        pass

    def check_mouse_press(self, x, y):
        if x > self.x + self.width / 2:
            self.highlighted = False
            return
        if x < self.x - self.width / 2:
            self.highlighted = False
            return
        if y > self.y + self.height / 2:
            self.highlighted = False
            return
        if y < self.y - self.height / 2:
            self.highlighted = False
            return
        self.on_press()

    def check_mouse_release(self, _x, _y):
        if self.highlighted:
            self.on_release()

    def update(self, _delta_time, text, symbol, cursor_index):
        self.text = text
        self.symbol = symbol
        self.cursor_index = cursor_index


class TextStorage:

    def __init__(self, box_width, font_size=24, theme=None):
        self.box_width = box_width
        self.font_size = font_size
        self.theme = theme
        if self.theme:
            self.font_size = self.theme.font_size
        self.char_limit = self.box_width / self.font_size
        self.text = ''
        self.cursor_index = 1
        self.cursor_symbol = '|'
        self.local_cursor_index = 0
        self.time = 0.0
        self.left_index = 0
        self.right_index = 1
        self.visible_text = ''

    def blink_cursor(self):
        seconds = self.time % 60
        if seconds > 0.1:
            if self.cursor_symbol == '_':
                self.cursor_symbol = '|'
            else:
                self.cursor_symbol = '_'
            self.time = 0.0

    def update(self, delta_time, key):
        self.time += delta_time
        if key:
            if key == arcadeplus.key.BACKSPACE:
                if self.cursor_index < len(self.text):
                    text = self.text[:self.cursor_index - 1]
                    self.text = text + self.text[self.cursor_index:]
                else:
                    self.text = self.text[:-1]
                if self.cursor_index > 0:
                    self.cursor_index -= 1
                if self.left_index > 0:
                    self.left_index -= 1
                if self.right_index > 1:
                    self.right_index -= 1
        elif key == arcadeplus.key.LEFT:
            if self.cursor_index > 0:
                self.cursor_index -= 1
            if 0 < self.left_index == self.cursor_index:
                self.left_index -= 1
                self.right_index -= 1
            elif key == arcadeplus.key.RIGHT:
                if self.cursor_index < len(self.text):
                    self.cursor_index += 1
                if len(self.text) > self.right_index == self.cursor_index:
                    self.right_index += 1
                    self.left_index += 1
            elif self.cursor_index < len(self.text):
                self.text = self.text[:self.cursor_index] + chr(key) + self.text[self.cursor_index:]
                self.cursor_index += 1
                self.right_index += 1
                if len(self.text) > self.char_limit:
                    self.left_index += 1
            else:
                self.text += chr(key)
                self.cursor_index += 1
                self.right_index += 1
            if len(self.text) >= self.char_limit:
                self.left_index += 1
            self.visible_text = self.text[self.left_index:self.right_index]
            if self.cursor_index > self.left_index:
                self.local_cursor_index = self.cursor_index - self.left_index
        else:
            self.local_cursor_index = self.left_index
        return (self.visible_text, self.cursor_symbol, self.local_cursor_index)


class TextBox:

    def __init__(self, x, y, width=300, height=40, theme=None, outline_color=arcadeplus.color.BLACK, font_size=24, shadow_color=arcadeplus.color.WHITE_SMOKE, highlight_color=arcadeplus.color.WHITE):
        self.theme = theme
        if self.theme:
            self.text_display = TextDisplay(x, y, width, height, theme=(self.theme))
            self.text_storage = TextStorage(width, theme=(self.theme))
        else:
            self.text_display = TextDisplay(x, y, width, height, outline_color, shadow_color, highlight_color)
            self.text_storage = TextStorage(width, font_size)
        self.text = ''

    def draw(self):
        self.text_display.draw()

    def update(self, delta_time, key):
        if self.text_display.highlighted:
            self.text, symbol, cursor_index = self.text_storage.update(delta_time, key)
            self.text_display.update(delta_time, self.text, symbol, cursor_index)

    def check_mouse_press(self, x, y):
        self.text_display.check_mouse_press(x, y)

    def check_mouse_release(self, x, y):
        self.text_display.check_mouse_release(x, y)


class Theme:

    def __init__(self):
        self.button_textures = {'normal':'', 
         'hover':'',  'clicked':'',  'locked':''}
        self.menu_texture = ''
        self.window_texture = ''
        self.dialogue_box_texture = ''
        self.text_box_texture = ''
        self.font_color = arcadeplus.color.BLACK
        self.font_size = 24
        self.font_name = ('Calibri', 'Arial')

    def add_button_textures(self, normal, hover='', clicked='', locked=''):
        self.button_textures['normal'] = arcadeplus.load_texture(normal)
        self.button_textures['hover'] = arcadeplus.load_texture(hover)
        self.button_textures['clicked'] = arcadeplus.load_texture(clicked)
        self.button_textures['locked'] = arcadeplus.load_texture(locked)

    def add_window_texture(self, window_texture):
        self.window_texture = arcadeplus.load_texture(window_texture)

    def add_menu_texture(self, menu_texture):
        self.menu_texture = arcadeplus.load_texture(menu_texture)

    def add_dialogue_box_texture(self, dialogue_box_texture):
        self.dialogue_box_texture = arcadeplus.load_texture(dialogue_box_texture)

    def add_text_box_texture(self, text_box_texture):
        self.text_box_texture = arcadeplus.load_texture(text_box_texture)

    def set_font(self, font_size, font_color, font_name=('Calibri', 'Arial')):
        self.font_color = font_color
        self.font_size = font_size
        self.font_name = font_name