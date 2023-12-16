from typing import Optional

import arcade

from entities.base import BaseSprite
from enums import FaceSide


class PositionState:
    def __init__(self, image: Optional[str] = None, scaling: Optional[float] = None, angle: Optional[int] = None,
                 visible: bool = True, face: Optional[FaceSide] = None):
        self.texture = None if image is None else arcade.load_texture(image)
        self.scaling = scaling
        self.angle = angle
        self.visible = visible
        self.face = face

    def set_state(self, sprite: BaseSprite):
        if self.texture is not None:
            sprite.texture = self.texture
        if self.scaling is not None:
            sprite.scale = self.scaling
        if self.angle is not None:
            sprite.angle = self.angle
        if self.face is not None:
            sprite.face_direction = self.face
        sprite.visible = self.visible
