from typing import Tuple

import arcade


class IndicatorBar:
    def __init__(self, sprite_list: arcade.SpriteList, position: Tuple[float, float] = (0, 0),
                 full_color: arcade.Color = arcade.color.GREEN, background_color: arcade.Color = arcade.color.BLACK,
                 width: int = 100, height: int = 4, border_size: int = 4) -> None:
        self.sprite_list: arcade.SpriteList = sprite_list

        self._box_width: int = width
        self._box_height: int = height
        self._half_box_width: int = self._box_width // 2
        self._center_x: float = 0.0
        self._center_y: float = 0.0
        self._fullness: float = 0.0

        self._background_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width + border_size,
            self._box_height + border_size,
            background_color,
        )
        self._full_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width,
            self._box_height,
            full_color,
        )
        self.sprite_list.append(self._background_box)
        self.sprite_list.append(self._full_box)

        self.fullness: float = 1.0
        self.position: Tuple[float, float] = position

    @property
    def background_box(self) -> arcade.SpriteSolidColor:
        return self._background_box

    @property
    def full_box(self) -> arcade.SpriteSolidColor:
        return self._full_box

    @property
    def fullness(self) -> float:
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness: float) -> None:
        if not (0.0 <= new_fullness <= 1.0):
            raise ValueError(f"Got {new_fullness}, but fullness must be between 0.0 and 1.0")

        self._fullness = new_fullness
        if new_fullness == 0.0:
            self.full_box.visible = False
        else:
            self.full_box.visible = True
            self.full_box.width = self._box_width * new_fullness
            self.full_box.left = self._center_x - (self._box_width // 2)

    @property
    def position(self) -> Tuple[float, float]:
        return self._center_x, self._center_y

    @position.setter
    def position(self, new_position: Tuple[float, float]) -> None:
        if new_position != self.position:
            self._center_x, self._center_y = new_position
            self.background_box.position = new_position
            self.full_box.position = new_position

            self.full_box.left = self._center_x - (self._box_width // 2)
