import random
from typing import Any

from collections import defaultdict

from internal.obstacles import BaseObstacle
from pkg import load_image


class Fire(BaseObstacle):
    def __init__(self, cfg: dict[str, Any]):
        super().__init__(cfg)

        self._x, _ = self.get_random_position()
        self._y = self.cfg.get("screen").get("height") - 88

        self.__total_fire_frames = 8
        self.__current_fire_frame = 0
        self.__random_fire = random.randrange(0, 4)

        self._frames = defaultdict(list)
        self.load_frames()

        self.image = self._frames.get(self.__random_fire)[self.__current_fire_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (self._x, self._y)

    def load_frames(self) -> None:
        for i in range(1, self.__total_fire_frames + 1):
            self._frames[0].append(load_image(self._images_dir + f"/fire/blue/{i}.png"))
            self._frames[1].append(load_image(self._images_dir + f"/fire/green/{i}.png"))
            self._frames[2].append(load_image(self._images_dir + f"/fire/orange/{i}.png"))
            self._frames[3].append(load_image(self._images_dir + f"/fire/purple/{i}.png"))

    def change_sprite(self):
        self.image = self._frames.get(self.__random_fire)[self.__current_fire_frame % self.__total_fire_frames]

        prev_x, prev_y = self.rect.x, self.rect.y

        self.rect = self.image.get_rect()
        self.rect.x = prev_x
        self.rect.y = prev_y

        self.__current_fire_frame += 1
