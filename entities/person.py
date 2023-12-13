import random

from enums import SpritePosition, PersonStates
from .base import BaseEntity
from elements import IndicatorBar
from arcade import SpriteList


class Person(BaseEntity):
    def __init__(self, image: str, scaling: float, speed: float = 5):
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
        self.hunger_indicator = IndicatorBar(SpriteList(), (940, 520))
        self.energy_indicator = IndicatorBar(SpriteList(), (940, 490))
        self.money_indicator = IndicatorBar(SpriteList(), (940, 460))
        self.products_indicator = IndicatorBar(SpriteList(), (940, 430))
        self.products_indicator.fullness = 0.5
        self.indicators = [self.hunger_indicator, self.energy_indicator, self.money_indicator, self.products_indicator]
        self.current_state = PersonStates.WAITING
        self.next_state = None

    def decide_what_do_next(self):
        if self.current_state != PersonStates.WAITING:
            return
        if self.hunger_indicator.fullness <= 0.2:
            self.next_position = SpritePosition.TABLE
            self.current_state = PersonStates.EATING
        elif self.energy_indicator.fullness <= 0.2:
            self.next_position = SpritePosition.BED
            self.current_state = PersonStates.SLEEPING
        elif self.products_indicator.fullness <= 0.2:
            self.next_position = SpritePosition.DOOR
            self.current_state = PersonStates.BUYING_PRODUCTS
        elif self.money_indicator.fullness <= 0.2:
            self.current_state = PersonStates.WORKING
            self.next_position = SpritePosition.DOOR
        else:
            self.current_state = PersonStates.WALKING
            self.next_position = random.choice(list(SpritePosition))

    def update_indicators(self, person):
        if self.current_state == PersonStates.EATING:
            self.hunger_indicator.fullness = 1
            if abs(self.energy_indicator.fullness) >= 0.1:
                self.energy_indicator.fullness -= 0.1
            if abs(self.products_indicator.fullness) >= 0.1:
                self.products_indicator.fullness -= 0.1

        if self.current_state == PersonStates.SLEEPING:
            if self.hunger_indicator.fullness >= 0.1:
                self.hunger_indicator.fullness -= 0.1
            self.energy_indicator.fullness = 1

        if self.current_state == PersonStates.WORKING:
            if self.hunger_indicator.fullness >= 0.1:
                self.hunger_indicator.fullness -= 0.1
            if self.energy_indicator.fullness >= 0.1:
                self.energy_indicator.fullness -= 0.1
            self.money_indicator.fullness = 1

        if self.current_state == PersonStates.BUYING_PRODUCTS:
            if self.hunger_indicator.fullness >= 0.1:
                self.hunger_indicator.fullness -= 0.1
            if self.energy_indicator.fullness >= 0.1:
                self.energy_indicator.fullness -= 0.1
            self.products_indicator.fullness = 1

        if self.current_state in [PersonStates.FEEDING_KITTEN, PersonStates.FEEDING_CAT]:
            if self.hunger_indicator.fullness >= 0.1:
                self.hunger_indicator.fullness -= 0.1
            if self.energy_indicator.fullness >= 0.1:
                self.energy_indicator.fullness -= 0.1
            if self.products_indicator.fullness >= 0.1:
                self.products_indicator.fullness -= 0.1

        if self.current_state in [PersonStates.PLAYING_WITH_CAT, PersonStates.PLAYING_WITH_KITTEN]:
            if self.hunger_indicator.fullness >= 0.1:
                self.hunger_indicator.fullness -= 0.1
            if self.energy_indicator.fullness >= 0.1:
                self.energy_indicator.fullness -= 0.1

        if self.current_state == PersonStates.WALKING:
            if self.hunger_indicator.fullness >= 0.1:
                self.hunger_indicator.fullness -= 0.1
            if self.energy_indicator.fullness >= 0.1:
                self.energy_indicator.fullness -= 0.1
