import pygame 
import sys
from bg import * 

class PlaneGame(object): 

    def __init__(self): 
        print("游戏初始化")

        #创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        #创建游戏的时钟
        self.clock = pygame.time.Clock()
        #调用私有方法，精灵和精灵组的创建
        self.__create_sprites()

    def __create_sprites(self): 

        #创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(is_alt=True)

        self.back_group = pygame.sprite.Group(bg1,bg2)

    def start_game(self): 
        print("游戏开始")

        while True: 
            #设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            #事件监听
            self.__event_handler()
            #碰撞检测
            self.__check_collide()
            #更新/绘制精灵组
            self.__update_sprites()
            #更新显示
            pygame.display.update()

    def __event_handler(self): 

        for event in pygame.event.get(): 

            #判断是否退出游戏
            if event.type == pygame.QUIT: 
                PlaneGame.__game_over()
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_q: 
                    sys.exit()
    
    def __check_collide(self): 
        pass 

    def __update_sprites(self): 

        self.back_group.update()
        self.back_group.draw(self.screen)

    def __game_over(): 
        print("游戏结束")

        pygame.quit()
        exit()

if __name__ == '__main__': 

    #创建游戏对象
    game = PlaneGame()

    #启动游戏
    game.start_game()