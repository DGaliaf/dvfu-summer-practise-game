import random
from typing import Any

import pygame.sprite
from collections import defaultdict

from pkg import SpriteSheet


class Fire(pygame.sprite.Sprite):
    def __init__(self, cfg: dict[str, Any], x: int, speed: int = 3):
        pygame.sprite.Sprite.__init__(self)

        self.cfg = cfg

        """ Sprite initializing """
        self.__images_dir = self.cfg.get("paths").get("obstacles")

        self.__blue_fire_sprite_sheet_image = pygame.image.load(
            self.__images_dir + "/blue_burning_loop_1.png").convert_alpha()
        self.__blue_fire_sprite_sheet = SpriteSheet(self.__blue_fire_sprite_sheet_image)

        self.__green_fire_sprite_sheet_image = pygame.image.load(
            self.__images_dir + "/green_burning_loop_1.png").convert_alpha()
        self.__green_fire_sprite_sheet = SpriteSheet(self.__green_fire_sprite_sheet_image)

        self.__orange_fire_sprite_sheet_image = pygame.image.load(
            self.__images_dir + "/orange_burning_loop_1.png").convert_alpha()
        self.__orange_fire_sprite_sheet = SpriteSheet(self.__orange_fire_sprite_sheet_image)

        self.__purple_fire_sprite_sheet_image = pygame.image.load(
            self.__images_dir + "/purple_burning_loop_1.png").convert_alpha()
        self.__purple_fire_sprite_sheet = SpriteSheet(self.__purple_fire_sprite_sheet_image)

        self.__total_fire_frames = 8
        self.__current_fire_frame = 0

        self.__frames = defaultdict(list)

        for i in range(self.__total_fire_frames):
            self.__frames[0].append(self.__blue_fire_sprite_sheet.get_image(i, 24, 32, 3, (0, 0, 0)))
            self.__frames[1].append(self.__green_fire_sprite_sheet.get_image(i, 24, 32, 3, (0, 0, 0)))
            self.__frames[2].append(self.__orange_fire_sprite_sheet.get_image(i, 24, 32, 3, (0, 0, 0)))
            self.__frames[3].append(self.__purple_fire_sprite_sheet.get_image(i, 24, 32, 3, (0, 0, 0)))

        self.__random_fire = random.randrange(0, 3)
        """ -------------------------- """

        self.image = self.__frames.get(self.__random_fire)[self.__current_fire_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (self.cfg["screen"]["width"] + x, self.cfg["screen"]["height"] - 98)

        self.__speed = speed

    def update(self) -> None:
        if self.rect.x < -100:
            self.kill()

        self.rect.x -= self.__speed

    def change_sprite(self):
        self.image = self.__frames.get(self.__random_fire)[self.__current_fire_frame % self.__total_fire_frames]

        prev_x, prev_y = self.rect.x, self.rect.y

        self.rect = self.image.get_rect()
        self.rect.x = prev_x
        self.rect.y = prev_y

        self.__current_fire_frame += 1
