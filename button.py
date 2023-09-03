import pygame

from constants import BUTTON_SCALE
from utils import build_path, scale_img

class Button():
    def __init__(self, x, y, asset_path) -> None:
        self.image = scale_img(pygame.image.load(build_path(asset_path)).convert_alpha(), BUTTON_SCALE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        action = False
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                action = True
        surface.blit(self.image, self.rect)

        return action