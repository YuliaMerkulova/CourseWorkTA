# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import arcade

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900

class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height)

        self.player_list = None
        self.owner = None
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        # Настроить игру здесь
        # Создать список спрайтов
        self.player_list = arcade.SpriteList()
        SPRITE_SCALING = 0.07
        self.owner = arcade.Sprite("resorses/student.png", SPRITE_SCALING)
        self.owner.center_x = 100
        self.owner.center_y = 300
        self.player_list.append(self.owner)
        pass

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        self.player_list.draw()
        # Здесь код рисунка

    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        pass


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()