import arcade
from pyglet.math import Vec2

from entities.person import Person
from enums import SpritePosition

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
        self.positions = [SpritePosition.DOOR, SpritePosition.FRIDGE, SpritePosition.PLAYING_ZONE]

    def setup(self):
        self.person = Person(image="resources/person.png", scaling=0.11)
        self.person.set_position(SpritePosition.BED)

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.person.sprite)
        self.background = arcade.load_texture("resources/background.png")

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, self.background)
        arcade.draw_rectangle_filled(905, DEFAULT_SCREEN_HEIGHT // 2, 190, DEFAULT_SCREEN_HEIGHT,
                                     arcade.color.LIGHT_GRAY)
        arcade.draw_scaled_texture_rectangle(830, 510, arcade.load_texture("resources/person_icon.png"), 0.2)

        # arcade.draw_text("draw_filled_rect", 363, 3, arcade.color.BLACK, 10)
        self.player_list.draw()
        self.person.hunger_indicator.sprite_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        # print(x, y)
        position = Vec2(x - self.width / 2, y - self.height / 2)
        # self.camera.move_to(position, CAMERA_SPEED)

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            print(self.person.sprite.angle) # 260
            print(f"click: {x}, {y}")
            # self.person.move_to(SpritePosition.FRIDGE)
            self.person.sprite.destination_point = x, y
        elif button == arcade.MOUSE_BUTTON_LEFT:
            if not len(self.positions):
                return
            new_point = self.positions[0]
            if len(self.positions) != 1:
                self.positions = self.positions[1:]
            else:
                self.positions = []
            self.person.set_path(self.person.find_path(self.person.get_position(), new_point))

    def update(self, delta_time):
        self.player_list.on_update()
        # self.owner.change_x += 1
        # self.owner.update()


if __name__ == "__main__":
    game = MyGame(DEFAULT_SCREEN_WIDTH + 40, DEFAULT_SCREEN_HEIGHT)
    game.setup()
    arcade.run()
