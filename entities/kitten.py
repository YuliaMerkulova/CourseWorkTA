import random

from . import Person
from .base import BaseEntity
from elements import IndicatorBar
from arcade import SpriteList
from enums import SpritePosition, KittenStates, PersonStates, KittenPositions


class Kitten(BaseEntity):
    def __init__(self, image: str, scaling: float, speed: float = 4):
        super().__init__(image, scaling, speed)
        self.map = {
            KittenPositions.KITTEN_COUCH: [KittenPositions.KITTEN_EAT, KittenPositions.KITTEN_PLAYING_ZONE,
                                           KittenPositions.KITTEN_WITH_MOTHER],
            KittenPositions.KITTEN_EAT: [KittenPositions.KITTEN_COUCH, KittenPositions.KITTEN_PLAYING_ZONE,
                                         KittenPositions.KITTEN_WITH_MOTHER],
            KittenPositions.KITTEN_PLAYING_ZONE: [KittenPositions.KITTEN_COUCH, KittenPositions.KITTEN_EAT,
                                                  KittenPositions.KITTEN_WITH_MOTHER],
            KittenPositions.KITTEN_WITH_MOTHER: [KittenPositions.KITTEN_COUCH, KittenPositions.KITTEN_EAT,
                                                 KittenPositions.KITTEN_PLAYING_ZONE]
        }
        self.hunger_indicator = IndicatorBar(SpriteList(), (940, 370))
        self.hunger_indicator.fullness = 0.1
        self.energy_indicator = IndicatorBar(SpriteList(), (940, 340))
        self.love_indicator = IndicatorBar(SpriteList(), (940, 310))
        self.fun_indicator = IndicatorBar(SpriteList(), (940, 280))
        self.indicators = [self.hunger_indicator, self.energy_indicator, self.love_indicator, self.fun_indicator]
        self.current_state = KittenStates.SLEEPING

    def decide_what_do_next(self, person: Person):
        # у котенка быстро будут уменьшатся все параметры. любовь, еда, сон, развлечение
        # необходимо ввести "преимущуства". сначала пытаемся выполнить самую важную нашу потребность
        # самое важное еда, сон, любовь, развлечение
        if self.hunger_indicator.fullness <= 0.2 and person.get_state() not in [PersonStates.WORKING,
                                                                                PersonStates.BUYING_PRODUCTS]:
            self.next_position = KittenPositions.KITTEN_EAT
            person.next_position = SpritePosition.ANIMAL_FOOD
            self.current_state = KittenStates.EATING
            person.current_state = PersonStates.FEEDING_KITTEN
        elif self.energy_indicator.fullness <= 0.2:
            self.next_position = KittenPositions.KITTEN_COUCH
            self.current_state = KittenStates.SLEEPING
        elif self.fun_indicator.fullness <= 0.1 and person.get_state() not in [PersonStates.WORKING,
                                                                               PersonStates.BUYING_PRODUCTS]:
            self.next_position = KittenPositions.KITTEN_PLAYING_ZONE
            person.next_position = SpritePosition.PLAYING_ZONE
            self.current_state = KittenStates.PLAYING_WITH_OWNER
            person.current_state = PersonStates.PLAYING_WITH_KITTEN
        else:
            self.next_position = random.choice(list(KittenPositions))
            self.current_state = KittenStates.SEARCHING

    def update_indicators(self, person: Person):
        if self.current_state == KittenStates.EATING:
            self.hunger_indicator.fullness = 1
            if self.energy_indicator.fullness >= 0.1:
                self.energy_indicator.fullness -= 0.1
            if self.love_indicator.fullness >= 0.1:
                self.love_indicator.fullness -= 0.1
            if self.fun_indicator.fullness >= 0.1:
                self.fun_indicator.fullness -= 0.25
            person.products_indicator.fullness -= 0.1

        if self.current_state == KittenStates.SLEEPING:
            if self.hunger_indicator.fullness >= 0.1:
                self.hunger_indicator.fullness -= 0.2
            self.energy_indicator.fullness = 1
            if self.love_indicator.fullness >= 0.1:
                self.love_indicator.fullness -= 0.1
            if self.fun_indicator.fullness >= 0.1:
                self.fun_indicator.fullness -= 0.25

        if self.current_state == KittenStates.PLAYING_WITH_OWNER:
            if self.hunger_indicator.fullness >= 0.1:
                self.hunger_indicator.fullness -= 0.2
            if self.energy_indicator.fullness >= 0.1:
                self.energy_indicator.fullness -= 0.1
            if self.love_indicator.fullness >= 0.1:
                self.love_indicator.fullness -= 0.1
            self.fun_indicator.fullness = 1

        if self.current_state in [KittenStates.SEARCHING, KittenStates.SUNBEAM]:
            if self.hunger_indicator.fullness >= 0.1:
                self.hunger_indicator.fullness -= 0.2
            if self.energy_indicator.fullness >= 0.1:
                self.energy_indicator.fullness -= 0.1
            if self.love_indicator.fullness >= 0.1:
                self.love_indicator.fullness -= 0.1
            if self.fun_indicator.fullness >= 0.1:
                self.fun_indicator.fullness -= 0.25

        if self.current_state == KittenStates.WITH_MOTHER:
            if self.hunger_indicator.fullness >= 0.1:
                self.hunger_indicator.fullness -= 0.2
            if self.energy_indicator.fullness >= 0.1:
                self.energy_indicator.fullness -= 0.1
            self.love_indicator.fullness = 1
            if self.fun_indicator.fullness >= 0.1:
                self.fun_indicator.fullness -= 0.25
