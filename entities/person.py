from enums import SpritePosition
from .base import BaseEntity


class Person(BaseEntity):
    def __init__(self, image: str, scaling: float, speed: float = 3):
        super().__init__(image, scaling, speed)
        self.map = {
            SpritePosition.DOOR: [SpritePosition.ADD_WINDOW, SpritePosition.ADD_TABLE_CORNER, SpritePosition.TABLE],
            SpritePosition.ADD_WINDOW: [SpritePosition.DOOR, SpritePosition.ADD_TABLE_CORNER, SpritePosition.FRIDGE],
            SpritePosition.ADD_TABLE_CORNER: [SpritePosition.ADD_WINDOW, SpritePosition.DOOR, SpritePosition.TABLE],
            SpritePosition.FRIDGE: [SpritePosition.ADD_WINDOW, SpritePosition.ANIMAL_FOOD],
            SpritePosition.TABLE: [SpritePosition.ADD_TABLE_CORNER, SpritePosition.ADD_CENTER, SpritePosition.DOOR],
            SpritePosition.ANIMAL_FOOD: [SpritePosition.FRIDGE, SpritePosition.ADD_CENTER],
            SpritePosition.ADD_CENTER: [SpritePosition.TABLE, SpritePosition.ADD_ROOM_DOOR, SpritePosition.PLAYING_ZONE,
                                        SpritePosition.ANIMAL_FOOD],
            SpritePosition.PLAYING_ZONE: [SpritePosition.ADD_CENTER, SpritePosition.ADD_ROOM_DOOR],
            SpritePosition.ADD_ROOM_DOOR: [SpritePosition.PLAYING_ZONE, SpritePosition.ADD_CENTER, SpritePosition.BED],
            SpritePosition.BED: [SpritePosition.ADD_ROOM_DOOR]
        }
