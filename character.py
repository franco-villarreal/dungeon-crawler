import math
import pygame
from constants import OFFSET, RED, SCALE

class Character():
    def __init__(self, x, y, health, max_health, char_type, animations):
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)
        self.frame_index = 0
        self.action = 0 #0:idle, 1:run
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.max_health = max_health
        self.health = health
        self.alive = True
        self.char_type = char_type
        self.animations = animations
        self.image = self.animations[self.action][self.frame_index]
        self.flip = False
        self.total_score = 0

    def move(self, dx, dy):
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)
        
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
        
        if self.running:
            self.update_action(1)#1:run
        else:
            self.update_action(0)#0:idle

        animation_cooldown = 70
        self.image = self.animations[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animations[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        
        if self.char_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - OFFSET * SCALE))
        else:
            surface.blit(flipped_image, self.rect)

        pygame.draw.rect(surface, RED, self.rect, 1)

    def cure(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def score(self, points):
        self.total_score += points

    def defend(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False