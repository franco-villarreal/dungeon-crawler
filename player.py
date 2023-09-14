from character import Character
from constants import OFFSET, SCALE, SCREEN_HEIGHT, SCROLL_THRESH


class Player(Character):
    def __init__(self, x, y, health, max_health, char_type):
        super().__init__(x, y, health, max_health, char_type)
        self.total_score = 0

    def calculate_offset(self):
        screen_scroll = [0, 0]
        left_offset = SCROLL_THRESH
        right_offset = (SCREEN_HEIGHT - SCROLL_THRESH)
        top_offset = SCROLL_THRESH
        bottom_offset = (SCREEN_HEIGHT - SCROLL_THRESH)

        if self.rect.left < left_offset:
            screen_scroll[0] = left_offset - self.rect.left
            self.rect.left = left_offset
        if self.rect.right > right_offset:
            screen_scroll[0] = right_offset - self.rect.right
            self.rect.right = right_offset

        if self.rect.top < top_offset:
            screen_scroll[1] = top_offset - self.rect.top
            self.rect.top = top_offset
        if self.rect.bottom > bottom_offset:
            screen_scroll[1] = bottom_offset - self.rect.bottom
            self.rect.bottom = bottom_offset

        return screen_scroll

    def get_draw_coordinates(self):
        return (self.rect.x, self.rect.y - OFFSET * SCALE)

    def score(self, points):
        self.total_score += points
