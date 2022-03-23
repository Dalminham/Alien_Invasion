import pygame
from time import sleep

class Mario:
    """管理马里奥的类"""
    def __init__(self, ai_game):
        self.status = 1
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #加载马里奥图像并获取外接矩阵
        self.right_image = pygame.image.load('images/right_mario.bmp')
        self.left_image = pygame.image.load('images/left_mario.bmp')
        self.right_image.set_colorkey((255,255,255))
        self.left_image.set_colorkey((255,255,255))
        self.right_image_n = pygame.image.load('images/right_mario_new.bmp')
        self.right_image_n.set_colorkey((255,255,255))
        self.left_image_n = pygame.image.load('images/left_mario_new.bmp')
        self.left_image_n.set_colorkey((255,255,255))
        self.rect = self.right_image.get_rect()

        #将马里奥放到屏幕中央
        self.rect.center = self.screen_rect.center

        #储存马里奥的位置
        self.x = float(self.rect.x)

        #马力奥移动方向：
        self.direction = 0

        #马里奥动作帧切换：
        self.img_cho = 1
    
    def update(self): 
        if self.rect.right < self.screen_rect.right and self.direction == 0 : 
            self.x += 3
            self.direction = 0
        else: 
            self.direction = 1
        if self.rect.left > self.screen_rect.left and self.direction == 1 : 
            self.x -= 3
            self.direction = 1 
        else: 
            self.direction = 0
        self.rect.x = self.x 
        



    def blitme(self): 
        """在指定位置绘制马里奥"""
        if self.direction == 0:
            if self.img_cho == 1:
                self.screen.blit(self.right_image, self.rect)
            elif self.img_cho == 0: 
                self.screen.blit(self.right_image_n, self.rect)
        elif self.direction == 1: 
            if self.img_cho == 1:
                self.screen.blit(self.left_image, self.rect)
            elif self.img_cho == 0: 
                self.screen.blit(self.left_image_n, self.rect)
        self.img_cho = (self.img_cho + 1) % 2
        