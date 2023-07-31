import pygame


class Button:
    def __init__(self, sfx_path, effects_volume, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()

        self.__click_sound = pygame.mixer.Sound(sfx_path + "/confirm.wav")
        self.__click_sound.set_volume(effects_volume)
        self.__hover_sound = pygame.mixer.Sound(sfx_path + "/hover.wav")
        self.__hover_sound.set_volume(effects_volume)

        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.clicked = False
        self.played_sound = False

    def draw(self, surface):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if not self.played_sound:
                self.__hover_sound.play()

                self.played_sound = True

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.__click_sound.play()
                self.clicked = True
                action = True
        else:
            self.played_sound = False

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
