import pygame
from time import sleep
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #加载飞船图像并获取其外接矩阵
        self.normal_image = pygame.image.load('images/small_ship.bmp')
        self.small_power_img = pygame.image.load('images/small_power.bmp')
        self.mid_power_img = pygame.image.load('images/mid_power.bmp')
        self.big_power_img = pygame.image.load('images/full_power.bmp')
        self.new_fly_img = pygame.image.load('images/new_palyer.png')
        #透明背景
        self.normal_image.set_colorkey((255,255,255))
        self.small_power_img.set_colorkey((255,255,255))
        self.mid_power_img.set_colorkey((255,255,255))
        self.big_power_img.set_colorkey((255,255,255))
        self.new_fly_img.set_colorkey((0,0,0))
        #初始化飞船图层
        self.image = self.normal_image
        self.img_cho = 1
        self.rect = self.image.get_rect()

        #对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        #在飞船的属性x中存储小数值 
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        #移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.change_fly = False


    def center_ship(self): 
        """让飞船在屏幕底端居中"""
        self.rect.midbottom = self.screen_rect.midbottom 
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self): 
        """根据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right: 
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left: 
            self.x -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed * (self.screen_rect.bottom / self.rect.bottom)
            self.img_cho = 2
        if self.moving_up and self.rect.top > 0: 
            self.y -= self.settings.ship_speed * (self.rect.bottom / self.screen_rect.bottom)**2
            self.img_cho = 3
        if self.change_fly: 
            self.img_cho = 4
        
        self.rect.x = self.x
        self.rect.y = self.y
    


    def blitme(self):
        """在指定位置绘制飞创"""
        if self.img_cho == 0:
            self.screen.blit(self.mid_power_img, self.rect)
        elif self.img_cho == 1: 
            self.screen.blit(self.small_power_img, self.rect)
        elif self.img_cho == 2:
            self.screen.blit(self.normal_image, self.rect)
        elif self.img_cho == 3: 
            self.screen.blit(self.big_power_img, self.rect)
        elif self.img_cho == 4: 
            self.screen.blit(self.new_fly_img, self.rect)

        self.img_cho = (self.img_cho + 1) % 3
        #time.sleep(0.02)
