import pygame
from pygame import mixer

from utils import build_path

mixer.init()

class AudioManager():
    def __init__(self) -> None:
        pygame.mixer.music.load(build_path("assets/audio/music.wav"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1, 0.0, 5000)
        self.shot_fx =pygame.mixer.Sound(build_path("assets/audio/arrow_shot.mp3"))
        self.shot_fx.set_volume(0.5)
        self.hit_fx =pygame.mixer.Sound(build_path("assets/audio/arrow_hit.wav"))
        self.hit_fx.set_volume(0.5)
        self.coin_fx =pygame.mixer.Sound(build_path("assets/audio/coin.wav"))
        self.coin_fx.set_volume(0.5)
        self.heal_fx =pygame.mixer.Sound(build_path("assets/audio/heal.wav"))
        self.heal_fx.set_volume(0.5)
