from typing import Any

import pygame

from internal.ui import Button

pygame.init()

class Menu:
    def __init__(self, screen: pygame.surface.Surface, cfg: dict[str, Any]):
        self.screen = screen
        self.cfg = cfg

        self.game_paused = True
        self.run = True

        self.menu_state = "START"

        self.__bg_image = pygame.image.load(self.cfg.get("paths").get("assets") + "/menu_background.png")
        self.__bg_image = pygame.transform.scale(self.__bg_image, (self.cfg.get("screen").get("width"), self.cfg.get("screen").get("height")))

        self._buttons_path = self.cfg.get("paths").get("buttons")
        self._sfx_path = self.cfg.get("paths").get("sfx")

        self.__resume_img = pygame.image.load(self._buttons_path + "/button_resume.png").convert_alpha()
        self.__play_img = pygame.image.load(self._buttons_path + "/button_play.png").convert_alpha()
        self.__quit_img = pygame.image.load(self._buttons_path + "/button_quit.png").convert_alpha()
        self.__back_img = pygame.image.load(self._buttons_path + "/button_back.png").convert_alpha()

        self.__resume_button = Button(self._sfx_path,
                                      self.cfg.get("game").get("sound").get("effects"),
                                      self.cfg.get("screen").get("width") / 2,
                                      (self.cfg.get("screen").get("height") / 2) - 50,
                                      self.__resume_img, 1)
        self.__play_button = Button(self._sfx_path,
                                    self.cfg.get("game").get("sound").get("effects"),
                                    self.cfg.get("screen").get("width") / 2,
                                    (self.cfg.get("screen").get("height") / 2) - 50,
                                    self.__play_img, 1)
        self.__quit_button = Button(self._sfx_path,
                                    self.cfg.get("game").get("sound").get("effects"),
                                    self.cfg.get("screen").get("width") / 2,
                                    (self.cfg.get("screen").get("height") / 2) + 50,
                                    self.__quit_img, 1)

        self.menu_sound = pygame.mixer.Sound(self._sfx_path + "/menu.wav")
        self.menu_sound.set_volume(self.cfg.get("game").get("sound").get("music"))

        self.pause_sound = pygame.mixer.Sound(self._sfx_path + "/pause.wav")
        self.pause_sound.set_volume(self.cfg.get("game").get("sound").get("effects"))

        self.unpause_sound = pygame.mixer.Sound(self._sfx_path + "/unpause.wav")
        self.unpause_sound.set_volume(self.cfg.get("game").get("sound").get("effects"))

        self.sound_played = False

    def show(self):
        self.screen.blit(self.__bg_image, (0, 0))

        if not self.sound_played:
            self.pause_sound.play()
            self.menu_sound.play()

            self.sound_played = True

        match self.menu_state:
            case "PAUSE": self.__draw_pause_menu()
            case "START": self.__draw_start_menu()
            case "END": self.__draw_end_menu()

    def __draw_pause_menu(self):
        if self.__resume_button.draw(self.screen):
            self.game_paused = False
        if self.__quit_button.draw(self.screen):
            self.run = False

    def __draw_start_menu(self):
        if self.__play_button.draw(self.screen):
            self.game_paused = False
        if self.__quit_button.draw(self.screen):
            self.run = False

    def __draw_end_menu(self):
        if self.__play_button.draw(self.screen):
            self.game_paused = False
        if self.__quit_button.draw(self.screen):
            self.run = False