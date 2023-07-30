import pygame


def load_image(image_path: str, scale: int = 3, colorkey: tuple[int, int, int] = (0, 0, 0), flipped: bool = False) -> pygame.Surface:
    img = pygame.image.load(image_path).convert_alpha()
    img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))

    if flipped:
        img = pygame.transform.flip(img, True, False)

    img.set_colorkey((0, 0, 0))

    return img

