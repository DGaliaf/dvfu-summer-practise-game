from typing import Any

import pygame

from internal.ui import Button

pygame.init()

class Menu:
    def __init__(self, screen: pygame.surface.Surface, cfg: dict[str, Any]):
        self.screen = screen
        self.cfg = cfg

        self.game_paused = False
        self.run = True

        self.menu_state = "pause"

        self.TEXT_COL = (255, 255, 255)
        self.MENU_COLOR = (52, 78, 91)

        self._buttons_path = self.cfg.get("paths").get("buttons")

        self.__resume_img = pygame.image.load(self._buttons_path + "/button_resume.png").convert_alpha()
        self.__quit_img = pygame.image.load(self._buttons_path + "/button_quit.png").convert_alpha()
        self.__back_img = pygame.image.load(self._buttons_path + "/button_back.png").convert_alpha()

        self.__resume_button = Button(self.cfg.get("screen").get("width") / 2,
                                      (self.cfg.get("screen").get("height") / 2) - 50,
                                      self.__resume_img, 1)
        self.__quit_button = Button(self.cfg.get("screen").get("width") / 2,
                                    (self.cfg.get("screen").get("height") / 2) + 50,
                                    self.__quit_img, 1)
        self.__back_button = Button(self.cfg.get("screen").get("width"),
                                    (self.cfg.get("screen").get("height") / 2) + 100,
                                    self.__back_img, 1)

    def show_menu(self):
        self.screen.fill(self.MENU_COLOR)

        match self.menu_state:
            case "pause": self.__draw_pause_menu()

    def __draw_pause_menu(self):
        if self.__resume_button.draw(self.screen):
            self.game_paused = False
        if self.__quit_button.draw(self.screen):
            self.run = False
