import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """管理游戏资源和行为的类"""
    
    def __init__(self) -> None:
        '''初始化并创建游戏'''
        # 屏幕初始化
        pygame.init()
        self.settings = Settings()
        
        # 非全屏
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
            )
        
        # # 全屏（貌似有点不兼容）
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
        # self.settings.screen_width = self.screen.get_rect().width 
        # self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")
        
        # 飞船
        self.ship = Ship(self)
        
        # 外星人
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        
        # 子弹
        self.bullets = pygame.sprite.Group()
    
    def _create_fleet(self):
        ''' 创建外星人星群 '''
        alien = Alien(self)
        
        # 计算一行可以放多少个外星人
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width) #计算屏幕可用宽度（余2个位置）
        number_aliens = available_space_x // (2 * alien_width)             #间隔一个位置摆一个外星人
        
        # 计算可以放多少行
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - 3 * alien_height - ship_height
        number_rows = available_space_y // (2 * alien_height)
        
        # 将外星人逐一添加到屏幕
        for row in range(number_rows):
            for alien_number in range(number_aliens):
                self._create_alien(row, alien_number)
        
    def _create_alien(self, row, alien_number):
        alien = Alien(self)
            
        # 计算坐标
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        
        alien.y = alien_height + 2 * alien_height * row
        alien.rect.y = alien.y
        
        self.aliens.add(alien)
        
    def _fire_bullet(self):
        ''' 创建一颗子弹，并把它加入到Group中 '''
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        
    def _check_keydown_event(self, event):
        ''' 辅助函数：->按下调用 '''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            
    def _check_keyup_event(self, event):
        ''' 辅助函数：->弹起调用'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    def _check_event(self):
        ''' 辅助函数：监视键盘和鼠标 '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
    
    def _update_screen(self):
        ''' 更新屏幕 '''
        
        # 每次都重新绘制颜色
        self.screen.fill(self.settings.screen_bg_color)
        
        # 每次都重新绘制飞船
        self.ship.blitme()
        
        # 每次重新绘制子弹
        for bullet in self.bullets:
            bullet.draw_bullet()
            
        # 绘制外星人
        self.aliens.draw(self.screen)
            
        # 绘制屏幕
        pygame.display.flip()
        
    def _update_bullets(self):
        # 更新子弹的位置
        self.bullets.update()
        
        # 删除越界的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
    def run_game(self):
        while True:
            # 获取鼠标键盘事件
            self._check_event()
            
            # 更新飞船的位置
            self.ship.update()
            
            # 更新子弹的位置
            self._update_bullets()
            
            # 更新屏幕绘制
            self._update_screen()
            

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()