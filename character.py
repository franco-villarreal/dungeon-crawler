import math
import pygame
from constants import ATTACK_RANGE, COLLIDE_RECT, ENEMY_SPEED, OFFSET, RANGE, RED, SCALE, SCREEN_HEIGHT, SCREEN_WIDTH, SCROLL_THRESH, TILE_SIZE
from weapon import Fireball

class Character():
    def __init__(self, x, y, health, max_health, char_type, animations, boss = False):
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
        self.animations = animations
        self.image = self.animations[self.action][self.frame_index]
        self.flip = False
        self.total_score = 0
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.stunned = False
        self.stunned_time = pygame.time.get_ticks()
        self.boss = boss
        self.last_attack = pygame.time.get_ticks()

    def move(self, dx, dy, obstacles, exit = None):
        screen_scroll = [0, 0]
        level_completed = False

        if not self.alive or self.stunned:
            return screen_scroll

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
        for obstacle in obstacles:
            if obstacle[1].colliderect(self.rect):
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right

        self.rect.y += dy
        for obstacle in obstacles:
            if obstacle[1].colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom

        if self.char_type == 0:
            if exit[1].colliderect(self.rect):
                exit_distance = math.sqrt(((self.rect.centerx - exit[1].centerx) ** 2) + ((self.rect.centery - exit[1].centery)** 2))
                if exit_distance < 20:
                    level_completed = True
            
            left_offset = SCROLL_THRESH
            right_offset = (SCREEN_HEIGHT - SCROLL_THRESH)
            top_offset = SCROLL_THRESH
            bottom_offset = (SCREEN_HEIGHT - SCROLL_THRESH)
            
            if self.rect.left < left_offset:
                screen_scroll[0] = left_offset - self.rect.left
                self.rect.left = left_offset
            if self.rect.right > right_offset:
                screen_scroll[0] = right_offset - self.rect.right
                self.rect.right = right_offset

            if self.rect.top < top_offset:
                screen_scroll[1] = top_offset - self.rect.top
                self.rect.top = top_offset
            if self.rect.bottom > bottom_offset:
                screen_scroll[1] = bottom_offset - self.rect.bottom
                self.rect.bottom = bottom_offset
            

        return screen_scroll, level_completed

    def ai(self, player, obstacles, screen_scroll, fireball_image = None):
        dx = 0
        dy = 0
        clipped_line = ()
        stun_cooldown = 1000
        fireball = None

        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        if not self.alive:
            return

        line_of_sight = ((self.rect.centerx, self.rect.centery), ((player.rect.centerx, player.rect.centery)))
        for obstacle in obstacles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)

        player_distance = math.sqrt(((self.rect.centerx - player.rect.centerx) ** 2) + ((self.rect.centery - player.rect.centery)** 2))
        if not clipped_line and player_distance > RANGE:
            if self.rect.centerx > player.rect.centerx:
                dx = -ENEMY_SPEED
            if self.rect.centerx < player.rect.centerx:
                dx = ENEMY_SPEED
            if self.rect.centery > player.rect.centery:
                dy = -ENEMY_SPEED
            if self.rect.centery < player.rect.centery:
                dy = ENEMY_SPEED

        if not self.stunned:
            self.move(dx, dy, obstacles)

            if player_distance < ATTACK_RANGE and not self.hit:
                self.hit = True
                self.last_hit = pygame.time.get_ticks()
                player.defend(5)
            
            fireball_cooldown = 500

            if self.boss:
                if player_distance < 500:
                    if pygame.time.get_ticks() - self.last_attack >= fireball_cooldown:
                        fireball = Fireball(fireball_image, self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
                        self.last_attack = pygame.time.get_ticks()
        elif (pygame.time.get_ticks() - self.stunned_time) > stun_cooldown:
            self.stunned = False
            
        return fireball
    
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
        
        if self.char_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - OFFSET * SCALE))
        else:
            surface.blit(flipped_image, self.rect)

        if COLLIDE_RECT:
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