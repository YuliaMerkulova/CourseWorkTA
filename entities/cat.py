from elements.resource_box import ResourceBox
from enums import Variables
from .base import BaseEntity


class Cat(BaseEntity):
    def __init__(self, image: str, scaling: float, speed: float = 3):
        super().__init__(image, scaling, speed)

        self.resources = ResourceBox(box_icon='resources/cat_sit.png', position=(830, 210), scaling=0.1)
        self.resources.set_resources({
            Variables.SATIETY: dict(icon='resources/food_icon.png', name='Сытость'),
            Variables.ENERGY: dict(icon='resources/sleep_icon.png', name='Энергия'),
            Variables.FUN: dict(icon='resources/fun_icon.png', name='Развлечение')
        })

    def update_indicators(self, person):
        pass
