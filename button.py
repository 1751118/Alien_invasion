import pygame.font

class Button:
    def __init__(self, ai_game, msg) -> None:
        ''' 初始化按钮 '''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        # 按钮尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        # 按钮的rect对象
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # 渲染
        self._pre_msg(msg)
        
    def _pre_msg(self, msg):
        ''' 将文本渲染成图像 '''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        ''' 绘制按钮 '''
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        
        