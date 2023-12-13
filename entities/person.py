import random

from elements.resource_box import ResourceBox
from enums import SpritePosition, PersonStates, SpriteAngle, Variables
from .base import BaseEntity


class Person(BaseEntity):
    def __init__(self, image: str, scaling: float, speed: float = 5):
        super().__init__(image, scaling, speed)
        self.position_angles = {
            SpritePosition.PERSON_BED: SpriteAngle.PERSON_BED
        }
        self.map = {
            SpritePosition.PERSON_DOOR: [SpritePosition.PERSON_ADD_WINDOW, SpritePosition.PERSON_ADD_TABLE_CORNER,
                                         SpritePosition.PERSON_TABLE],
            SpritePosition.PERSON_ADD_WINDOW: [SpritePosition.PERSON_DOOR, SpritePosition.PERSON_ADD_TABLE_CORNER,
                                               SpritePosition.PERSON_FRIDGE],
            SpritePosition.PERSON_ADD_TABLE_CORNER: [SpritePosition.PERSON_ADD_WINDOW, SpritePosition.PERSON_DOOR,
                                                     SpritePosition.PERSON_TABLE],
            SpritePosition.PERSON_FRIDGE: [SpritePosition.PERSON_ADD_WINDOW, SpritePosition.PERSON_ANIMAL_FOOD],
            SpritePosition.PERSON_TABLE: [SpritePosition.PERSON_ADD_TABLE_CORNER, SpritePosition.PERSON_ADD_CENTER,
                                          SpritePosition.PERSON_DOOR],
            SpritePosition.PERSON_ANIMAL_FOOD: [SpritePosition.PERSON_FRIDGE, SpritePosition.PERSON_ADD_CENTER],
            SpritePosition.PERSON_ADD_CENTER: [SpritePosition.PERSON_TABLE, SpritePosition.PERSON_ADD_ROOM_DOOR,
                                               SpritePosition.PERSON_PLAYING_ZONE,
                                               SpritePosition.PERSON_ANIMAL_FOOD],
            SpritePosition.PERSON_PLAYING_ZONE: [SpritePosition.PERSON_ADD_CENTER, SpritePosition.PERSON_ADD_ROOM_DOOR],
            SpritePosition.PERSON_ADD_ROOM_DOOR: [SpritePosition.PERSON_PLAYING_ZONE, SpritePosition.PERSON_ADD_CENTER,
                                                  SpritePosition.PERSON_BED],
            SpritePosition.PERSON_BED: [SpritePosition.PERSON_ADD_ROOM_DOOR]
        }

        self.resources = ResourceBox(box_icon='resources/person_icon.png', position=(830, 510), scaling=0.2)
        self.resources.set_resources({
            Variables.SATIETY: dict(icon='resources/food_icon.png', name='Сытость'),
            Variables.ENERGY: dict(icon='resources/sleep_icon.png', name='Энергия'),
            Variables.MONEY: dict(icon='resources/money_icon.png', name='Деньги'),
            Variables.PRODUCTS: dict(icon='resources/products_icon.png', name='Продукты')
        })

        self.resources.set_resource_value(Variables.PRODUCTS, 0.5)
        self.current_state = PersonStates.WAITING
        self.next_state = None
        self.day = {
            PersonStates.SLEEPING: PersonStates.EATING,
            PersonStates.EATING: [PersonStates.WORKING, PersonStates.FEEDING],
            PersonStates.FEEDING: [PersonStates.WORKING, PersonStates.PLAYING_WITH_CAT,
                                   PersonStates.PLAYING_WITH_KITTEN],
            PersonStates.WORKING: [PersonStates.SLEEPING, PersonStates.BUYING_PRODUCTS,
                                   PersonStates.PLAYING_WITH_KITTEN],
            PersonStates.PLAYING_WITH_KITTEN: [PersonStates.SLEEPING, PersonStates.BUYING_PRODUCTS],
            PersonStates.PLAYING_WITH_CAT: [PersonStates.SLEEPING, PersonStates.BUYING_PRODUCTS],
            PersonStates.BUYING_PRODUCTS: [PersonStates.SLEEPING],
        }

    def ready_to_play_with_cat(self):
        return self.current_state == PersonStates.FEEDING

    def ready_to_play_with_kitten(self):
        return self.current_state == PersonStates.FEEDING or self.current_state == PersonStates.WORKING

    def ready_to_feed(self):
        return self.current_state == PersonStates.EATING

    def lie_on_bed(self):
        self.sprite.angle = SpriteAngle.PERSON_BED.value

    def decide_what_do_next(self):
        if self.current_state != PersonStates.WAITING:
            return
        if self.resources.get_resource_value(Variables.SATIETY) <= 0.2:
            self.next_position = SpritePosition.PERSON_TABLE
            self.current_state = PersonStates.EATING
        elif self.resources.get_resource_value(Variables.ENERGY) <= 0.2:
            self.next_position = SpritePosition.PERSON_BED
            self.current_state = PersonStates.SLEEPING
        elif self.resources.get_resource_value(Variables.PRODUCTS) <= 0.2:
            self.next_position = SpritePosition.PERSON_DOOR
            self.current_state = PersonStates.BUYING_PRODUCTS
        elif self.resources.get_resource_value(Variables.MONEY) <= 0.2:
            self.current_state = PersonStates.WORKING
            self.next_position = SpritePosition.PERSON_DOOR
        else:
            self.current_state = PersonStates.WALKING
            self.next_position = random.choice([SpritePosition.PERSON_DOOR, SpritePosition.PERSON_BED,
                                                SpritePosition.PERSON_FRIDGE])

    def update_indicators(self, person):
        if self.current_state == PersonStates.EATING:
            self.resources.set_resource_value(Variables.SATIETY, 1)
            if abs(self.resources.get_resource_value(Variables.ENERGY)) >= 0.1:
                self.resources.set_resource_value(Variables.ENERGY, change=-0.1)
            if abs(self.resources.get_resource_value(Variables.PRODUCTS)) >= 0.1:
                self.resources.set_resource_value(Variables.PRODUCTS, change=-0.1)

        if self.current_state == PersonStates.SLEEPING:
            if self.resources.get_resource_value(Variables.SATIETY) >= 0.1:
                self.resources.set_resource_value(Variables.SATIETY, change=-0.1)
            self.resources.set_resource_value(Variables.ENERGY, 1)

        if self.current_state == PersonStates.WORKING:
            if self.resources.get_resource_value(Variables.SATIETY) >= 0.1:
                self.resources.set_resource_value(Variables.SATIETY, change=-0.1)
            if self.resources.get_resource_value(Variables.ENERGY) >= 0.1:
                self.resources.set_resource_value(Variables.ENERGY, change=-0.1)
            self.resources.set_resource_value(Variables.MONEY, 1)

        if self.current_state == PersonStates.BUYING_PRODUCTS:
            if self.resources.get_resource_value(Variables.SATIETY) >= 0.1:
                self.resources.set_resource_value(Variables.SATIETY, change=-0.1)
            if self.resources.get_resource_value(Variables.ENERGY) >= 0.1:
                self.resources.set_resource_value(Variables.ENERGY, change=-0.1)
            self.resources.set_resource_value(Variables.PRODUCTS, 1)

        if self.current_state == PersonStates.FEEDING:
            if self.resources.get_resource_value(Variables.SATIETY) >= 0.1:
                self.resources.set_resource_value(Variables.SATIETY, change=-0.1)
            if self.resources.get_resource_value(Variables.ENERGY) >= 0.1:
                self.resources.set_resource_value(Variables.ENERGY, change=-0.1)
            if self.resources.get_resource_value(Variables.PRODUCTS) >= 0.1:
                self.resources.set_resource_value(Variables.PRODUCTS, change=-0.1)

        if self.current_state in [PersonStates.PLAYING_WITH_CAT, PersonStates.PLAYING_WITH_KITTEN]:
            if self.resources.get_resource_value(Variables.SATIETY) >= 0.1:
                self.resources.set_resource_value(Variables.SATIETY, change=-0.1)
            if self.resources.get_resource_value(Variables.ENERGY) >= 0.1:
                self.resources.set_resource_value(Variables.ENERGY, change=-0.1)

        if self.current_state == PersonStates.WALKING:
            if self.resources.get_resource_value(Variables.SATIETY) >= 0.1:
                self.resources.set_resource_value(Variables.SATIETY, change=-0.1)
            if self.resources.get_resource_value(Variables.ENERGY) >= 0.1:
                self.resources.set_resource_value(Variables.ENERGY, change=-0.1)
