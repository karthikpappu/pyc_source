# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\pymunk_pegboard.py
# Compiled at: 2020-03-29 18:07:17
# Size of source mod 2**32: 6128 bytes
__doc__ = '\nUse Pymunk physics engine.\n\nFor more info on Pymunk see:\nhttp://www.pymunk.org/en/latest/\n\nTo install pymunk:\npip install pymunk\n\nArtwork from http://kenney.nl\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.pymunk_pegboard\n\nClick and drag with the mouse to move the boxes.\n'
import arcadeplus, pymunk, random, timeit, math, os
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Pymunk Pegboard Example'

class CircleSprite(arcadeplus.Sprite):

    def __init__(self, filename, pymunk_shape):
        super().__init__(filename, center_x=(pymunk_shape.body.position.x), center_y=(pymunk_shape.body.position.y))
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2
        self.pymunk_shape = pymunk_shape


class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.peg_list = arcadeplus.SpriteList()
        self.ball_list = arcadeplus.SpriteList()
        arcadeplus.set_background_color(arcadeplus.color.DARK_SLATE_GRAY)
        self.draw_time = 0
        self.processing_time = 0
        self.time = 0
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)
        self.static_lines = []
        self.ticks_to_next_ball = 10
        body = pymunk.Body(body_type=(pymunk.Body.STATIC))
        shape = pymunk.Segment(body, [0, 10], [SCREEN_WIDTH, 10], 0.0)
        shape.friction = 10
        self.space.add(shape)
        self.static_lines.append(shape)
        body = pymunk.Body(body_type=(pymunk.Body.STATIC))
        shape = pymunk.Segment(body, [SCREEN_WIDTH - 50, 10], [SCREEN_WIDTH, 30], 0.0)
        shape.friction = 10
        self.space.add(shape)
        self.static_lines.append(shape)
        body = pymunk.Body(body_type=(pymunk.Body.STATIC))
        shape = pymunk.Segment(body, [50, 10], [0, 30], 0.0)
        shape.friction = 10
        self.space.add(shape)
        self.static_lines.append(shape)
        radius = 20
        separation = 150
        for row in range(6):
            for column in range(6):
                x = column * separation + separation // 2 * (row % 2)
                y = row * separation + separation // 2
                body = pymunk.Body(body_type=(pymunk.Body.STATIC))
                body.position = (x, y)
                shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
                shape.friction = 0.3
                self.space.add(body, shape)
                sprite = CircleSprite(':resources:images/pinball/bumper.png', shape)
                self.peg_list.append(sprite)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        draw_start_time = timeit.default_timer()
        self.peg_list.draw()
        self.ball_list.draw()
        for line in self.static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            arcadeplus.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, arcadeplus.color.WHITE, 2)

        output = f"Processing time: {self.processing_time:.3f}"
        arcadeplus.draw_text(output, 20, SCREEN_HEIGHT - 20, arcadeplus.color.WHITE, 12)
        output = f"Drawing time: {self.draw_time:.3f}"
        arcadeplus.draw_text(output, 20, SCREEN_HEIGHT - 40, arcadeplus.color.WHITE, 12)
        self.draw_time = timeit.default_timer() - draw_start_time

    def on_update(self, delta_time):
        start_time = timeit.default_timer()
        self.ticks_to_next_ball -= 1
        if self.ticks_to_next_ball <= 0:
            self.ticks_to_next_ball = 20
            mass = 0.5
            radius = 15
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT
            body.position = (x, y)
            shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
            shape.friction = 0.3
            self.space.add(body, shape)
            sprite = CircleSprite(':resources:images/items/coinGold.png', shape)
            self.ball_list.append(sprite)
        for ball in self.ball_list:
            if ball.pymunk_shape.body.position.y < 0:
                self.space.remove(ball.pymunk_shape, ball.pymunk_shape.body)
                ball.remove_from_sprite_lists()

        self.space.step(0.016666666666666666)
        for ball in self.ball_list:
            ball.center_x = ball.pymunk_shape.body.position.x
            ball.center_y = ball.pymunk_shape.body.position.y
            ball.angle = math.degrees(ball.pymunk_shape.body.angle)

        self.time = timeit.default_timer() - start_time


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.run()


if __name__ == '__main__':
    main()