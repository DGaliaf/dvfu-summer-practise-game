from typing import Any

from internal.obstacles import BaseObstacle
from pkg import load_image


class Iceball(BaseObstacle):
    def __init__(self, cfg: dict[str, Any]):
        super().__init__(cfg)

        self._x, self._y = self.get_random_position()

        self.__total_frames = 5
        self.__current_frame = 0

        self._frames = []
        self.load_frames()

        self.image = self._frames[self.__current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (self._x, self._y)

    def load_frames(self) -> None:
        for i in range(1, self.__total_frames+1):
            self._frames.append(load_image(self._images_dir + f"/iceball/{i}.png", scale=2, flipped=True))

    def change_sprite(self):
        self.image = self._frames[self.__current_frame % self.__total_frames]
        self.__current_frame += 1

        prev_x, prev_y = self.rect.x, self.rect.y

        self.rect = self.image.get_rect()
        self.rect.x = prev_x
        self.rect.y = prev_y

