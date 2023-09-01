import pygame

from constants import FONT_SIZE, ITEM_SCALE, POTION_SCALE, RED, SCREEN_HEIGHT, SCREEN_WIDTH, FPS, SCALE, SPEED, BACKGROUND_COLOR, UI_COLOR, WEAPON_SCALE, WHITE
from character import Character
from item import Item
from weapon import Weapon

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

clock = pygame.time.Clock()
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", FONT_SIZE)

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
red_potion_image = scale_img(pygame.image.load(f"assets/images/items/potion_red.png").convert_alpha(), POTION_SCALE)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

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
    
    draw_text(f"X{player.total_score}", font, WHITE, SCREEN_WIDTH - 100, 15)

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

player_char_type = 0
player = Character(x=100, y=100, health=80, max_health=100,char_type=player_char_type, animations=chars_animations[player_char_type])
bow = Weapon(bow_image, arrow_image)

enemy = Character(x=200, y=200, health=100, max_health=100, char_type=1, animations=chars_animations[1])

enemies = []
arrow_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
ui_item_group = pygame.sprite.Group()

enemies.append(enemy)

ui_coin = Item(SCREEN_WIDTH - 115, 23, 0, coin_images)
ui_item_group.add(ui_coin)

potion = Item(200, 200, 1, [red_potion_image])
item_group.add(potion)

coin = Item(400, 400, 0, coin_images)
item_group.add(coin)

# Game Loop
run = True
while run:
    clock.tick(FPS)
    screen.fill(BACKGROUND_COLOR)
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

    player.move(dx, dy)

    player.update()
    arrow = bow.update(player)

    if arrow:
        arrow_group.add(arrow)

    player.draw(screen)    
    bow.draw(screen)

    for enemy in enemies:
        enemy.update()
        enemy.draw(screen)

    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemies)
        if damage > 0 and damage_pos:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), RED)
            damage_text_group.add(damage_text)
        arrow.draw(screen)

    damage_text_group.update()
    damage_text_group.draw(screen)

    item_group.update(player)
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