import math
import pygame
from constants import SHOW_COLLIDE_RECT, SCALE, TILE_SIZE
from colours import RED
from utils import build_path, scale_img

class Character():
    def __init__(self, x, y, health, max_health, char_type, boss = False):
        self.rect = pygame.Rect(0, 0, TILE_SIZE - 10, TILE_SIZE - 10)
        self.rect.center = (x, y)
        self.frame_index = 0
        self.action = 0 #0:idle, 1:run
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.max_health = max_health
        self.health = health
        self.alive = True
        self.char_type = char_type
        self.animations = self.load_animations()
        self.image = self.animations[self.action][self.frame_index]
        self.flip = False
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.stunned = False
        self.stunned_time = pygame.time.get_ticks()
        self.boss = boss
        self.last_attack = pygame.time.get_ticks()

    def load_animations(self):  
        char_animations = []
        char_animation_types = ["idle", "run"]

        for action in char_animation_types:
            animation_images = []

            for i in range(4):
                img = scale_img(pygame.image.load(build_path(f"assets/images/characters/{self.char_type}/{action}/{i}.png")).convert_alpha(), SCALE)
                animation_images.append(img)

            char_animations.append(animation_images)

        return char_animations

    def move(self, dx, dy, obstacles, exit = None):
        if not self.alive or self.stunned:
            return [0, 0]

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
        self.calculate_dx_collitions(dx, obstacles)
        self.rect.y += dy
        self.calculate_dy_collitions(dy, obstacles)
        level_completed = self.calculate_exit_collitions(exit)
        screen_scroll = self.calculate_offset()

        return screen_scroll, level_completed
    
    def calculate_dx_collitions(self, dx, obstacles):
        for obstacle in obstacles:
            if obstacle[1].colliderect(self.rect):
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right
    
    def calculate_dy_collitions(self, dy, obstacles):
        for obstacle in obstacles:
            if obstacle[1].colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom

    def calculate_exit_collitions(self, exit):
        exit_collition = False
        if exit and exit[1].colliderect(self.rect):
            exit_distance = math.sqrt(((self.rect.centerx - exit[1].centerx) ** 2) + ((self.rect.centery - exit[1].centery)** 2))
            if exit_distance < 20:
                exit_collition = True
        
        return exit_collition
    
    def calculate_offset(self):
        return [0, 0]

    def update(self):
        if not self.alive or self.stunned:
            self.image = self.animations[0][0]
            return
        
        if self.health <= 0:
            self.health = 0
            self.alive = False
        
        hit_cooldown = 1000

        if self.hit and (pygame.time.get_ticks() - self.last_hit > hit_cooldown):
            self.hit = False
        
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
        surface.blit(flipped_image, self.get_draw_coordinates())

        if SHOW_COLLIDE_RECT:
            pygame.draw.rect(surface, RED, self.rect, 1)

    def get_draw_coordinates(self):
        return self.rect

    def cure(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def defend(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False