import random
from abc import abstractmethod
from typing import Any

import pygame.sprite


class BaseObstacle(pygame.sprite.Sprite):
    def __init__(self, cfg: dict[str, Any]):
        pygame.sprite.Sprite.__init__(self)

        self.cfg = cfg
        self._images_dir = self.cfg.get("paths").get("obstacles")

        self._frames = None

        self._x, self._y = 0, 0

        self.image = None
        self.rect: pygame.rect.Rect = None

        self.__speed = random.randrange(2, 4)

    def update(self) -> None:
        if self.rect.x < -75:
            self.kill()

        self.rect.x -= self.__speed

    def get_random_position(self) -> (int, int):
        offset_y = random.randint(230, 600)

        position_x = random.randrange(self.cfg["screen"]["width"] + 200,
                                      self.cfg["screen"]["width"] + random.randint(900, 1600),
                                      random.randint(100, 400))
        position_y = random.randrange(self.cfg["screen"]["height"] - offset_y,
                                      self.cfg["screen"]["height"] - 200,
                                      random.randint(20, 100))

        return (position_x, position_y)

    def reset(self) -> None:
        self.rect.center = (self._x, self._y)

    @abstractmethod
    def load_frames(self) -> (list | dict, pygame.Surface):
        pass

    @abstractmethod
    def change_sprite(self):
        pass
