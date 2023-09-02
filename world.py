from character import Character
from constants import PLAYER_INITIAL_HEALTH, TILE_SIZE
from item import Item


class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []
        self.exit_tile = None
        self.items = []
        self.player = None
        self.enemies = []

    def map(self, map, tiles, item_animations, char_animations):
        self.level_length = len(map)
        for y, row in enumerate(map):
            for x, col in enumerate(row):
                image = tiles[col]
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
                        coin = Item(image_x, image_y, 0, item_animations[0])
                        self.items.append(coin)
                        tile[0] = tiles[0]
                    if col == 10:
                        red_potion = Item(image_x, image_y, 1, item_animations[1])
                        self.items.append(red_potion)
                        tile[0] = tiles[0]
                    if col == 11:
                        char_type = 0
                        player = Character(x=image_x, y=image_y, health=PLAYER_INITIAL_HEALTH, max_health=100,char_type=char_type, animations=char_animations[char_type])
                        self.player = player
                        tile[0] = tiles[0]
                    if col >= 12 and col <= 16:
                        char_type = col - 11
                        enemy = Character(x=image_x, y=image_y, health=100, max_health=100,char_type=char_type, animations=char_animations[char_type])
                        self.enemies.append(enemy)
                        tile[0] = tiles[0]
                    if col == 17:
                        char_type = col - 11
                        enemy = Character(x=image_x, y=image_y, health=100, max_health=100,char_type=char_type, animations=char_animations[char_type], boss=True)
                        self.enemies.append(enemy)
                        tile[0] = tiles[0]
    
    def update(self, screen_scroll=[0,0]):
        for tile in self.map_tiles:
            print(tile[2])
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])