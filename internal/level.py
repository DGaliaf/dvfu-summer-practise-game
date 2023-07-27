from typing import Any

import pygame

from internal.player import Player


class Level:
    def __init__(self, screen: pygame.surface.Surface, cfg: dict[str, Any]):
        self.screen = screen
        self.cfg = cfg

        # Parallax variables
        self.__ground_image = pygame.image.load(self.cfg.get("paths").get("background") + "/ground.png").convert_alpha()
        self.__ground_width = self.__ground_image.get_width()
        self.__ground_height = self.__ground_image.get_height()

        self.__bg_images = []
        for i in range(1, 6):
            bg_image = pygame.image.load(self.cfg.get("paths").get("background") + f"/plx-{i}.png").convert_alpha()
            bg_image = pygame.transform.scale(bg_image,
                                              (self.cfg.get("screen").get("width"),
                                               self.cfg.get("screen").get("height")))
            self.__bg_images.append(bg_image)
        self.__bg_width = self.__bg_images[0].get_width()

        self.__scroll = 0
        # -------------------------------------------

        self.player = None
        self.obstacles = None

        self.player_group = pygame.sprite.Group()
        self.obstacles_group = pygame.sprite.Group()

        self.__init = False

    def start(self, player: Player, obstacles: list) -> None:
        self.__draw_bg()
        self.__draw_ground()

        if not self.__init:
            self.player_group.add(player)

            for obstacle in obstacles:
                self.obstacles_group.add(obstacle)

            self.__init = True

            self.player = player
            self.obstacles = obstacles

        self.player_group.draw(self.screen)
        self.obstacles_group.draw(self.screen)

        self.player_group.update()
        self.obstacles_group.update()

    def handle_key(self, key: pygame.key.ScancodeWrapper) -> None:
        if abs(self.__scroll) > self.__bg_width:
            self.__scroll = 0

        if key[pygame.K_d] and self.__scroll < 3000:
            self.__scroll += 5

        if key[pygame.K_a] and self.__scroll > 0:
            self.__scroll -= 5

    def __draw_bg(self) -> None:
        for x in range(5):
            speed = 1
            for i in self.__bg_images:
                self.screen.blit(i, ((x * self.__bg_width) - self.__scroll * speed, 0))
                speed += 0.2

    def __draw_ground(self) -> None:
        for x in range(15):
            self.screen.blit(self.__ground_image,
                             ((x * self.__ground_width) - self.__scroll * 0.5,
                              self.cfg.get("screen").get("width") - self.cfg.get("screen").get("height") - 100))
