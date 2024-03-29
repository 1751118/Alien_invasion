import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

class AlienInvasion:
    """管理游戏资源和行为的类"""
    
    def __init__(self) -> None:
        '''初始化并创建游戏'''
        # 屏幕初始化
        pygame.init()
        self.settings = Settings()
        self.stats = GameStats(self)
        
        # 非全屏
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
            )
        
        # # 全屏（貌似有点不兼容）
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
        # self.settings.screen_width = self.screen.get_rect().width 
        # self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")
        
        # 按钮
        self.play_button = Button(self, 'Play')
        
        # 飞船
        self.ship = Ship(self)
        
        # 外星人
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        
        # 子弹
        self.bullets = pygame.sprite.Group()
        
        # 得分板
        self.scoreboard = ScoreBoard(self)
    
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
        elif event.key == pygame.K_p:
            self._check_play_button((self.play_button.rect.x, self.play_button.rect.y))
            
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        ''' 单击play按钮开始游戏 '''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #重置游戏状态
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()
            
            # 重置外星人、子弹、飞船
            self._reset()
            
            #隐藏光标
            pygame.mouse.set_visible(False)
            
            
    def _reset(self):
        # 清空外星人和弹药
        self.aliens.empty()
        self.bullets.empty()
        
        # 创建新的外星人
        self._create_fleet()
        self.ship.center_ship()
        
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
        
        # 绘制得分板
        self.scoreboard.show_score()
        
        # 绘制play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()
            
        # 绘制屏幕
        pygame.display.flip()
        
    def _update_bullets(self):
        # 更新子弹的位置
        self.bullets.update()
        # 删除越界的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alient_collisions()
        
    def _check_bullet_alient_collisions(self):
        # 检测子弹和外星人的碰撞,返回字典{bullet1: alien1, bullet2: alien2 ......} 表示碰撞的两个编组集合
        # 两个布尔值表示子弹/外星人是否会在碰撞后消失
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collision:
            for aliens in collision.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                for number in range(len(aliens)):
                    pygame.mixer.Sound("./music/hit.mp3").play()
                    
                    
            self.scoreboard.check_high_score()
            self.scoreboard.prep_score()
    
        # 检查外星人是否为空，为空则清楚现有子弹，重新创建一批外星人
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
            self.stats.level += 1
            self.scoreboard.prep_level()
            
    def _update_aliens(self):
        ''' 更新外星人位置 '''
        
        # 检查是否到边缘
        self._check_fleet_edges()
        self.aliens.update()
        
        # 检查是否碰撞飞船
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
        # 检查是否到了底部
        self._check_alien_bottom()
    
    def _ship_hit(self):
        ''' 响应飞船碰撞 '''
        # 生命值减1
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()
            self._reset()
            
            # 暂停
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            with open('./record.txt', 'w') as f:
                f.write(str(self.stats.high_score))
            
    def _check_fleet_edges(self):
        ''' 到达边缘改变方向 '''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _check_alien_bottom(self):
        ''' 检查是否到底部 '''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
                
    def _change_fleet_direction(self):
        ''' 向下移动一个然后改变方向为向左 '''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def run_game(self):
        bgm = './music/bgm.mp3'
        try:
            pygame.mixer.music.load(bgm)
        except:
            print("[Error]Can't find the background music!")
            sys.exit()
        pygame.mixer.music.play(-1)
        
        while True:
            # 获取鼠标键盘事件
            self._check_event()
            
            if self.stats.game_active:
                # 更新飞船的位置
                self.ship.update()
                
                # 更新子弹的位置
                self._update_bullets()
                
                # 更新外星人位置
                self._update_aliens()
            
            # 更新屏幕绘制
            self._update_screen()
            

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
    pygame.quit()