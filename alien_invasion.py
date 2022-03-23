import imp
import sys
from time import sleep
from math import ceil
from background.bg import *

import pygame
from pygame.time import get_ticks
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

from ship import Ship
from mario import Mario
from bullet import Bullet
from alien import Alien
from tips import Tips
from bomb import Bomb



class AlienInvasion:
    """管理游戏资源和行为"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #窗口尺寸
        self.screen_rect = self.screen.get_rect()
        self.settings.screen_height = self.screen.get_rect().height 
        self.settings.screen_width = self.screen.get_rect().width
        pygame.display.set_caption("Alien Invasion")
        #设置背景
        self._bg_sprites()

        #创建一个用于存储游戏统计信息的实例。
        self.stats = GameStats(self)
        #创建计分板
        self.sb = Scoreboard(self)


        self.ship = Ship(self)

        self.ship = Ship(self)
        self.mario = Mario(self)
        self.tips = Tips(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bomb = pygame.sprite.Group()

        self._create_fleet()

        #创建Play按钮
        self.play_button = Button(self,"Play")


    def _check_events(self):
        """响应按键和鼠标事件"""   
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit() 
                elif event.type == pygame.KEYDOWN: 
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP: 
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
    
    def _check_keydown_events(self, event): 
        """响应按键"""
        if event.key == pygame.K_RIGHT: 
            #向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT: 
            #向左移动飞船
            self.ship.moving_left = True
        elif event.key == pygame.K_UP: 
            self.ship.moving_up = True 
        elif event.key == pygame.K_DOWN: 
            self.ship.moving_down = True
        elif event.key == pygame.K_q: 
            sys.exit()
        elif event.key == pygame.K_SPACE: 
            self._fire_bullet()
        elif event.key == pygame.K_r: 
            self.ship.change_fly = True
    
    
    def _check_keyup_events(self, event): 
        """响应松开"""
        if event.key == pygame.K_RIGHT: 
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT: 
            self.ship.moving_left = False
        if event.key == pygame.K_UP: 
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN: 
            self.ship.moving_down = False
        elif event.key == pygame.K_r: 
            self.ship.change_fly = False

    def _check_play_button(self, mouse_pos): 
        """在玩家单击play按钮时开始新的游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active: 
            #重置游戏统计信息。
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True 
            print("Start Game")
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人并让飞船居中。
            self._create_fleet()
            self.ship.center_ship()

            #隐藏鼠标光标
            pygame.mouse.set_visible(False)


    def _fire_bullet(self): 
        """创建一颗子弹,并将其加入编组bullets中。"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self) 
            self.bullets.add(new_bullet)
    
    def _update_bullets(self): 
        """更新子弹位置并删除消失的子弹。"""
        #更新子弹位置
        self.bullets.update()
        #删除消失的子弹
        for bullet in self.bullets.copy(): 
                if bullet.rect.bottom <= 0: 
                    self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
    
    def _update_bomb(self): 
        """更新爆炸位置并删除"""
        time = get_ticks()
        for bomb in self.bomb.copy(): 
            if time - bomb.time > 500: 
                self.bomb.remove(bomb)
         
        

    def _check_bullet_alien_collisions(self): 
        """响应子弹和外星人碰撞"""
        #删除发生碰撞的子弹和外星人

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)  
        if collisions: 
            for bullet, alien in collisions.items():
                self.bullets.remove(bullet)
                self.aliens.remove(alien)
            time = get_ticks()
            new_bomb = Bomb(self,(bullet.rect.x, bullet.rect.y),time)
            self.bomb.add(new_bomb)
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens: 
            #删除现有的子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()    
            self.settings.increase_speed()   

            #提高等级
            self.stats.level += 1 
            self.sb.prep_level() 
    
    def _create_fleet(self): 
        """创建外星人群"""
        #创建一个外星人并计算一行可以容纳多少个外星人
        #外星人的间距为外星人宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width) - 1

        #计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height 
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height) - 1

        #创建第一行外星人
        for row_number in range(number_rows): 
            #self._create_alien(number_aliens_x - row_number, row_number)
            alien_num = number_aliens_x - row_number
            if (number_aliens_x - row_number)%2 == 0: 
                odd = False
            else:
                odd = True 
            for alien_number in range(alien_num ):
                #创建外星人群
                self._create_alien(alien_number,row_number, odd)
    

    def _create_alien(self, alien_number, row_number, odd = False): 
        """创建一个外星人并将其放在当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        half_width = alien_width/2
        #alien.x = alien_width + 2 * alien_width * alien_number
        if odd:
            alien.x = self.screen_rect.centerx - alien_width + alien_width * ceil(alien_number/2) * (-1)**(alien_number)
        else: 
            alien.x = self.screen_rect.centerx - half_width + alien_width * ceil(alien_number/2) * (-1)**(alien_number)
        alien.rect.x = alien.x 
        alien.rect.y = 2*alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    


    def _check_fleet_edges(self): 
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites(): 
            if alien.check_edges(): 
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self): 
        """将整群外星人下移，并改变它们的方向"""
        for alien in self.aliens.sprites(): 
            alien.rect.y += self.settings.fleet_drop_speed 
        self.settings.fleet_direction *= -1


    def _update_aliens(self): 
        """更新外星人群中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        #检测外星人和飞船之间的碰撞。
        if pygame.sprite.spritecollideany(self.ship, self.aliens): 
            self._ship_hit()

        
        #检查是否有外星人到达了屏幕底端。
        self._check_aliens_bottom()
    

    def _check_aliens_bottom(self): 
        """检查是否有外星人到达了屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites(): 
            if alien.rect.bottom >= screen_rect.bottom: 
                #像飞船被撞到一样处理
                self._ship_hit()
                break


    def _ship_hit(self): 
        """响应飞船被外星人撞到"""

        if self.stats.ships_left > 0:
            print("Ship Hit!")
            #将ship_left 减为1
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人，并将飞船放到屏幕底端的中央
            self._create_fleet()
            self.ship.center_ship()

            #暂停
            sleep(0.5)
        else: 
            self.stats.game_active = False
            print("Ship Destroyed!")
            pygame.mouse.set_visible(True)

    #背景处理
    def _bg_sprites(self): 
        #创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(is_alt=True)

        self.back_group = pygame.sprite.Group(bg1,bg2)
    
    def _update_bg(self): 

        self.back_group.update()
        self.back_group.draw(self.screen)
    
    
    
    def _updata_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        #self.screen.fill(self.settings.bg_color)
        if self.stats.screen_active:
            #self.screen.blit(self.settings.bg_img,(0,0))
            self._update_bg()
            self.ship.blitme()
            self.tips.blitme()
            if self.sb.stats.score > 5000:
                self.mario.blitme()
            for bullet in self.bullets.sprites(): 
                bullet.draw_bullet()
            for bomb in self.bomb.sprites(): 
                bomb.draw_bomb()
            self.aliens.draw(self.screen)
            self.sb.show_score()
        self.stats.screen_active = self.stats.game_active

        #如果游戏处于非活动状态，就绘制Play按钮。
        if not self.stats.game_active: 
            self.play_button.draw_button()
        

        pygame.display.flip()

    
        

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监视键盘和鼠标事件。
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self.mario.update()
                self._update_bullets()
                self._update_aliens()
                self._update_bomb()

            self._updata_screen()
            
        
        

if __name__ == '__main__':
    #创建游戏实例并运行游戏。
    ai = AlienInvasion()
    ai.run_game()