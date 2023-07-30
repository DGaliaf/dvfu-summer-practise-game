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

        self.image = None
        self.rect = None

        self.__speed = random.randrange(2, 4)

    def update(self) -> None:
        if self.rect.x < -75:
            self.kill()

        self.rect.x -= self.__speed

    def get_random_position(self) -> (int, int):
        x = random.randint(230, 600)

        return (random.randint(self.cfg["screen"]["width"] + 200, self.cfg["screen"]["width"] + random.randint(400, 800)),
                random.randint(self.cfg["screen"]["height"] - x, self.cfg["screen"]["height"] - 230))

    @abstractmethod
    def load_frames(self) -> (list | dict, pygame.Surface):
        pass

    @abstractmethod
    def change_sprite(self):
        pass
