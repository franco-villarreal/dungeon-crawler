import pygame
from pygame import mixer
import csv
from button import Button
from constants import CAPTION, COLS, FIREBALL_SCALE, FONT_SIZE, ITEM_SCALE, POTION_SCALE, ROWS, SCREEN_HEIGHT, SCREEN_WIDTH, FPS, SCALE, SPEED, TILE_SIZE, TILE_TYPES, WEAPON_SCALE
from colours import BLACK, RED, PINK, LIGHT_BLACK
from fader import Fader
from ui_manager import UiManager
from utils import build_path, scale_img
from weapon import Weapon
from world import World

mixer.init()
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(CAPTION)

clock = pygame.time.Clock()
font = pygame.font.Font(build_path("assets/fonts/AtariClassic.ttf"), FONT_SIZE)
ui_manager = UiManager()
level = 1
start_game = False
pause_game = False
start_intro = False
screen_scroll = [0, 0]
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# Load music and sounds
pygame.mixer.music.load(build_path("assets/audio/music.wav"))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
shot_fx =pygame.mixer.Sound(build_path("assets/audio/arrow_shot.mp3"))
shot_fx.set_volume(0.5)
hit_fx =pygame.mixer.Sound(build_path("assets/audio/arrow_hit.wav"))
hit_fx.set_volume(0.5)
coin_fx =pygame.mixer.Sound(build_path("assets/audio/coin.wav"))
coin_fx.set_volume(0.5)
heal_fx =pygame.mixer.Sound(build_path("assets/audio/heal.wav"))
heal_fx.set_volume(0.5)

# Load weapon images
bow_image = scale_img(pygame.image.load(build_path("assets/images/weapons/bow.png")).convert_alpha(), WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load(build_path("assets/images/weapons/arrow.png")).convert_alpha(), WEAPON_SCALE)
fireball_image = scale_img(pygame.image.load(build_path("assets/images/weapons/fireball.png")).convert_alpha(), FIREBALL_SCALE)

world = World()
world.load_map(current_level=level)

def reload_map():
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()

    world = World()
    world.load_map(current_level=level)

    return world

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self, screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

player = world.player
enemies = world.enemies
bow = Weapon(bow_image, arrow_image)

arrow_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

for item in world.items:
    item_group.add(item)

intro_fade_in = Fader(BLACK, 4)
death_fade_out = Fader(PINK, 4)
start_button = Button(SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 2 - 150, "assets/images/buttons/button_start.png")
exit_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, "assets/images/buttons/button_exit.png")
resume_button = Button(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 - 150, "assets/images/buttons/button_resume.png")
restart_button = Button(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 - 50, "assets/images/buttons/button_restart.png")

# Game Loop
run = True
while run:
    clock.tick(FPS)

    if not start_game:
        screen.fill(LIGHT_BLACK)
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    
    if start_game:
        if pause_game:
            if resume_button.draw(screen):
                pause_game = False
            if exit_button.draw(screen):
                run = False

        if not pause_game:
            screen.fill(LIGHT_BLACK)

            if player.alive:
                dx = 0
                dy = 0

                if moving_right:
                    dx = SPEED
                if moving_left:
                    dx = -SPEED
                if moving_up:
                    dy = -SPEED
                if moving_down:
                    dy = SPEED

                screen_scroll, level_completed = player.move(dx, dy, world.obstacle_tiles, world.exit_tile)
            
                world.update(screen_scroll)
                player.update()
                arrow = bow.update(player)

                if arrow:
                    shot_fx.play()
                    arrow_group.add(arrow)
                    
            world.draw(screen)
            player.draw(screen)    
            bow.draw(screen)

            for enemy in enemies:
                fireball = enemy.ai(player, world.obstacle_tiles, screen_scroll, fireball_image)
                if fireball:
                    fireball_group.add(fireball)
                enemy.update()
                enemy.draw(screen)

            for arrow in arrow_group:
                damage, damage_pos = arrow.update(screen_scroll, world.obstacle_tiles, enemies)
                if damage > 0 and damage_pos:
                    hit_fx.play()
                    damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), RED)
                    damage_text_group.add(damage_text)
                arrow.draw(screen)

            damage_text_group.update(screen_scroll)
            damage_text_group.draw(screen)

            item_group.update(player, screen_scroll, [coin_fx, heal_fx])
            item_group.draw(screen)

            fireball_group.update(screen_scroll, world.obstacle_tiles, player)
            fireball_group.draw(screen)

            ui_manager.draw_ui(surface=screen, current_level=level, player_health=player.health, player_score=player.total_score)

            if level_completed:
                start_intro = True
                level += 1
                temp_player_score = player.total_score
                temp_player_health= player.health
                world = reload_map()
                player = world.player
                player.total_score = temp_player_score
                player.health = temp_player_health
                enemies = world.enemies

                for item in world.items:
                    item_group.add(item)
            
            if start_intro:
                if intro_fade_in.fade_in(screen):
                    start_intro = False
                    intro_fade_in.fade_counter = 0
            
            if not player.alive:
                if death_fade_out.fade_out(screen):
                    if restart_button.draw(screen):
                        death_fade_out.fade_counter = 0
                        start_intro = True
                        world = reload_map()
                        player = world.player
                        enemies = world.enemies

                        for item in world.items:
                            item_group.add(item)
    #event-handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_ESCAPE:
                pause_game = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False
    
    pygame.display.update()
    
pygame.quit()