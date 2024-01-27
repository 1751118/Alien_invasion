import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    ''' 管理子弹发射的类 '''
    def __init__(self, ai_game) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        
        # 在（0，0）处创建一个矩形子弹，再设置正确的位置（飞船的位置）
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # 子弹的位置
        self.y = float(self.rect.y)
        
    def update(self):
        ''' 更新子弹位置 '''
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
        
    def draw_bullet(self):
        ''' 绘制子弹 '''
        pygame.draw.rect(self.screen, self.color, self.rect)