import collections
import math
from typing import Tuple, Optional, List, Dict

from arcade import Sprite, load_texture, SpriteList

from elements import IndicatorBar
from enums import SpritePosition, FaceSide, SpriteAngle


def load_texture_pair(filename):
    return load_texture(filename), load_texture(filename, flipped_horizontally=True)


class BaseSprite(Sprite):
    def __init__(self, image: str, scaling: float, speed: float, start_side: FaceSide = FaceSide.LEFT):
        super().__init__(image, scaling)
        self.face_direction = start_side
        self.sprite_textures = load_texture_pair(image)
        self.texture = self.sprite_textures[start_side.value]
        self.destination_point = None
        self.speed = speed
        self.path = None

    def on_update(self, delta_time: float = 1 / 60):
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
            self.destination_point = None


class BaseEntity:
    def __init__(self, image: str, scaling: float, speed: float):
        self.sprite = BaseSprite(image, scaling, speed)
        self.position: Optional[SpritePosition] = None
        self.map: Dict[SpritePosition, List[SpritePosition]] = {}
        self.current_state = None
        self.next_state = None
        self.next_position = None

    def set_face_side(self, side: FaceSide = FaceSide.RIGHT):
        self.sprite.face_direction = side

    def set_position(self, position):
        self.position = position
        self.sprite.position = position.value

    def move_to(self, position):
        self.position = position
        self.sprite.destination_point = position.value

    def get_position(self) -> Optional:
        if self.sprite.destination_point:
            return None
        return self.position

    def find_path(self, start, finish):
        position_queue = collections.deque([(start, [start])])

        while position_queue:
            current, path = position_queue.popleft()
            if current == finish:
                return path
            for neighbor in self.map[current]:
                if neighbor not in path:
                    position_queue.append((neighbor, path + [neighbor]))

    def set_path(self, path):
        self.sprite.destination_point = path[0].value
        if len(path) > 1:
            self.sprite.path = list(map(lambda x: x.value, path[1:]))
        self.position = path[-1]

    def set_angle(self, angle: SpriteAngle):
        pass

    def get_state(self):
        return self.current_state

    def update_indicators(self, person):
        pass
