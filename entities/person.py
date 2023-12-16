import random

from elements.position_state import PositionState
from elements.resource_box import ResourceBox
from enums import SpritePosition, PersonStates, SpriteAngle, Variables
from .base import BaseEntity


class Person(BaseEntity):
    def __init__(self, image: str, scaling: float, speed: float = 4):
        super().__init__(image, scaling, speed)
        self.sprite.position_states = {
            SpritePosition.PERSON_BED.value: PositionState(angle=SpriteAngle.PERSON_BED.value),
            SpritePosition.PERSON_DOOR.value: PositionState(visible=False),
        }
        self.sprite.set_state(SpritePosition.PERSON_BED.value)
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

        self.resources.set_resource_value(Variables.PRODUCTS, 50)
        self.current_state = PersonStates.SLEEPING
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
        self.resources.set_resource_value(Variables.SATIETY, 20)
        self.resources.set_resource_value(Variables.MONEY, 10)
        self.has_called = False
        self.long_action = 0

    def ready_to_eat(self):
        return self.current_state == PersonStates.SLEEPING

    def ready_to_sleep(self):
        return self.current_state in [PersonStates.WORKING, PersonStates.PLAYING_WITH_KITTEN,
                                      PersonStates.PLAYING_WITH_CAT, PersonStates.BUYING_PRODUCTS,
                                      PersonStates.SLEEPING]

    def ready_to_work(self):
        return self.current_state == PersonStates.EATING or self.current_state == PersonStates.FEEDING

    def ready_to_buy_products(self):
        return self.current_state in [PersonStates.WORKING, PersonStates.PLAYING_WITH_KITTEN,
                                      PersonStates.PLAYING_WITH_CAT]

    def ready_to_play_with_cat(self):
        return self.current_state == PersonStates.FEEDING

    def ready_to_play_with_kitten(self):
        return self.current_state == PersonStates.FEEDING or self.current_state == PersonStates.WORKING

    def ready_to_feed(self):
        return self.current_state == PersonStates.EATING

    def has_food(self):
        return self.resources.get_resource_value(Variables.PRODUCTS) >= 10

    def lie_on_bed(self):
        self.sprite.angle = SpriteAngle.PERSON_BED.value

    def busy(self):
        return self.long_action == 1

    def need_sleep(self):
        return self.resources.get_resource_value(Variables.ENERGY) < 70

    def has_products(self):
        return self.resources.get_resource_value(Variables.PRODUCTS) >= 20

    def has_money(self):
        return self.resources.get_resource_value(Variables.MONEY) >= 20

    def need_products(self):
        return self.resources.get_resource_value(Variables.PRODUCTS) <= 30

    def decide_what_do_next(self):
        if not self.has_called and self.ready_to_buy_products() and self.has_money() and self.need_products():
            self.next_position = SpritePosition.PERSON_DOOR
            self.current_state = PersonStates.BUYING_PRODUCTS
        elif not self.has_called and self.ready_to_sleep() and self.has_food() and self.need_sleep():
            self.next_position = SpritePosition.PERSON_BED
            self.current_state = PersonStates.SLEEPING
        elif not self.has_called and self.ready_to_eat() and self.has_food():
            self.next_position = SpritePosition.PERSON_TABLE
            self.current_state = PersonStates.EATING
        elif self.has_called and self.has_products() and self.ready_to_feed() and self.has_food():
            self.next_position = SpritePosition.PERSON_ANIMAL_FOOD
            self.current_state = PersonStates.FEEDING
        elif not self.has_called and self.ready_to_work() and self.has_called:
            return
        elif not self.has_called and self.ready_to_work():
            self.next_position = SpritePosition.PERSON_DOOR
            self.current_state = PersonStates.WORKING
        # if self.long_action == 1:
        #     self.long_action += 1
        #     self.update_indicators(self)
        #     return
        # if self.long_action == 2:
        #     self.long_action = 0
        # if not self.has_called and self.ready_to_eat() and self.has_food():
        #     self.next_position = SpritePosition.PERSON_TABLE
        #     self.current_state = PersonStates.EATING
        # elif not self.has_called and self.ready_to_buy_products() and \
        #         self.resources.get_resource_value(Variables.PRODUCTS) <= 40:
        #     self.next_position = SpritePosition.PERSON_DOOR
        #     self.current_state = PersonStates.BUYING_PRODUCTS
        #     self.long_action += 1
        # elif not self.has_called and self.ready_to_sleep():
        #     self.next_position = SpritePosition.PERSON_BED
        #     self.current_state = PersonStates.SLEEPING
        # elif not self.has_called and self.ready_to_work():
        #     self.current_state = PersonStates.WORKING
        #     self.next_position = SpritePosition.PERSON_DOOR
        #     self.long_action += 1

    def update_indicators(self, person, *args, **kwargs):
        if self.current_state == PersonStates.EATING:
            self.resources.set_resource_value(Variables.SATIETY, 100)
            if abs(self.resources.get_resource_value(Variables.ENERGY)) >= 10:
                self.resources.set_resource_value(Variables.ENERGY, change=-10)
            if abs(self.resources.get_resource_value(Variables.PRODUCTS)) >= 10:
                self.resources.set_resource_value(Variables.PRODUCTS, change=-10)
            return
        if self.current_state == PersonStates.SLEEPING:
            if self.resources.get_resource_value(Variables.SATIETY) >= 10:
                self.resources.set_resource_value(Variables.SATIETY, change=-10)
            self.resources.set_resource_value(Variables.ENERGY, change=30)
            return
        if self.current_state == PersonStates.WORKING:
            if self.resources.get_resource_value(Variables.SATIETY) >= 10:
                self.resources.set_resource_value(Variables.SATIETY, change=-10)
            if self.resources.get_resource_value(Variables.ENERGY) >= 30:
                self.resources.set_resource_value(Variables.ENERGY, change=-30)
            self.resources.set_resource_value(Variables.MONEY, change=50)
            return
        if self.current_state == PersonStates.BUYING_PRODUCTS:
            if self.resources.get_resource_value(Variables.SATIETY) >= 10:
                self.resources.set_resource_value(Variables.SATIETY, change=-10)
            if self.resources.get_resource_value(Variables.ENERGY) >= 20:
                self.resources.set_resource_value(Variables.ENERGY, change=-20)
            if self.resources.get_resource_value(Variables.MONEY) >= 20:
                self.resources.set_resource_value(Variables.MONEY, change=-20)
            self.resources.set_resource_value(Variables.PRODUCTS, change=50)
            return
        if self.current_state == PersonStates.FEEDING:
            if self.resources.get_resource_value(Variables.SATIETY) >= 10:
                self.resources.set_resource_value(Variables.SATIETY, change=-10)
            if self.resources.get_resource_value(Variables.ENERGY) >= 10:
                self.resources.set_resource_value(Variables.ENERGY, change=-10)
            #if self.resources.get_resource_value(Variables.PRODUCTS) >= 10 * (kwargs['eat'] + 1):
            #    self.resources.set_resource_value(Variables.PRODUCTS, change=-10 * (kwargs['eat'] + 1))
            return
        if self.current_state in [PersonStates.PLAYING_WITH_CAT, PersonStates.PLAYING_WITH_KITTEN]:
            if self.resources.get_resource_value(Variables.SATIETY) >= 10:
                self.resources.set_resource_value(Variables.SATIETY, change=-10)
            if self.resources.get_resource_value(Variables.ENERGY) >= 10:
                self.resources.set_resource_value(Variables.ENERGY, change=-10)
