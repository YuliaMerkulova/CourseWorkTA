import random

from elements.resource_box import ResourceBox
from . import Person, Cat
from .base import BaseEntity
from enums import SpritePosition, KittenStates, PersonStates, Variables, CatStates


class Kitten(BaseEntity):
    def __init__(self, image: str, scaling: float, speed: float = 4):
        super().__init__(image, scaling, speed)
        self.map = {
            SpritePosition.KITTEN_COUCH: [SpritePosition.KITTEN_EAT, SpritePosition.KITTEN_PLAYING_ZONE,
                                          SpritePosition.KITTEN_WITH_MOTHER],
            SpritePosition.KITTEN_EAT: [SpritePosition.KITTEN_COUCH, SpritePosition.KITTEN_PLAYING_ZONE,
                                        SpritePosition.KITTEN_WITH_MOTHER],
            SpritePosition.KITTEN_PLAYING_ZONE: [SpritePosition.KITTEN_COUCH, SpritePosition.KITTEN_EAT,
                                                 SpritePosition.KITTEN_WITH_MOTHER],
            SpritePosition.KITTEN_WITH_MOTHER: [SpritePosition.KITTEN_COUCH, SpritePosition.KITTEN_EAT,
                                                SpritePosition.KITTEN_PLAYING_ZONE]
        }

        self.resources = ResourceBox(box_icon='resources/kitten_sit.png', position=(830, 360), scaling=0.1)
        self.resources.set_resources({
            Variables.SATIETY: dict(icon='resources/food_icon.png', name='Сытость'),
            Variables.ENERGY: dict(icon='resources/sleep_icon.png', name='Энергия'),
            Variables.LOVE: dict(icon='resources/love_icon.png', name='Любовь'),
            Variables.FUN: dict(icon='resources/fun_icon.png', name='Развлечение')
        })
        self.resources.set_resource_value(Variables.SATIETY, 0.5)
        self.current_state = KittenStates.SLEEPING

    def decide_what_do_next(self, person: Person, cat: Cat):
        # у котенка быстро будут уменьшатся все параметры. любовь, еда, сон, развлечение
        # необходимо ввести "преимущуства". сначала пытаемся выполнить самую важную нашу потребность
        # самое важное еда, сон, любовь, развлечение
        print("KITTEN PERSON CAN FEED?", person.ready_to_feed())
        print("KITTEN PERSON CAN PLAY?", person.ready_to_play_with_kitten())
        if self.resources.get_resource_value(Variables.SATIETY) <= 0.4 and person.ready_to_feed() and not person.busy() and person.has_food():
            self.next_position = SpritePosition.KITTEN_EAT
            person.next_position = SpritePosition.PERSON_ANIMAL_FOOD
            self.current_state = KittenStates.EATING
            person.current_state = PersonStates.FEEDING
            person.has_called = True
        elif self.resources.get_resource_value(Variables.ENERGY) <= 0.4:
            self.next_position = SpritePosition.KITTEN_COUCH
            self.current_state = KittenStates.SLEEPING
        elif self.resources.get_resource_value(Variables.FUN) <= 0.3 and person.ready_to_play_with_kitten() and not person.busy():
            self.next_position = SpritePosition.KITTEN_PLAYING_ZONE
            person.next_position = SpritePosition.PERSON_PLAYING_ZONE
            self.current_state = KittenStates.PLAYING_WITH_OWNER
            person.current_state = PersonStates.PLAYING_WITH_KITTEN
            person.has_called = True
        elif self.resources.get_resource_value(Variables.LOVE) <= 0.3 or self.resources.get_resource_value(Variables.FUN) <= 0.3:
            self.next_position = SpritePosition.KITTEN_WITH_MOTHER
            cat.next_position = SpritePosition.CAT_WITH_KITTEN
            self.current_state = KittenStates.WITH_MOTHER
            cat.current_state = CatStates.WITH_KITTEN
            cat.has_called = True
        else:
            self.next_position = random.choice([SpritePosition.KITTEN_COUCH, SpritePosition.KITTEN_WITH_MOTHER,
                                                SpritePosition.KITTEN_EAT, SpritePosition.KITTEN_PLAYING_ZONE])
            self.current_state = KittenStates.SEARCHING

    def update_indicators(self, person: Person):
        if self.current_state == KittenStates.EATING:
            self.resources.set_resource_value(Variables.SATIETY, 1)
            if self.resources.get_resource_value(Variables.ENERGY) >= 0.1:
                self.resources.set_resource_value(Variables.ENERGY, change=-0.1)
            if self.resources.get_resource_value(Variables.LOVE) >= 0.1:
                self.resources.set_resource_value(Variables.LOVE, change=-0.1)
            if self.resources.get_resource_value(Variables.FUN) >= 0.25:
                self.resources.set_resource_value(Variables.FUN, change=-0.25)
            person.resources.set_resource_value(Variables.PRODUCTS, change=-0.1)

        if self.current_state == KittenStates.SLEEPING:
            if self.resources.get_resource_value(Variables.SATIETY) >= 0.2:
                self.resources.set_resource_value(Variables.SATIETY, change=-0.2)
            self.resources.set_resource_value(Variables.ENERGY, 1)
            if self.resources.get_resource_value(Variables.LOVE) >= 0.1:
                self.resources.set_resource_value(Variables.LOVE, change=-0.1)
            if self.resources.get_resource_value(Variables.FUN) >= 0.25:
                self.resources.set_resource_value(Variables.FUN, change=-0.25)

        if self.current_state == KittenStates.PLAYING_WITH_OWNER:
            if self.resources.get_resource_value(Variables.SATIETY) >= 0.2:
                self.resources.set_resource_value(Variables.SATIETY, change=-0.2)
            if self.resources.get_resource_value(Variables.ENERGY) >= 0.1:
                self.resources.set_resource_value(Variables.ENERGY, change=-0.1)
            if self.resources.get_resource_value(Variables.LOVE) >= 0.1:
                self.resources.set_resource_value(Variables.LOVE, change=-0.1)
            self.resources.set_resource_value(Variables.FUN, 1)

        if self.current_state in [KittenStates.SEARCHING, KittenStates.SUNBEAM]:
            if self.resources.get_resource_value(Variables.SATIETY) >= 0.2:
                self.resources.set_resource_value(Variables.SATIETY, change=-0.2)
            else:
                self.resources.set_resource_value(Variables.SATIETY, value=0)
            if self.resources.get_resource_value(Variables.ENERGY) >= 0.1:
                self.resources.set_resource_value(Variables.ENERGY, change=-0.1)
            if self.resources.get_resource_value(Variables.LOVE) >= 0.1:
                self.resources.set_resource_value(Variables.LOVE, change=-0.1)
            if self.resources.get_resource_value(Variables.FUN) >= 0.05:
                self.resources.set_resource_value(Variables.FUN, change=-0.05)
            else:
                self.resources.set_resource_value(Variables.FUN, 0)

        if self.current_state == KittenStates.WITH_MOTHER:
            if self.resources.get_resource_value(Variables.SATIETY) >= 0.2:
                self.resources.set_resource_value(Variables.SATIETY, change=-0.2)
            if self.resources.get_resource_value(Variables.ENERGY) >= 0.1:
                self.resources.set_resource_value(Variables.ENERGY, change=-0.1)
            self.resources.set_resource_value(Variables.LOVE, 1)
            if self.resources.get_resource_value(Variables.FUN) >= 0.25:
                self.resources.set_resource_value(Variables.FUN, change=-0.25)
