import pygame
from button import Button
from colours import GREY, LIGHT_BLACK, WHITE
from constants import FONT_SIZE, GRID, ITEM_SCALE, SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from utils import build_path, scale_img

class UiManager():
    def __init__(self) -> None:
        self.font = pygame.font.Font(build_path("assets/fonts/AtariClassic.ttf"), FONT_SIZE)
        self.empty_heart = scale_img(pygame.image.load(build_path("assets/images/items/heart_empty.png")).convert_alpha(), ITEM_SCALE)
        self.half_heart = scale_img(pygame.image.load(build_path("assets/images/items/heart_half.png")).convert_alpha(), ITEM_SCALE)
        self.full_heart = scale_img(pygame.image.load(build_path("assets/images/items/heart_full.png")).convert_alpha(), ITEM_SCALE)
        self.coin = scale_img(pygame.image.load(build_path("assets/images/items/coin_f0.png")).convert_alpha(), ITEM_SCALE)
        self.start_button = Button(SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 2 - 150, "assets/images/buttons/button_start.png")
        self.exit_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, "assets/images/buttons/button_exit.png")
        self.resume_button = Button(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 - 150, "assets/images/buttons/button_resume.png")
        self.restart_button = Button(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 - 50, "assets/images/buttons/button_restart.png")

    def draw_text(self, surface, text, text_color, x, y):
        img = self.font.render(text, True, text_color)
        surface.blit(img, (x, y))

    def draw_ui(self, surface, current_level, player_health, player_score):
        if GRID:
            for x in range(30):
                pygame.draw.line(surface, WHITE, (x * TILE_SIZE, 0), (x * TILE_SIZE, SCREEN_HEIGHT))
                pygame.draw.line(surface, WHITE, (0, x * TILE_SIZE), (SCREEN_WIDTH, x * TILE_SIZE))
        
        pygame.draw.rect(surface, GREY, (0, 0, SCREEN_WIDTH, 50))
        pygame.draw.line(surface, WHITE, (0, 50), (SCREEN_WIDTH, 50))

        half_heart_drawn = False
        for i in range(5):
            pos = (10 + i * 50, 0)
            if player_health >= ((i + 1) * 20):
                surface.blit(self.full_heart, pos)
            elif (player_health % 20 > 0) and half_heart_drawn == False:
                half_heart_drawn = True
                surface.blit(self.half_heart, pos)
            else:
                surface.blit(self.empty_heart, pos)
        
        surface.blit(self.coin, (SCREEN_WIDTH - 125, 10))
        self.draw_text(surface, f"LEVEL: {str(current_level)}", WHITE, SCREEN_WIDTH / 2, 15)
        self.draw_text(surface, f"X{player_score}", WHITE, SCREEN_WIDTH - 100, 15)
    
    def draw_start_menu(self, surface):
        surface.fill(LIGHT_BLACK)
        if self.start_button.draw(surface):
            return "START"
        if self.exit_button.draw(surface):
            return "EXIT"
    
    def draw_pause_menu(self, surface):
        if self.resume_button.draw(surface):
            return "RESUME"
        if self.exit_button.draw(surface):
            return "EXIT"
        
    def draw_restart_menu(self, surface):
        if self.restart_button.draw(surface):
            return "RESTART"
        