import math
import random
import pygame
from constants import FIREBALL_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, ARROW_SPEED

class Weapon():
    def __init__(self, image, arrow_image) -> None:
        self.angle = 0
        self.original_image = image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.arrow_image = arrow_image
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player):
        self.rect.center = player.rect.center
        pos = pygame.mouse.get_pos()
        x_distance = pos[0] - self.rect.centerx
        y_distance = -(pos[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_distance, x_distance))

        arrow = None
        shot_cooldown = 300
        # Get mouse left-click:0
        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown:
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()
        
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False
        
        return arrow

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))

class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle
        self.original_image = image
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dx = math.cos(math.radians(self.angle)) * ARROW_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * ARROW_SPEED)

    def update(self, screen_scroll, obstacles, enemies):
        damage = 0
        damage_pos = None

        self.rect.x += (self.dx + screen_scroll[0])
        self.rect.y += (self.dy + screen_scroll[1])

        for obstacle in obstacles:
            if obstacle[1].colliderect(self.rect):
                self.kill()

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
        
        for enemy in enemies:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 50 + random.randint(-5, 5)
                damage_pos = enemy.rect
                enemy.defend(damage)
                enemy.stunned = True
                enemy.stunned_time = pygame.time.get_ticks()
                self.kill()
                break
        
        return damage, damage_pos

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))

class Fireball(pygame.sprite.Sprite):
    def __init__(self, image, x, y, target_x, target_y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        x_dist = target_x - x
        y_dist = -(target_y - y)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dx = math.cos(math.radians(self.angle)) * FIREBALL_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * FIREBALL_SPEED)

    def update(self, screen_scroll, obstacles, player):
        damage = 0
        damage_pos = None

        self.rect.x += (self.dx + screen_scroll[0]) + self.dx
        self.rect.y += (self.dy + screen_scroll[1]) + self.dy

        for obstacle in obstacles:
            if obstacle[1].colliderect(self.rect):
                self.kill()

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
      
        if player.rect.colliderect(self.rect) and player.alive:
            damage = 20 + random.randint(-5, 5)
            damage_pos = player.rect
            player.defend(damage)
            self.kill()
        
        return damage, damage_pos

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))

