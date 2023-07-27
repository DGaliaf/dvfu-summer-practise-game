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

    def start(self):
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption("Jumping Man")

        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 75)

        player = Player(self._cfg)

        level1 = Level(self._screen, self._cfg)

        while self.__menu.run:
            clock.tick(self._cfg.get("screen").get("fps"))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__menu.game_paused = not self.__menu.game_paused

                if event.type == CHANGE_SPRITE:
                    if level1.player is not None:
                        level1.player.change_sprite()

            if self.__menu.game_paused:
                self.__menu.show_menu()
            else:
                key = pygame.key.get_pressed()

                level1.start(player, [])
                level1.handle_key(key)

            pygame.display.update()

        pygame.quit()
