import pygame
import os

class GameStats:
    def __init__(self, ai_game) -> None:
        ''' 初始化 '''
        self.settings = ai_game.settings
        
        # 最高记录
        try:
            with open('record.txt', 'r') as f:
                score = f.readline()
        except:
            score = 0
            
        self.high_score = int(score)
        self.level = 1
        self.game_active = False
        self.reset_stats()
    
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0