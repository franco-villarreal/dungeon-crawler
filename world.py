import pygame
import csv
from constants import COLS, ITEM_SCALE, PLAYER_INITIAL_HEALTH, POTION_SCALE, ROWS, TILE_SIZE, TILE_TYPES
from enemy import Enemy
from item import Item
from player import Player
from utils import build_path, scale_img

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []
        self.exit_tile = None
        self.items = []
        self.player = None
        self.enemies = []
        self.tiles = self.load_tiles()
        self.items_animations = [self.load_coins(), self.load_potions()]

    def load_tiles(self):
        tiles = []
        for x in range(TILE_TYPES):
            tile = pygame.image.load(build_path(f"assets/images/tiles/{x}.png")).convert_alpha()
            tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
            tiles.append(tile)

        return tiles
    
    def load_coins(self):
        coin_images = []
        for i in range(4):
            img = scale_img(pygame.image.load(build_path(f"assets/images/items/coin_f{i}.png")).convert_alpha(), ITEM_SCALE)
            coin_images.append(img)

        return coin_images
    
    def load_potions(self):
        return [scale_img(pygame.image.load(build_path(f"assets/images/items/potion_red.png")).convert_alpha(), POTION_SCALE)]
    
    def load_map(self, current_level):
        map = []
        for row in range(ROWS):
            r = [-1] * COLS
            map.append(r)

        with open(build_path(f"levels/level{current_level}_data.csv"), newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for y, row in enumerate(reader):
                for x, col in enumerate(row):
                    map[y][x] = int(col)
        
        self.level_length = len(map)

        for y, row in enumerate(map):
            for x, col in enumerate(row):
                image = self.tiles[col]
                image_rect = image.get_rect()
                image_x = x * TILE_SIZE
                image_y = y * TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile = [image, image_rect, image_x, image_y]

                if col >= 0:
                    self.map_tiles.append(tile)
                    if col == 7:
                        self.obstacle_tiles.append(tile)
                    if col == 8:
                        self.exit_tile = tile
                    if col == 9:
                        coin = Item(image_x, image_y, 0, self.items_animations[0])
                        self.items.append(coin)
                        tile[0] = self.tiles[0]
                    if col == 10:
                        red_potion = Item(image_x, image_y, 1, self.items_animations[1])
                        self.items.append(red_potion)
                        tile[0] = self.tiles[0]
                    if col == 11:
                        char_type = "elf"
                        player = Player(x=image_x, y=image_y, health=PLAYER_INITIAL_HEALTH, max_health=100, char_type=char_type)
                        self.player = player
                        tile[0] = self.tiles[0]
                    if col >= 12 and col <= 16:
                        char_type = "imp" # col - 11 // Create an enum or dictionary
                        enemy = Enemy(x=image_x, y=image_y, health=100, max_health=100, char_type=char_type)
                        self.enemies.append(enemy)
                        tile[0] = self.tiles[0]
                    if col == 17:
                        char_type = "big_demon"
                        enemy = Enemy(x=image_x, y=image_y, health=100, max_health=100, char_type=char_type, boss=True)
                        self.enemies.append(enemy)
                        tile[0] = self.tiles[0]
    
        return self

    def update(self, screen_scroll=[0,0]):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])