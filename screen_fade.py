import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH


class ScreenFade():
    def __init__(self, colour, speed):
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0
    
    def fade_in(self, surface):
        completed = False
        self.fade_counter += self.speed
      
        pygame.draw.rect(surface, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        pygame.draw.rect(surface, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(surface, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        pygame.draw.rect(surface, self.colour, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
    
        if self.fade_counter >= SCREEN_WIDTH:
            completed = True

        return completed
    
    def fade_out(self, surface):
        completed = False
        self.fade_counter += self.speed

        pygame.draw.rect(surface, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))

        if self.fade_counter >= SCREEN_WIDTH:
            completed = True

        return completed