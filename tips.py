import pygame 

class Tips:
    """提示的类"""

    def __init__(self, ai_game): 
        """初始化提示并设置其起始位置"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #加载tips图像并设置其rect属性。 
        self.image = pygame.image.load('images/tips.PNG')
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()


        #每个外星人最初都在屏幕左上角附近。
        self.rect.bottomright = self.screen_rect.bottomright
    
    def blitme(self):
        """在指定位置绘制"""
        self.screen.blit(self.image, self.rect)


    

        
