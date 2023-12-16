import random

from arcade import Sprite

from elements.resource_box import ResourceBox
from enums import Variables, SpritePosition, CatStates, PersonStates
from . import Person
from .base import BaseEntity


class Cat(BaseEntity):
    def __init__(self, image: str, scaling: float, speed: float = 4):
        super().__init__(image, scaling, speed)

        self.map = {
            SpritePosition.CAT_COUCH: [SpritePosition.CAT_WITH_KITTEN, SpritePosition.CAT_EAT,
                                       SpritePosition.CAT_PLAYING_ZONE],
            SpritePosition.CAT_EAT: [SpritePosition.CAT_COUCH, SpritePosition.CAT_PLAYING_ZONE,
                                     SpritePosition.CAT_WITH_KITTEN, SpritePosition.CAT_FRIDGE],
            SpritePosition.CAT_PLAYING_ZONE: [SpritePosition.CAT_COUCH, SpritePosition.CAT_WITH_KITTEN,
                                              SpritePosition.CAT_EAT],
            SpritePosition.CAT_WITH_KITTEN: [SpritePosition.CAT_COUCH, SpritePosition.CAT_PLAYING_ZONE,
                                             SpritePosition.CAT_EAT],
            SpritePosition.CAT_FRIDGE: [SpritePosition.CAT_EAT, SpritePosition.CAT_WINDOW],
            SpritePosition.CAT_WINDOW: [SpritePosition.CAT_FRIDGE]
        }

        self.resources = ResourceBox(box_icon='resources/cat_sit.png', position=(830, 130), scaling=0.1)
        self.resources.set_resources({
            Variables.SATIETY: dict(icon='resources/food_icon.png', name='Сытость'),
            Variables.ENERGY: dict(icon='resources/sleep_icon.png', name='Энергия'),
            Variables.FUN: dict(icon='resources/fun_icon.png', name='Радость')
        })
        self.resources.set_resource_value(Variables.SATIETY, 50)
        self.current_state = CatStates.SLEEPING
        self.has_called = False

        self.mouse = Sprite('resources/mouse.png', scale=0.1)
        self.mouse.visible = False

    def draw(self):
        super().draw()
        if self.mouse.visible:
            self.mouse.draw()

    def update_indicators(self, person):
        if self.current_state == CatStates.EATING:
            self.resources.set_resource_value(Variables.SATIETY, 100)
            if self.resources.get_resource_value(Variables.ENERGY) >= 10:
                self.resources.set_resource_value(Variables.ENERGY, change=-10)
            if self.resources.get_resource_value(Variables.FUN) >= 25:
                self.resources.set_resource_value(Variables.FUN, change=-25)
            person.resources.set_resource_value(Variables.PRODUCTS, change=-10)
            return
        if self.current_state == CatStates.SLEEPING:
            if self.resources.get_resource_value(Variables.SATIETY) >= 20:
                self.resources.set_resource_value(Variables.SATIETY, change=-20)
            self.resources.set_resource_value(Variables.ENERGY, 100)
            if self.resources.get_resource_value(Variables.FUN) >= 25:
                self.resources.set_resource_value(Variables.FUN, change=-25)
            return
        if self.current_state == CatStates.PLAYING_WITH_OWNER:
            if self.resources.get_resource_value(Variables.SATIETY) >= 20:
                self.resources.set_resource_value(Variables.SATIETY, change=-20)
            if self.resources.get_resource_value(Variables.ENERGY) >= 10:
                self.resources.set_resource_value(Variables.ENERGY, change=-10)
            self.resources.set_resource_value(Variables.FUN, 100)
            return
        if self.current_state in [CatStates.WATCHING_WINDOW, CatStates.CATCHING_MOUSE]:
            if self.resources.get_resource_value(Variables.SATIETY) >= 20:
                self.resources.set_resource_value(Variables.SATIETY, change=-20)
            else:
                self.resources.set_resource_value(Variables.SATIETY, value=0)
            if self.resources.get_resource_value(Variables.ENERGY) >= 10:
                self.resources.set_resource_value(Variables.ENERGY, change=-10)
            if self.resources.get_resource_value(Variables.FUN) >= 5:
                # TODO: Тут надо делать + наверное, иначе веселье в 0 уходит. Ну и 5 как-то мало
                self.resources.set_resource_value(Variables.FUN, change=-5)
            else:
                self.resources.set_resource_value(Variables.FUN, 0)
            return
        if self.current_state == CatStates.WITH_KITTEN:
            if self.resources.get_resource_value(Variables.SATIETY) >= 20:
                self.resources.set_resource_value(Variables.SATIETY, change=-20)
            if self.resources.get_resource_value(Variables.ENERGY) >= 10:
                self.resources.set_resource_value(Variables.ENERGY, change=-10)
            if self.resources.get_resource_value(Variables.FUN) <= 75:
                self.resources.set_resource_value(Variables.FUN, change=25)
            else:
                self.resources.set_resource_value(Variables.FUN, value=100)

    def decide_what_do_next(self, person: Person):
        print("CAT PERSON CAN FEED?", person.ready_to_feed())
        print("CAT PERSON CAN PLAY?", person.ready_to_play_with_cat())
        if person.has_called and person.current_state == PersonStates.FEEDING:
            return
        if random.randint(1, 10) >= 8 and self.current_state != CatStates.WATCHING_WINDOW:
            # TODO: Юле провалидировать условие + поправить свой граф
            self.current_state = CatStates.CATCHING_MOUSE
            self.mouse.position = (random.randint(176, 456), random.randint(160, 270)) if random.randint(0, 1) else \
                (random.randint(389, 629), random.randint(88, 220))
            self.mouse.visible = True
            self.sprite.destination_point = (self.mouse.position[0] +
                                             (-50 if self.mouse.position[0] > self.sprite.position[0] else 50),
                                             self.mouse.position[1])
        elif not self.has_called and self.resources.get_resource_value(
                Variables.SATIETY) <= 40 and person.ready_to_feed() and not person.busy() and person.has_food():
            self.next_position = SpritePosition.CAT_EAT
            person.next_position = SpritePosition.PERSON_ANIMAL_FOOD
            self.current_state = CatStates.EATING
            person.current_state = PersonStates.FEEDING
            person.has_called = True
        elif not self.has_called and self.resources.get_resource_value(Variables.ENERGY) <= 40:
            self.next_position = SpritePosition.CAT_COUCH
            self.current_state = CatStates.SLEEPING
        elif not self.has_called and self.resources.get_resource_value(
                Variables.FUN) <= 30 and person.ready_to_play_with_kitten() and not person.busy():
            self.next_position = SpritePosition.CAT_PLAYING_ZONE
            person.next_position = SpritePosition.PERSON_PLAYING_ZONE
            self.current_state = CatStates.PLAYING_WITH_OWNER
            person.current_state = PersonStates.PLAYING_WITH_KITTEN
            person.has_called = True
        elif not self.has_called:
            self.next_position = SpritePosition.CAT_WINDOW
            print("cat next pos: ", self.next_position)
            self.current_state = CatStates.WATCHING_WINDOW
