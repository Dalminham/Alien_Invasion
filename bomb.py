import pygame 
from pygame.sprite import Sprite 

class Bomb(Sprite):
    """管理飞船所发射子弹的类"""

    def __init__(self, ai_game, pos = (0,0), time = 0): 
        """在当前飞船创建一个子弹对象"""
        super().__init__() #继承父类的init方法
        self.screen = ai_game.screen 
        self.settings = ai_game.settings 
        self.color = self.settings.bullet_color
        self.bomb_img = pygame.image.load('images/bomb.png')
        self.bomb_img.set_colorkey((255,255,255))

        #在(0,0)处创建一个一个表示子弹的矩形，再设置正确的位置
        self.rect = self.bomb_img.get_rect()
        self.rect.center = pos
        self.time = time

        #存储用小数表示的子弹位置。
    
    def update(self): 
        pass
    
    def draw_bomb(self): 
        """在屏幕上绘制子弹"""
        self.screen.blit(self.bomb_img, self.rect)




