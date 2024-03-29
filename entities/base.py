import collections
import math
from abc import abstractmethod
from typing import Tuple, Optional, List, Dict

import arcade
from arcade import Sprite, load_texture, SpriteList

from elements import IndicatorBar
from elements.resource_box import ResourceBox
from enums import SpritePosition, FaceSide, SpriteAngle


def load_texture_pair(filename):
    return load_texture(filename), load_texture(filename, flipped_horizontally=True)


class BaseSprite(Sprite):
    def __init__(self, image: str, scaling: float, speed: float, start_side: FaceSide, angle):
        super().__init__(image, scaling)
        self.base_scale = scaling
        self.base_texture = load_texture(image)
        self.base_angle = angle
        self.face_direction = start_side
        self.sprite_textures = load_texture_pair(image)
        self.texture = self.sprite_textures[start_side.value]
        self.destination_point = None
        self.speed = speed
        self.path = None
        self.position_states = {}

    def update(self, delta_time: float = 1 / 60):
        if not self.destination_point:
            return

        x_diff = self.destination_point[0] - self.center_x
        y_diff = self.destination_point[1] - self.center_y
        target_angle_radians = math.atan2(y_diff, x_diff)
        change_x = self.speed * math.cos(target_angle_radians)
        self.center_x += change_x
        self.center_y += self.speed * math.sin(target_angle_radians)

        if change_x < 0 and self.face_direction == FaceSide.RIGHT:
            self.face_direction = FaceSide.LEFT
        elif change_x > 0 and self.face_direction == FaceSide.LEFT:
            self.face_direction = FaceSide.RIGHT
        self.texture = self.sprite_textures[self.face_direction.value]

        if abs(x_diff) < self.speed and abs(y_diff) < self.speed:
            if self.path:
                self.destination_point = self.path[0]
                if len(self.path) > 1:
                    self.path = self.path[1:]
                else:
                    self.path = None
                return
            if self.destination_point in self.position_states:
                self.position_states[self.destination_point].set_state(self)
            self.destination_point = None

    def move(self, path: List[Tuple[float, float]]):
        self.reset()
        self.destination_point = path[0]
        self.path = path[1:]

    def reset(self):
        self.angle = self.base_angle
        self.texture = self.base_texture
        self.scale = self.scale
        self.visible = True

    def set_state(self, position: Tuple[float, float]):
        if position in self.position_states:
            self.position_states[position].set_state(self)


class BaseEntity:
    def __init__(self, image: str, scaling: float, speed: float, angle: float = 0,
                 start_side: FaceSide = FaceSide.LEFT):
        self.sprite = BaseSprite(image, scaling, speed, start_side, angle)
        self.position: Optional[SpritePosition] = None
        self.map: Dict[SpritePosition, List[SpritePosition]] = {}
        self.current_state = None
        self.next_position = None
        self.resources: Optional[ResourceBox] = None
        self.scaling = scaling
        self.speed = speed

    def draw(self):
        self.sprite.draw()
        if self.resources:
            self.resources.draw()
        arcade.draw_text(f'Статус: {self.current_state.value}', self.resources.position[0] - 10,
                         self.resources.position[1] - len(self.resources.resources) * 40 + 10, arcade.color.BLACK,
                         font_size=11)

    def update(self):
        self.sprite.update()

    def set_position(self, position):
        self.position = position
        self.sprite.position = position.value

    def is_moving(self):
        return self.sprite.destination_point is not None

    def move_to(self, position: SpritePosition):
        if self.position == position:
            return
        self.sprite.move(list(map(lambda x: x.value, self.find_path(self.position, position))))
        self.position = position

    def get_position(self) -> Optional[SpritePosition]:
        if self.sprite.destination_point:
            return None
        return self.position

    def find_path(self, start, finish):
        if start == finish:
            return []
        position_queue = collections.deque([(start, [start])])

        while position_queue:
            current, path = position_queue.popleft()
            if current == finish:
                return path
            for neighbor in self.map[current]:
                if neighbor not in path:
                    position_queue.append((neighbor, path + [neighbor]))

    def get_state(self):
        return self.current_state

    @abstractmethod
    def update_indicators(self, person):
        pass
