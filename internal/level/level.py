import random
from typing import Any

import pygame

from internal.obstacles import BaseObstacle, Firebolt, Iceball, Waterball, Fire
from internal.player import Player, get_best_score, write_best_score


class Level:
    def __init__(self, screen: pygame.surface.Surface, cfg: dict[str, Any], player: Player):
        self.screen = screen
        self.cfg = cfg

        self.__ui_image = pygame.image.load(self.cfg.get("paths").get("assets") + "/ui.png").convert_alpha()
        self.__ui_image = pygame.transform.scale(self.__ui_image, (self.cfg.get("screen").get("width"),
                                                                   self.cfg.get("screen").get("height")))
        # Parallax
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

        self.player = player
        self.current_score = 0
        self.best_score = int(get_best_score(self.cfg))

        self.difficulty = 1
        self.multiplier = 0.00001

        self.player_group = pygame.sprite.Group()
        self.obstacles_group = pygame.sprite.Group()

        self.max_obstacles = 5

    def start(self) -> None:
        self.__draw_bg()
        self.__draw_ui()
        self.__draw_ground()

        if len(self.player_group.sprites()) == 0:
            self.player_group.add(self.player)

        if len(self.obstacles_group.sprites()) < self.max_obstacles:
            obstacles = self.__get_obstacles()

            self.obstacles_group.add(obstacles[random.randint(0, len(obstacles) - 1)])

        if pygame.sprite.spritecollideany(self.player, self.obstacles_group):
            self.player.is_alive = False

            if int(self.current_score) > self.best_score:
                write_best_score(self.cfg, int(self.current_score))
                self.best_score = int(get_best_score(self.cfg))

            self.reset()

        self.player_group.draw(self.screen)
        self.obstacles_group.draw(self.screen)

        self.current_score += ((self.difficulty-1) * 10 if self.difficulty <= 1000 else 1000)
        self.difficulty += self.multiplier

        self.player_group.update()
        self.obstacles_group.update()

    def handle_key(self, key: pygame.key.ScancodeWrapper) -> None:
        if abs(self.__scroll) > self.__bg_width:
            self.__scroll = 0

        if key[pygame.K_d] and self.__scroll < 3000:
            self.__scroll += 5

        if key[pygame.K_a] and self.__scroll > 0:
            self.__scroll -= 5

    def reset(self):
        self.current_score = 0
        self.difficulty = 1

    def __get_obstacles(self) -> list[BaseObstacle]:
        return [
                Firebolt(self.cfg),
                Iceball(self.cfg),
                Waterball(self.cfg),
                Fire(self.cfg)
            ]

    def __draw_ui(self):
        font = pygame.font.Font(self.cfg.get("paths").get("assets") + "/font.ttf", 45)

        print(self.current_score)

        best_score = font.render(str(int(self.best_score)), False, (253, 198, 137))
        current_score = font.render(str(int(self.current_score)), False, (253, 198, 137))
        difficulty = font.render(str(int(self.difficulty)), False, (253, 198, 137))

        self.screen.blit(self.__ui_image, (0, 0))
        self.screen.blit(best_score, (1015, 20))
        self.screen.blit(current_score, (140, 20))
        self.screen.blit(difficulty, (635, 31))

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
