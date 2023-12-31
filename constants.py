
import pyautogui

screen_width, screen_height = pyautogui.size()

if screen_width > 1920:
    screen_width = 1920
if screen_height > 1080:
    screen_height = 1080


CAPTION = "Dungeon Crawler"
FPS = 60
SCREEN_WIDTH = screen_width
SCREEN_HEIGHT = screen_height
SCALE = 3
WEAPON_SCALE = 1.5
ITEM_SCALE = 3
POTION_SCALE = 2
FIREBALL_SCALE = 1
BUTTON_SCALE = 1
SPEED = 5
ARROW_SPEED = 10
ENEMY_SPEED = 4
FIREBALL_SPEED = 2
OFFSET = 12
FONT_SIZE = 20
TILE_SIZE = 16 * SCALE
TILE_TYPES = 18
ROWS = 150
COLS = 150
SCROLL_THRESH = 200
RANGE = 50
ATTACK_RANGE = 60
PLAYER_INITIAL_HEALTH = 75

SHOW_GRID = False
SHOW_COLLIDE_RECT = False
