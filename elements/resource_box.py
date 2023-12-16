from typing import Dict, Tuple, Optional

import arcade
from arcade import SpriteList

from elements.resource import Resource
from enums import Variables


class ResourceBox:
    def __init__(self, box_icon: str, position: Tuple[float, float], scaling: float):
        self.icon_texture = arcade.load_texture(box_icon)
        self.position = position
        self.scaling = scaling
        self.resources: Dict[Variables, Resource] = {}
        self.sprite_list = SpriteList()

    def draw(self):
        arcade.draw_scaled_texture_rectangle(self.position[0], self.position[1], self.icon_texture, self.scaling)
        for resource in self.resources.values():
            resource.draw()
        self.sprite_list.draw()

    def set_resources(self, resources: Dict[Variables, Dict]):
        self.resources.clear()
        for index, pair in enumerate(resources.items()):
            self.resources[pair[0]] = Resource(**pair[1], position=(self.position[0] + 40,
                                                                    self.position[1] + 10 - index * 40),
                                               sprite_list=self.sprite_list)

    def get_resource_value(self, resource: Variables):
        if resource in self.resources:
            return self.resources[resource].value

    def set_resource_value(self, resource: Variables, value: Optional[float] = None, change: Optional[float] = None):
        if resource in self.resources:
            if value is not None:
                self.resources[resource].value = value
            elif change:
                self.resources[resource].value += change
