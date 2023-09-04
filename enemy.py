import math
import pygame
from character import Character
from constants import ATTACK_RANGE, ENEMY_SPEED, RANGE
from weapon import Fireball

class Enemy(Character):
    def __init__(self, x, y, health, max_health, char_type, boss=False):
        super().__init__(x, y, health, max_health, char_type, boss)
    
    def ai(self, player, obstacles, screen_scroll):
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
                        fireball = Fireball(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
                        self.last_attack = pygame.time.get_ticks()
        elif (pygame.time.get_ticks() - self.stunned_time) > stun_cooldown:
            self.stunned = False
            
        return fireball