from .base import BaseEntity
from elements import IndicatorBar
from arcade import SpriteList


class Cat(BaseEntity):
    def __init__(self, image: str, scaling: float, speed: float = 3):
        super().__init__(image, scaling, speed)
        self.hunger_indicator = IndicatorBar(SpriteList(), (940, 220))
        self.energy_indicator = IndicatorBar(SpriteList(), (940, 190))
        self.fun_indicator = IndicatorBar(SpriteList(), (940, 160))
        self.indicators = [self.hunger_indicator, self.energy_indicator, self.fun_indicator]
