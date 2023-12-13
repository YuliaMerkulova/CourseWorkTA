import time

import arcade
from pyglet.math import Vec2

from entities.person import Person
from entities.kitten import Kitten
from entities.cat import Cat
from enums import SpritePosition, KittenStates, PersonStates, KittenPositions

DEFAULT_SCREEN_WIDTH = 960
DEFAULT_SCREEN_HEIGHT = 540
SPRITE_SCALING = 0.3


class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.background = None
        self.player_list = None
        self.person = None
        self.cat = None
        self.kitten = None
        self.positions_kitten = [KittenPositions.KITTEN_EAT, KittenPositions.KITTEN_WITH_MOTHER, KittenPositions.KITTEN_PLAYING_ZONE]

    def setup(self):
        self.person = Person(image="resources/person.png", scaling=0.11)
        self.person.set_position(SpritePosition.BED)
        self.kitten = Kitten(image="resources/kitten_stand.png", scaling=0.09)
        self.kitten.set_position(KittenPositions.KITTEN_COUCH)
        self.cat = Cat(image="resources/cat_stand.png", scaling=0.11)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.person.sprite)
        self.player_list.append(self.kitten.sprite)
        self.background = arcade.load_texture("resources/background.png")

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, self.background)
        arcade.draw_rectangle_filled(905, DEFAULT_SCREEN_HEIGHT // 2, 190, DEFAULT_SCREEN_HEIGHT,
                                     arcade.color.LIGHT_GRAY)
        arcade.draw_scaled_texture_rectangle(830, 510, arcade.load_texture("resources/person_icon.png"), 0.2)
        arcade.draw_scaled_texture_rectangle(870, 520, arcade.load_texture("resources/food_icon.png"), 0.07)
        arcade.draw_scaled_texture_rectangle(870, 490, arcade.load_texture("resources/sleep_icon.png"), 0.07)
        arcade.draw_scaled_texture_rectangle(870, 460, arcade.load_texture("resources/money_icon.png"), 0.07)
        arcade.draw_scaled_texture_rectangle(870, 430, arcade.load_texture("resources/products_icon.png"), 0.07)

        arcade.draw_scaled_texture_rectangle(830, 360, arcade.load_texture("resources/kitten_sit.png"), 0.1)
        arcade.draw_scaled_texture_rectangle(870, 370, arcade.load_texture("resources/food_icon.png"), 0.07)
        arcade.draw_scaled_texture_rectangle(870, 340, arcade.load_texture("resources/sleep_icon.png"), 0.07)
        arcade.draw_scaled_texture_rectangle(870, 310, arcade.load_texture("resources/love_icon.png"), 0.07)
        arcade.draw_scaled_texture_rectangle(870, 280, arcade.load_texture("resources/fun_icon.png"), 0.07)

        arcade.draw_scaled_texture_rectangle(830, 210, arcade.load_texture("resources/cat_sit.png"), 0.1)
        arcade.draw_scaled_texture_rectangle(870, 220, arcade.load_texture("resources/food_icon.png"), 0.07)
        arcade.draw_scaled_texture_rectangle(870, 190, arcade.load_texture("resources/sleep_icon.png"), 0.07)
        arcade.draw_scaled_texture_rectangle(870, 160, arcade.load_texture("resources/fun_icon.png"), 0.07)
        # arcade.draw_text("draw_filled_rect", 363, 3, arcade.color.BLACK, 10)
        self.player_list.draw()
        self.draw_indicators()

    def draw_indicators(self):
        for indicator in self.person.indicators:
            indicator.sprite_list.draw()
        arcade.draw_text("Еда", 890, 500, arcade.color.BLACK, 10)
        arcade.draw_text("Энергия", 890, 470, arcade.color.BLACK, 10)
        arcade.draw_text("Деньги", 890, 440, arcade.color.BLACK, 10)
        arcade.draw_text("Продукты", 890, 410, arcade.color.BLACK, 10)
        for indicator in self.kitten.indicators:
            indicator.sprite_list.draw()
        arcade.draw_text("Еда", 890, 350, arcade.color.BLACK, 10)
        arcade.draw_text("Энергия", 890, 320, arcade.color.BLACK, 10)
        arcade.draw_text("Любовь", 890, 290, arcade.color.BLACK, 10)
        arcade.draw_text("Развлечение", 890, 260, arcade.color.BLACK, 10)
        for indicator in self.cat.indicators:
            indicator.sprite_list.draw()
        arcade.draw_text("Еда", 890, 200, arcade.color.BLACK, 10)
        arcade.draw_text("Энергия", 890, 170, arcade.color.BLACK, 10)
        arcade.draw_text("Развлечение", 890, 140, arcade.color.BLACK, 10)


    def on_mouse_motion(self, x, y, dx, dy):
        # print(x, y)
        position = Vec2(x - self.width / 2, y - self.height / 2)
        # self.camera.move_to(position, CAMERA_SPEED)

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            print(self.kitten.sprite.angle) # 260
            print(f"click: {x}, {y}")
            # self.person.move_to(SpritePosition.FRIDGE)
            self.kitten.sprite.destination_point = x, y
        elif button == arcade.MOUSE_BUTTON_LEFT:
            self.kitten.decide_what_do_next(person=self.person)
            self.person.decide_what_do_next()
            if not len(self.positions_kitten):
                return
            new_point_kitten = self.kitten.next_position
            print(self.kitten.get_position(), new_point_kitten)
            print(self.kitten.find_path(self.kitten.get_position(), new_point_kitten))
            self.kitten.set_path(self.kitten.find_path(self.kitten.get_position(), new_point_kitten))
            self.person.set_path(self.person.find_path(self.person.get_position(), self.person.next_position))

    def update(self, delta_time):
        self.player_list.on_update()
        if self.person.next_position is not None and self.kitten.next_position is not None:
            if not self.person.sprite.destination_point and not self.kitten.sprite.destination_point:
                print("HURRAY")
                time.sleep(1)
                self.kitten.update_indicators(self.person)
                self.person.update_indicators(self.person)
                self.person.current_state = PersonStates.WAITING
                self.person.next_position = None
                self.kitten.next_position = None


if __name__ == "__main__":
    game = MyGame(DEFAULT_SCREEN_WIDTH + 40, DEFAULT_SCREEN_HEIGHT)
    game.setup()
    arcade.run()
