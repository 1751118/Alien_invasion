import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_game) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.image = pygame.image.load('./images/alien.bmp')
        self.rect = self.image.get_rect()
        
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # 外星人水平坐标
        self.x = float(self.rect.x)