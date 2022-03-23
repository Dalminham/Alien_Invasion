import pygame 

class Settings:
    """存储游戏中所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        #天蓝色
        self.bg_color = (193, 210, 240)

        #飞船设定
        self.ship_limit = 3

        #子弹设置
        self.bullet_width = 10 
        self.bullet_height = 30 
        self.bullet_color = (255, 215, 0)
        self.bullets_allowed = 3

        #外星人设置
        self.fleet_drop_speed = 5
        #fleet_direction 为1表示向右移， 为-1表示向左移
        self.fleet_direction = 1

        #爆炸时间 
        self.bomb_time = 2

        #加快游戏节奏
        self.speedup_scale = 1.1 

        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self): 
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.5 
        self.bullet_speed = 3.0 
        self.alien_speed = 1.0 

        #fleet_direction 为1表示向右， 为-1表示向左。
        self.fleet_direction = 1

        #记分
        self.alien_points = 50
    
    def increase_speed(self): 
        """提高速度设置"""
        self.ship_speed *= self.speedup_scale 
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale



