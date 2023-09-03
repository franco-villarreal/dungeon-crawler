import os, sys
import pygame

def build_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def scale_img(image, scale):
    width = image.get_width()
    height = image.get_height()

    return pygame.transform.scale(image, (width * scale, height * scale))