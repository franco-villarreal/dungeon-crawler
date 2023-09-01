import pygame
import csv

from constants import COLS, GRID, FONT_SIZE, ITEM_SCALE, POTION_SCALE, RED, ROWS, SCREEN_HEIGHT, SCREEN_WIDTH, FPS, SCALE, SPEED, BACKGROUND_COLOR, TILE_SIZE, TILE_TYPES, UI_COLOR, WEAPON_SCALE, WHITE
from character import Character
from item import Item
from weapon import Weapon
from world import World

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

clock = pygame.time.Clock()
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", FONT_SIZE)
level = 1
screen_scroll = [0, 0]
moving_left = False
moving_right = False
moving_up = False
moving_down = False

def scale_img(image, scale):
    width = image.get_width()
    height = image.get_height()

    return pygame.transform.scale(image, (width * scale, height * scale))

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

map = []
for row in range(ROWS):
    r = [-1] * COLS
    map.append(r)

with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for y, row in enumerate(reader):
        for x, col in enumerate(row):
            map[y][x] = int(col)

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

world = World()
world.map(map, tiles, items_images, chars_animations)

player = world.player
enemies = world.enemies
bow = Weapon(bow_image, arrow_image)

arrow_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
ui_item_group = pygame.sprite.Group()

ui_coin = Item(SCREEN_WIDTH - 115, 23, 0, coin_images)
ui_item_group.add(ui_coin)

for item in world.items:
    item_group.add(item)

# Game Loop
run = True
while run:
    clock.tick(FPS)
    screen.fill(BACKGROUND_COLOR)

    if GRID:
        draw_grid()

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

    screen_scroll = player.move(dx, dy, world.obstacle_tiles)

    world.update(screen_scroll)
    player.update()
    arrow = bow.update(player)

    if arrow:
        arrow_group.add(arrow)

    world.draw(screen)
    player.draw(screen)    
    bow.draw(screen)

    for enemy in enemies:
        enemy.ai(screen_scroll)
        enemy.update()
        enemy.draw(screen)

    for arrow in arrow_group:
        damage, damage_pos = arrow.update(screen_scroll, enemies)
        if damage > 0 and damage_pos:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), RED)
            damage_text_group.add(damage_text)
        arrow.draw(screen)

    damage_text_group.update(screen_scroll)
    damage_text_group.draw(screen)

    item_group.update(player, screen_scroll)
    item_group.draw(screen)

    draw_ui(player)

    ui_item_group.update(player)
    ui_item_group.draw(screen)

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