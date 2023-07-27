from collections import defaultdict
from typing import Any

import pygame

from pkg import SpriteSheet


class Player(pygame.sprite.Sprite):
    def __init__(self, cfg: dict[str, Any]):
        pygame.sprite.Sprite.__init__(self)

        self.cfg = cfg

        """ Sprite initializing """
        self.__images_dir = self.cfg.get("paths").get("character")

        self.__run_sprite_sheet_image = pygame.image.load(self.__images_dir + "/run cycle 48x48.png").convert_alpha()
        self.__run_sprite_sheet = SpriteSheet(self.__run_sprite_sheet_image)
        self.__total_run_frames = 8
        self.__current_run_frame = 0

        self.__idle_sprite_sheet_image = pygame.image.load(
            self.__images_dir + "/Character Idle 48x48.png").convert_alpha()
        self.__idle_sprite_sheet = SpriteSheet(self.__idle_sprite_sheet_image)
        self.__total_idle_frames = 10
        self.__current_idle_frame = 0

        self.__jump_sprite_sheet_image = pygame.image.load(self.__images_dir + "/player jump 48x48.png").convert_alpha()
        self.__jump_sprite_sheet = SpriteSheet(self.__jump_sprite_sheet_image)
        self.__total_jump_frames = 3
        self.__current_jump_frame = 0

        self.__frames = defaultdict(list)

        for i in range(self.__total_run_frames):
            self.__frames["RUN"].append(self.__run_sprite_sheet.get_image(i, 48, 48, 3, (0, 0, 0)))

        for i in range(self.__total_idle_frames):
            self.__frames["IDLE"].append(self.__idle_sprite_sheet.get_image(i, 48, 48, 3, (0, 0, 0)))

        for i in range(self.__total_jump_frames):
            self.__frames["JUMP"].append(self.__jump_sprite_sheet.get_image(i, 48, 48, 3, (0, 0, 0)))
        """ -------------------------- """

        self.__state = "IDLE"

        self.__jumping = False
        self.__y_gravity = 0.6
        self.__jump_height = 20
        self.__y_velocity = self.__jump_height

        self.__speed = 5
        self.__dir_x = 1

        self.image = self.__frames.get("IDLE")[self.__current_idle_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (100, self.cfg["screen"]["height"] - 100)

    def update(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_d]:
            self.__dir_x = 1
        if key[pygame.K_a]:
            self.__dir_x = -1

        if not (key[pygame.K_a] or key[pygame.K_d]) and not self.__jumping:
            self.__state = "IDLE"

        if key[pygame.K_SPACE]:
            self.__state = "JUMP"
            self.__jumping = True

        if self.__jumping:
            self.__jump()

        if key[pygame.K_a] or key[pygame.K_d]:
            if not self.__jumping:
                self.__state = "RUN"

            self.rect.x += self.__dir_x * self.__speed

        self.__keep_in_boundaries()

    def change_sprite(self):
        match self.__state:
            case "RUN":
                self.__current_idle_frame = 0
                self.__current_jump_frame = 0

                if self.__current_run_frame >= self.__total_run_frames:
                    self.__current_run_frame = 0

                if self.__dir_x == 1:
                    self.image = self.__frames.get("RUN")[self.__current_run_frame]
                elif self.__dir_x == -1:
                    self.image = self.__frames.get("RUN")[self.__current_run_frame]
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.image.set_colorkey((0, 0, 0))

                self.__current_run_frame += 1
            case "IDLE":
                self.__current_run_frame = 0
                self.__current_jump_frame = 0

                if self.__current_idle_frame >= self.__total_idle_frames:
                    self.__current_idle_frame = 0

                if self.__dir_x == 1:
                    self.image = self.__frames.get("IDLE")[self.__current_idle_frame]
                elif self.__dir_x == -1:
                    self.image = self.__frames.get("IDLE")[self.__current_idle_frame]
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.image.set_colorkey((0, 0, 0))

                self.__current_idle_frame += 1
            case "JUMP":
                self.__current_run_frame = 0
                self.__current_idle_frame = 0

                if self.__current_jump_frame >= self.__total_jump_frames:
                    self.__current_jump_frame = 2

                if self.__dir_x == 1:
                    self.image = self.__frames.get("JUMP")[self.__current_jump_frame]
                elif self.__dir_x == -1:
                    self.image = self.__frames.get("JUMP")[self.__current_jump_frame]
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.image.set_colorkey((0, 0, 0))

                self.__current_jump_frame += 1

        prev_x, prev_y = self.rect.x, self.rect.y

        self.rect = self.image.get_rect()
        self.rect.x = prev_x
        self.rect.y = prev_y

    def __jump(self):
        if self.__jumping:
            self.rect.y -= self.__y_velocity
            self.__y_velocity -= self.__y_gravity
            if self.__y_velocity < -self.__jump_height:
                self.__jumping = False
                self.__y_velocity = self.__jump_height
                self.rect.y = (self.cfg["screen"]["height"] - 172)

    def __keep_in_boundaries(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.cfg.get("screen").get("width"):
            self.rect.right = self.cfg.get("screen").get("width")
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.cfg.get("screen").get("height"):
            self.rect.bottom = self.cfg.get("screen").get("height")
