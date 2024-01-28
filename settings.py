class Settings:
    def __init__(self) -> None:
        
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_bg_color = (230, 230, 230)
        
        # 飞船设置
        self.ship_limit = 3
        
        # 子弹设置
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3
        
        # 外星人设置
        self.fleet_drop_speed = 10
        
        # 速度和分数等的增长规模
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        ''' 初始化随游戏进行而变化的设置 '''
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.5
        self.fleet_direction = 1    # 1表示向右，-1表示向左
        
        # 击杀每个外星人得分
        self.alien_points = 50
        
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_allowed += 1
        self.bullet_width += 5
        self.alien_points = int(self.score_scale * self.alien_points)