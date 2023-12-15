from typing import Tuple

import arcade
from arcade import SpriteList

from elements import IndicatorBar


class Resource:
    FONT_SIZE = 10

    def __init__(self, icon: str, name: str, position: Tuple[float, float], sprite_list: SpriteList,
                 scaling: float = 0.07):
        # TODO: добавить max value и управлять значением в заданном диапазоне
        self.icon_texture = arcade.load_texture(icon)
        self.scaling = scaling
        self.position = position
        self.resource_name = name
        self.indicator = IndicatorBar(sprite_list, (self.position[0] + 70, self.position[1]))
        self._value = 100

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, new_value: float) -> None:
        if not 0 <= new_value <= 100:
            raise ValueError(f"Resource value must be between 0 and 100, got {new_value}")
        self._value = new_value
        self.indicator.fullness = new_value / 100

    def draw(self):
        arcade.draw_scaled_texture_rectangle(self.position[0], self.position[1], self.icon_texture, self.scaling)
        arcade.draw_text(self.resource_name, self.position[0] + 20, self.position[1] - 20, arcade.color.BLACK,
                         Resource.FONT_SIZE)
        arcade.draw_text(self.value, self.position[0] + 90, self.position[1] - 20, arcade.color.BLACK,
                         Resource.FONT_SIZE)
