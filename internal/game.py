from typing import Any
import pygame

from internal.level import Level
from internal.obstacles.fire import Fire
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

        self.player = Player(self._cfg)

        self.levels = [
            Level(self._screen, self._cfg, self.player, [
                Fire(self._cfg, x=100, speed=3),
                Fire(self._cfg, x=400, speed=4),
                Fire(self._cfg, x=150, speed=2),
            ], "Level #1"),
            Level(self._screen, self._cfg, self.player, [
                Fire(self._cfg, x=100, speed=3),
                Fire(self._cfg, x=400, speed=4),
                Fire(self._cfg, x=150, speed=2),
            ], "Level #2"),
            Level(self._screen, self._cfg, self.player, [
                Fire(self._cfg, x=100, speed=3),
                Fire(self._cfg, x=400, speed=4),
                Fire(self._cfg, x=150, speed=2),
            ], "Level #3")
        ]
        self.current_level = 0
        self.next_level = True

    def load_level(self, levels) -> bool:
        key = pygame.key.get_pressed()

        levels[self.current_level].start()
        levels[self.current_level].handle_key(key)

        if len(self.levels[self.current_level].obstacles_group.sprites()) == 0:
            self.current_level = (self.current_level + 1) % len(self.levels)

    def start(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        pygame.display.set_caption("Jumping Man")

        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 75)

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
                    self.levels[self.current_level].player.change_sprite()

                    for obstacle in self.levels[self.current_level].obstacles:
                        obstacle.change_sprite()

            if pygame.sprite.spritecollide(self.player, self.levels[self.current_level].obstacles_group, False):
                # print("Collided")
                pass

            # TODO: Level switches
            if self.__menu.game_paused:
                self.__menu.show()
            else:
                self.load_level()

            pygame.display.update()

        pygame.quit()
