# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\platformer.py
# Compiled at: 2020-03-29 18:06:56
# Size of source mod 2**32: 7751 bytes
"""
Platformer Game
"""
import arcadeplus
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = 'Platformer'
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 25
LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 100

class MyGame(arcadeplus.Window):
    __doc__ = '\n    Main application class.\n    '

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.view_bottom = 0
        self.view_left = 0
        self.score = 0
        self.collect_coin_sound = arcadeplus.load_sound(':resources:sounds/coin1.wav')
        self.jump_sound = arcadeplus.load_sound(':resources:sounds/jump1.wav')
        arcadeplus.set_background_color(arcadeplus.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.view_bottom = 0
        self.view_left = 0
        self.score = 0
        self.player_list = arcadeplus.SpriteList()
        self.wall_list = arcadeplus.SpriteList()
        self.coin_list = arcadeplus.SpriteList()
        image_source = ':resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png'
        self.player_sprite = arcadeplus.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)
        map_name = ':resources:tmx_maps/test_map_7.tmx'
        platforms_layer_name = 'Platforms'
        coins_layer_name = 'Coins'
        my_map = arcadeplus.tilemap.read_tmx(map_name)
        self.wall_list = arcadeplus.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)
        self.coin_list = arcadeplus.tilemap.process_layer(my_map, coins_layer_name, TILE_SCALING)
        if my_map.background_color:
            arcadeplus.set_background_color(my_map.background_color)
        self.physics_engine = arcadeplus.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        """ Render the screen. """
        arcadeplus.start_render()
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        score_text = f"Score: {self.score}"
        arcadeplus.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcadeplus.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcadeplus.key.UP or key == arcadeplus.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcadeplus.play_sound(self.jump_sound)
        elif key == arcadeplus.key.LEFT or key == arcadeplus.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            if key == arcadeplus.key.RIGHT or key == arcadeplus.key.D:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcadeplus.key.LEFT or key == arcadeplus.key.A:
            self.player_sprite.change_x = 0
        else:
            if key == arcadeplus.key.RIGHT or key == arcadeplus.key.D:
                self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.physics_engine.update()
        coin_hit_list = arcadeplus.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcadeplus.play_sound(self.collect_coin_sound)
            self.score += 1

        changed = False
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True
        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            arcadeplus.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()