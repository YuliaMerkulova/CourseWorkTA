from typing import Tuple

from arcade import Sprite


class Turn(Sprite):
    def __init__(self, image: str, scaling: float, position: Tuple[float, float]):
        super().__init__(image, scaling)
        self.position = position
        self.visible = False

    def start(self):
        self.visible = True
        self.angle = 0

    def update(self, delta_time: float = 1 / 60):
        self.angle += 5
