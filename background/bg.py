import pygame 

#屏幕大小的常量
SCREEN_RECT = pygame.Rect(0,0,1536,2304)
#设置刷新的帧率
FRAME_PER_SEC = 60

class GameSprite(pygame.sprite.Sprite): 
    def __init__(self, image_name, speed=1): 
        #调用父类的初始化方法
        super().__init__()

        #定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed 

    def update(self): 

        #在屏幕垂直方向上移动
        self.rect.y += self.speed 

class Background(GameSprite): 
    """游戏背景精灵"""

    def __init__(self, is_alt=False): 
        #调用父类方法实现精灵的创建
        super().__init__("./background/background5.JPG")

        #判断是否交替图像，如果是，需要设置初始位置
        if is_alt: 
            self.rect.y = -self.rect.height

    def update(self): 
        #调用父类方法:垂直移动
        super().update()

        #判断是否移出屏幕，若移出屏幕，应该将图像设置到图像上方
        if self.rect.y >= SCREEN_RECT.height: 
            self.rect.y = -self.rect.height 
