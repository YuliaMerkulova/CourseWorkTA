from elements.resource_box import ResourceBox
from enums import Variables, SpritePosition, CatStates, PersonStates
from . import Person
from .base import BaseEntity


class Cat(BaseEntity):
    def __init__(self, image: str, scaling: float, speed: float = 3):
        super().__init__(image, scaling, speed)

        self.map = {
            SpritePosition.CAT_COUCH: [SpritePosition.CAT_WITH_KITTEN, SpritePosition.CAT_EAT,
                                       SpritePosition.CAT_PLAYING_ZONE, SpritePosition.CAT_BIRD],
            SpritePosition.CAT_EAT: [SpritePosition.CAT_COUCH, SpritePosition.CAT_PLAYING_ZONE,
                                     SpritePosition.CAT_WITH_KITTEN, SpritePosition.CAT_FRIDGE,
                                     SpritePosition.CAT_BIRD],
            SpritePosition.CAT_PLAYING_ZONE: [SpritePosition.CAT_COUCH, SpritePosition.CAT_WITH_KITTEN,
                                              SpritePosition.CAT_EAT, SpritePosition.CAT_BIRD],
            SpritePosition.CAT_WITH_KITTEN: [SpritePosition.CAT_COUCH, SpritePosition.CAT_PLAYING_ZONE,
                                             SpritePosition.CAT_EAT, SpritePosition.CAT_BIRD],
            SpritePosition.CAT_FRIDGE: [SpritePosition.CAT_EAT, SpritePosition.CAT_WINDOW],
            SpritePosition.CAT_WINDOW: [SpritePosition.CAT_FRIDGE],
            SpritePosition.CAT_BIRD: [SpritePosition.CAT_COUCH, SpritePosition.CAT_PLAYING_ZONE,
                                      SpritePosition.CAT_WITH_KITTEN,
                                      SpritePosition.CAT_EAT]
        }

        self.resources = ResourceBox(box_icon='resources/cat_sit.png', position=(830, 210), scaling=0.1)
        self.resources.set_resources({
            Variables.SATIETY: dict(icon='resources/food_icon.png', name='Сытость'),
            Variables.ENERGY: dict(icon='resources/sleep_icon.png', name='Энергия'),
            Variables.FUN: dict(icon='resources/fun_icon.png', name='Развлечение')
        })
        self.resources.set_resource_value(Variables.SATIETY, 0.5)
        self.has_called = False

    def update_indicators(self, person):
        if self.current_state == CatStates.EATING:
            self.resources.set_resource_value(Variables.SATIETY, 1)
            if self.resources.get_resource_value(Variables.ENERGY) >= 0.1:
                self.resources.set_resource_value(Variables.ENERGY, change=-0.1)
            if self.resources.get_resource_value(Variables.FUN) >= 0.25:
                self.resources.set_resource_value(Variables.FUN, change=-0.25)
            person.resources.set_resource_value(Variables.PRODUCTS, change=-0.1)

        if self.current_state == CatStates.SLEEPING:
            if self.resources.get_resource_value(Variables.SATIETY) >= 0.2:
                self.resources.set_resource_value(Variables.SATIETY, change=-0.2)
            self.resources.set_resource_value(Variables.ENERGY, 1)
            if self.resources.get_resource_value(Variables.FUN) >= 0.25:
                self.resources.set_resource_value(Variables.FUN, change=-0.25)

        if self.current_state == CatStates.PLAYING_WITH_OWNER:
            if self.resources.get_resource_value(Variables.SATIETY) >= 0.2:
                self.resources.set_resource_value(Variables.SATIETY, change=-0.2)
            if self.resources.get_resource_value(Variables.ENERGY) >= 0.1:
                self.resources.set_resource_value(Variables.ENERGY, change=-0.1)
            self.resources.set_resource_value(Variables.FUN, 1)

        if self.current_state in [CatStates.WATCHING_WINDOW, CatStates.CATCHING_BIRD]:
            if self.resources.get_resource_value(Variables.SATIETY) >= 0.2:
                self.resources.set_resource_value(Variables.SATIETY, change=-0.2)
            else:
                self.resources.set_resource_value(Variables.SATIETY, value=0)
            if self.resources.get_resource_value(Variables.ENERGY) >= 0.1:
                self.resources.set_resource_value(Variables.ENERGY, change=-0.1)
            if self.resources.get_resource_value(Variables.FUN) >= 0.05:
                self.resources.set_resource_value(Variables.FUN, change=-0.05)
            else:
                self.resources.set_resource_value(Variables.FUN, 0)

        if self.current_state == CatStates.WITH_KITTEN:
            if self.resources.get_resource_value(Variables.SATIETY) >= 0.2:
                self.resources.set_resource_value(Variables.SATIETY, change=-0.2)
            if self.resources.get_resource_value(Variables.ENERGY) >= 0.1:
                self.resources.set_resource_value(Variables.ENERGY, change=-0.1)
            if self.resources.get_resource_value(Variables.FUN) <= 0.75:
                self.resources.set_resource_value(Variables.FUN, change=0.25)
            else :
                self.resources.set_resource_value(Variables.FUN, value=1)

    def decide_what_do_next(self, person: Person):
        print("CAT PERSON CAN FEED?", person.ready_to_feed())
        print("CAT PERSON CAN PLAY?", person.ready_to_play_with_cat())
        if not self.has_called and self.resources.get_resource_value(
                Variables.SATIETY) <= 0.4 and person.ready_to_feed() and not person.busy() and person.has_food():
            self.next_position = SpritePosition.CAT_EAT
            person.next_position = SpritePosition.PERSON_ANIMAL_FOOD
            self.current_state = CatStates.EATING
            person.current_state = PersonStates.FEEDING
            person.has_called = True
        elif not self.has_called and self.resources.get_resource_value(Variables.ENERGY) <= 0.4:
            self.next_position = SpritePosition.CAT_COUCH
            self.current_state = CatStates.SLEEPING
        elif not self.has_called and self.resources.get_resource_value(
                Variables.FUN) <= 0.3 and person.ready_to_play_with_kitten() and not person.busy():
            self.next_position = SpritePosition.CAT_PLAYING_ZONE
            person.next_position = SpritePosition.PERSON_PLAYING_ZONE
            self.current_state = CatStates.PLAYING_WITH_OWNER
            person.current_state = PersonStates.PLAYING_WITH_KITTEN
            person.has_called = True
        elif not self.has_called:
            self.next_position = SpritePosition.CAT_WINDOW
            print("cat next pos: ", self.next_position)
            self.current_state = CatStates.WATCHING_WINDOW