import arcade
from pyglet.math import Vec2

from elements.turn_model import Turn
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
        self.turn = Turn('resources/turn.png', 0.01, (50, 50))
        self.end_turn = False
        self.timer = 0

    def setup(self):
        self.background = arcade.load_texture("resources/background.png")
        self.person = Person(image="resources/person.png", scaling=0.11)
        self.person.set_position(SpritePosition.PERSON_BED)
        self.person.lie_on_bed()
        self.kitten = Kitten(image="resources/kitten_stand.png", scaling=0.09)
        self.kitten.set_position(SpritePosition.KITTEN_COUCH)
        self.cat = Cat(image="resources/cat_stand.png", scaling=0.11)
        self.cat.set_position(SpritePosition.CAT_COUCH)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, self.background)
        arcade.draw_rectangle_filled(910, DEFAULT_SCREEN_HEIGHT // 2, 200, DEFAULT_SCREEN_HEIGHT,
                                     arcade.color.LIGHT_GRAY)
        self.person.draw()
        self.kitten.draw()
        self.cat.draw()
        self.turn.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            print(f"click: {x}, {y}")
            # self.kitten.sprite.destination_point = x, y
        elif button == arcade.MOUSE_BUTTON_LEFT and not self.turn.visible:
            self.kitten.decide_what_do_next(person=self.person, cat=self.cat)
            self.cat.decide_what_do_next(self.person)
            self.person.decide_what_do_next()
            print("CURRENT PERSON STATE: ", self.person.current_state)
            print("CURRENT KITTEN STATE: ", self.kitten.current_state)
            print("CURRENT CAT STATE: ", self.cat.current_state)
            print("NEXT KITTEN POSITION: ", self.kitten.next_position)
            print("NEXT PERSON POSITION: ", self.person.next_position)
            print("NEXT CAT POSITION: ", self.cat.next_position)
            if not self.kitten.running_for_beam:
                self.kitten.move_to(self.kitten.next_position)
            self.person.move_to(self.person.next_position)
            if not self.cat.mouse.visible:
                self.cat.move_to(self.cat.next_position)
            self.turn.start()

    def update(self, delta_time):
        if self.turn.visible:
            self.turn.update()

        if self.end_turn:
            self.timer += 1
            if self.timer == 30:
                print("dest points: ", self.person.sprite.destination_point, self.kitten.sprite.destination_point)
                self.end_turn = False
                self.turn.visible = False
                self.timer = 0
                self.kitten.update_indicators(self.person)
                self.person.update_indicators(self.person)
                self.cat.update_indicators(self.person)
                self.kitten.running_for_beam = None
                self.cat.mouse.visible = False
                self.kitten.next_position = None
                self.person.has_called = False
                self.cat.has_called = False
            return

        self.person.update()
        self.kitten.update()
        self.cat.update()

        if self.person.next_position is not None and self.kitten.next_position is not None and \
                self.kitten.next_position is not None or self.kitten.running_for_beam is not None:
            if not self.person.is_moving() and not self.kitten.is_moving() and not self.cat.is_moving():
                self.end_turn = True


if __name__ == "__main__":
    game = MyGame(DEFAULT_SCREEN_WIDTH + 50, DEFAULT_SCREEN_HEIGHT)
    game.setup()
    arcade.run()
