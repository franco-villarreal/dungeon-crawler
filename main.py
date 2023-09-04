import pygame
from audio_manager import AudioManager
from constants import CAPTION, SCREEN_HEIGHT, SCREEN_WIDTH, FPS, SPEED
from colours import BLACK, RED, PINK, LIGHT_BLACK
from damage_text import DamageText
from fader import Fader
from ui_manager import UiManager
from weapon import Bow
from world import World

pygame.init()
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
audio_manager = AudioManager()
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
world = World()
world.load_map(current_level=level)
player = world.player
enemies = world.enemies
bow = Bow()
arrow_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

for item in world.items:
    item_group.add(item)

def reload_world():
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()
    world = World()
    world.load_map(current_level=level)

    return world

def handle_move():
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

    return dx, dy

run = True
while run:
    clock.tick(FPS)

    if not start_game:
        option = ui_manager.draw_start_menu(screen)
        if option == "START":
            start_game = True
            start_intro = True
        if option == "EXIT":
            run = False
    else:
        if pause_game:
            option = ui_manager.draw_pause_menu(screen)
            if option == "RESUME":
                pause_game = False
            if option == "EXIT":
                run = False
        else:
            screen.fill(LIGHT_BLACK)
            if player.alive:
                dx, dy = handle_move()
                screen_scroll, level_completed = player.move(dx, dy, world.obstacle_tiles, world.exit_tile)
                world.update(screen_scroll)
                player.update()
                arrow = bow.update(player)

                if arrow:
                    audio_manager.shot_fx.play()
                    arrow_group.add(arrow)
            else:
                if ui_manager.fade_out(screen):
                    option = ui_manager.draw_restart_menu(screen)
                    if option == "RESTART":
                        ui_manager.reset_faders()
                        start_intro = True
                        world = reload_world()
                        player = world.player
                        enemies = world.enemies

                        for item in world.items:
                            item_group.add(item)
            world.draw(screen)
            player.draw(screen)
            bow.draw(screen)

            for enemy in enemies:
                fireball = enemy.ai(player, world.obstacle_tiles, screen_scroll)
                if fireball:
                    fireball_group.add(fireball)
                enemy.update()
                enemy.draw(screen)

            for arrow in arrow_group:
                damage, damage_pos = arrow.update(screen_scroll, world.obstacle_tiles, enemies)
                if damage > 0 and damage_pos:
                    audio_manager.hit_fx.play()
                    damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), RED)
                    damage_text_group.add(damage_text)
                arrow.draw(screen)

            damage_text_group.update(screen_scroll)
            damage_text_group.draw(screen)
            item_group.update(player, screen_scroll, [audio_manager.coin_fx, audio_manager.heal_fx])
            item_group.draw(screen)
            fireball_group.update(screen_scroll, world.obstacle_tiles, player)
            fireball_group.draw(screen)
            ui_manager.draw_ui(surface=screen, current_level=level, player_health=player.health, player_score=player.total_score)

            if level_completed:
                start_intro = True
                level += 1
                temp_player_score = player.total_score
                temp_player_health= player.health
                world = reload_world()
                player = world.player
                player.total_score = temp_player_score
                player.health = temp_player_health
                enemies = world.enemies

                for item in world.items:
                    item_group.add(item)
            
            if start_intro:
                if ui_manager.fade_in(screen):
                    ui_manager.reset_faders()
                    start_intro = False
            
            if not player.alive:
                if ui_manager.fade_out(screen):
                    option = ui_manager.draw_restart_menu(screen)
                    if option == "RESTART":
                        ui_manager.reset_faders()
                        start_intro = True
                        world = reload_world()
                        player = world.player
                        enemies = world.enemies

                        for item in world.items:
                            item_group.add(item)

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