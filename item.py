import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, images):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type#0: coin, 1: health_potion
        self.images = images
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self, player, screen_scroll=[0,0], sounds=[]):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        if player.rect.colliderect(self.rect):
            if self.item_type == 0:
                sounds[0].play()
                player.score(1)
            if self.item_type == 1:
                sounds[1].play()
                player.cure(10)
            self.kill()

        animation_cooldown = 150
        self.image = self.images[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.images):
            self.frame_index = 0
    

