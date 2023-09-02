import pygame
from pygame import mixer
import csv
from button import Button
from constants import BLACK, BUTTON_SCALE, COLS, FIREBALL_SCALE, GRID, FONT_SIZE, ITEM_SCALE, MENU_COLOUR, PINK, POTION_SCALE, RED, ROWS, SCREEN_HEIGHT, SCREEN_WIDTH, FPS, SCALE, SPEED, BACKGROUND_COLOR, TILE_SIZE, TILE_TYPES, UI_COLOR, WEAPON_SCALE, WHITE
from item import Item
from weapon import Weapon
from world import World

mixer.init()
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

clock = pygame.time.Clock()
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", FONT_SIZE)
level = 1
start_game = False
pause_game = False
start_intro = False
screen_scroll = [0, 0]
moving_left = False
moving_right = False
moving_up = False
moving_down = False

def scale_img(image, scale):
    width = image.get_width()
    height = image.get_height()

    return pygame.transform.scale(image, (width * scale, height * scale))

# Load music and sounds
pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
shot_fx =pygame.mixer.Sound("assets/audio/arrow_shot.mp3")
shot_fx.set_volume(0.5)
hit_fx =pygame.mixer.Sound("assets/audio/arrow_hit.wav")
hit_fx.set_volume(0.5)
coin_fx =pygame.mixer.Sound("assets/audio/coin.wav")
coin_fx.set_volume(0.5)
heal_fx =pygame.mixer.Sound("assets/audio/heal.wav")
heal_fx.set_volume(0.5)
# Load characters images
char_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]
chars_animations = []
char_animation_types = ["idle", "run"]

for char in char_types:
    char_animations = []
    for animation in char_animation_types:
        char_animation = []

        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{char}/{animation}/{i}.png").convert_alpha()
            img = scale_img(img, SCALE)
            char_animation.append(img)

        char_animations.append(char_animation)

    chars_animations.append(char_animations)

# Load weapon images
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), WEAPON_SCALE)
fireball_image = scale_img(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(), FIREBALL_SCALE)

# Load button images
start_button_image = scale_img(pygame.image.load("assets/images/buttons/button_start.png").convert_alpha(), BUTTON_SCALE)
exit_button_image = scale_img(pygame.image.load("assets/images/buttons/button_exit.png").convert_alpha(), BUTTON_SCALE)
resume_button_image = scale_img(pygame.image.load("assets/images/buttons/button_resume.png").convert_alpha(), BUTTON_SCALE)
restart_button_image = scale_img(pygame.image.load("assets/images/buttons/button_restart.png").convert_alpha(), BUTTON_SCALE)

# Load heart images
empty_heart = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), ITEM_SCALE)
half_heart = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), ITEM_SCALE)
full_heart = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), ITEM_SCALE)

# Load coin images
coin_images = []
for i in range(4):
    img = scale_img(pygame.image.load(f"assets/images/items/coin_f{i}.png").convert_alpha(), ITEM_SCALE)
    coin_images.append(img)

# Load potion image
red_potion_images = [scale_img(pygame.image.load(f"assets/images/items/potion_red.png").convert_alpha(), POTION_SCALE)]

items_images = []
items_images.append(coin_images)
items_images.append(red_potion_images)

# Load map tiles
tiles = []
for x in range(TILE_TYPES):
    tile = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
    tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
    tiles.append(tile)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def draw_grid():
    for x in range(30):
        pygame.draw.line(screen, WHITE, (x * TILE_SIZE, 0), (x * TILE_SIZE, SCREEN_HEIGHT))
        pygame.draw.line(screen, WHITE, (0, x * TILE_SIZE), (SCREEN_WIDTH, x * TILE_SIZE))

def draw_ui(player):
    # Draw UI panel
    pygame.draw.rect(screen, UI_COLOR, (0, 0, SCREEN_WIDTH, 50))
    pygame.draw.line(screen, WHITE, (0, 50), (SCREEN_WIDTH, 50))

    half_heart_drawn = False
    for i in range(5):
        pos = (10 + i * 50, 0)
        if player.health >= ((i + 1) * 20):
            screen.blit(full_heart, pos)
        elif (player.health % 20 > 0) and half_heart_drawn == False:
            half_heart_drawn = True
            screen.blit(half_heart, pos)
        else:
            screen.blit(empty_heart, pos)
    draw_text(f"LEVEL: {str(level)}", font, WHITE, SCREEN_WIDTH / 2, 15)
    draw_text(f"X{player.total_score}", font, WHITE, SCREEN_WIDTH - 100, 15)

def load_map():
    map = []
    for row in range(ROWS):
        r = [-1] * COLS
        map.append(r)

    with open(f"levels/level{level}_data.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for y, row in enumerate(reader):
            for x, col in enumerate(row):
                map[y][x] = int(col)
    
    world = World()
    world.map(map, tiles, items_images, chars_animations)

    return world

def reload_map():
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()

    return load_map()

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

class ScreenFade():
    def __init__(self, colour, speed):
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0
    
    def fade_in(self):
        completed = False
        self.fade_counter += self.speed
      
        pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
    
        if self.fade_counter >= SCREEN_WIDTH:
            completed = True

        return completed
    
    def fade_out(self):
        completed = False
        self.fade_counter += self.speed

        pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))

        if self.fade_counter >= SCREEN_WIDTH:
            completed = True

        return completed
    
world = load_map()

player = world.player
enemies = world.enemies
bow = Weapon(bow_image, arrow_image)

arrow_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
ui_item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

ui_coin = Item(SCREEN_WIDTH - 115, 23, 0, coin_images)
ui_item_group.add(ui_coin)

for item in world.items:
    item_group.add(item)

intro_fade_in = ScreenFade(BLACK, 4)
death_fade_out = ScreenFade(PINK, 4)
start_button = Button(SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 2 - 150, start_button_image)
exit_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_button_image)
resume_button = Button(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 - 150, resume_button_image)
restart_button = Button(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 - 50, restart_button_image)

# Game Loop
run = True
while run:
    clock.tick(FPS)

    if not start_game:
        screen.fill(MENU_COLOUR)
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
            screen.fill(BACKGROUND_COLOR)

            if GRID:
                draw_grid()

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

            draw_ui(player)

            ui_item_group.update(player)
            ui_item_group.draw(screen)

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
                if intro_fade_in.fade_in():
                    start_intro = False
                    intro_fade_in.fade_counter = 0
            
            if not player.alive:
                if death_fade_out.fade_out():
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