import copy
from typing import Any
import pygame

from internal.level import Level
from internal.player import Player
from internal.ui import Menu

CHANGE_SPRITE = pygame.USEREVENT


class Game:
    def __init__(self, cfg: dict[str, Any]):
        self._cfg = cfg
        self._screen = screen = pygame.display.set_mode((
            self._cfg.get("screen").get("width"),
            self._cfg.get("screen").get("height"),
        ))

        self.__menu = Menu(self._screen, self._cfg)

        self.next_level = True

    def start(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        pygame.display.set_caption("Jumping Man")

        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 75)

        player = Player(self._cfg)
        level = Level(self._screen, self._cfg, player)

        while self.__menu.run:
            clock.tick(self._cfg.get("screen").get("fps"))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__menu.menu_state = "PAUSE"
                        self.__menu.game_paused = not self.__menu.game_paused

                if event.type == CHANGE_SPRITE:
                    level.player.change_sprite()

                    for obstacle in level.obstacles_group.sprites():
                        obstacle.change_sprite()

            if pygame.sprite.spritecollide(player, level.obstacles_group, False):
                print("Collided")

            if self.__menu.game_paused:
                self.__menu.show()
            else:
                key = pygame.key.get_pressed()

                level.start()
                level.handle_key(key)

            pygame.display.update()

        pygame.quit()
