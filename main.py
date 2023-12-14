import arcade
from pyglet.math import Vec2

from entities.cat import Cat
from entities.kitten import Kitten
from entities.person import Person
from enums import SpritePosition, PersonStates

DEFAULT_SCREEN_WIDTH = 960
DEFAULT_SCREEN_HEIGHT = 540
SPRITE_SCALING = 0.3


class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, center_window=True, title="Кошка, котёнок и человек")

        self.background = None
        self.person = None
        self.cat = None
        self.kitten = None
        self.positions_kitten = [SpritePosition.KITTEN_EAT, SpritePosition.KITTEN_WITH_MOTHER,
                                 SpritePosition.KITTEN_PLAYING_ZONE]
        self.end_turn = False
        self.timer = 0

    def setup(self):
        self.person = Person(image="resources/person.png", scaling=0.11)
        self.person.set_position(SpritePosition.PERSON_BED)
        self.person.lie_on_bed()
        self.kitten = Kitten(image="resources/kitten_stand.png", scaling=0.09)
        self.kitten.set_position(SpritePosition.KITTEN_COUCH)
        self.cat = Cat(image="resources/cat_stand.png", scaling=0.11)
        self.background = arcade.load_texture("resources/background.png")

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, self.background)
        arcade.draw_rectangle_filled(905, DEFAULT_SCREEN_HEIGHT // 2, 190, DEFAULT_SCREEN_HEIGHT,
                                     arcade.color.LIGHT_GRAY)

        self.person.draw()
        self.kitten.draw()
        self.cat.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        # print(x, y)
        position = Vec2(x - self.width / 2, y - self.height / 2)
        # self.camera.move_to(position, CAMERA_SPEED)

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            print(self.kitten.sprite.angle)
            print(f"click: {x}, {y}")
            # self.kitten.sprite.destination_point = x, y
        elif button == arcade.MOUSE_BUTTON_LEFT:
            self.kitten.decide_what_do_next(person=self.person)
            self.person.decide_what_do_next()
            if not len(self.positions_kitten):
                return
            print(self.kitten.next_position)
            print(self.person.next_position)
            self.kitten.move_to(self.kitten.next_position)
            self.person.move_to(self.person.next_position)

    def update(self, delta_time):
        if self.end_turn:
            self.timer += 1
            if self.timer == 30:
                self.end_turn = False
                self.timer = 0

                self.kitten.update_indicators(self.person)
                self.person.update_indicators(self.person)
                self.person.current_state = PersonStates.WAITING
                self.person.next_position = None
                self.kitten.next_position = None
            return

        self.person.update()
        self.kitten.update()

        if self.person.next_position is not None and self.kitten.next_position is not None:
            if not self.person.sprite.destination_point and not self.kitten.sprite.destination_point:
                self.end_turn = True


if __name__ == "__main__":
    game = MyGame(DEFAULT_SCREEN_WIDTH + 40, DEFAULT_SCREEN_HEIGHT)
    game.setup()
    arcade.run()
