from typing import Any
import pygame

from internal.level import Level
from internal.player import Player
from internal.ui import Menu

CHANGE_SPRITE = pygame.USEREVENT
RUN_SOUND_PLAY = pygame.USEREVENT + 1


class Game:
    def __init__(self, cfg: dict[str, Any]):
        self._cfg = cfg
        self._screen = screen = pygame.display.set_mode((
            self._cfg.get("screen").get("width"),
            self._cfg.get("screen").get("height"),
        ))

        self.__game_sound = pygame.mixer.Sound(self._cfg.get("paths").get("sfx") + "/forest_sound.wav")
        self.__game_sound.set_volume(self._cfg.get("game").get("sound").get("music"))
        self.__game_sound_played = False

        self.__menu = Menu(self._screen, self._cfg)

    def start(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        pygame.display.set_caption("Jumping Man")

        clock = pygame.time.Clock()
        pygame.time.set_timer(CHANGE_SPRITE, 75)
        pygame.time.set_timer(RUN_SOUND_PLAY, 275)

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

                if event.type == RUN_SOUND_PLAY:
                    if player.get_state() == "RUN":
                        player.run_sound.play()

            if self.__menu.game_paused:
                self.__menu.show()

                self.__game_sound_played = False
                self.__game_sound.stop()
            else:
                if not player.is_alive:
                    self.__menu.menu_state = "END"
                    self.__menu.game_paused = True

                    player.reset()

                    for obstacle in level.obstacles_group.sprites():
                        obstacle.reset()
                else:
                    self.__menu.sound_played = False

                    if not self.__game_sound_played:
                        self.__menu.menu_sound.stop()
                        self.__menu.unpause_sound.play()
                        self.__game_sound.play()

                        self.__game_sound_played = True

                    key = pygame.key.get_pressed()

                    level.start()
                    level.handle_key(key)

            pygame.display.update()

        pygame.quit()
