import pygame
import sys
from pygame.sprite import Sprite 
class GameSprite(Sprite):
    def __init__ (self, filename, frames = 1):
        super().__init__() #继承父类的init方法
        self.images = []
        img = pygame.image.load(filename)
        self.original_width = img.get_width() // frames
        self.original_height = img.get_height()
        frame_surface = pygame.Surface([self.original_width, self.original_height])
        x = 0
        for frame_no in range(frames):
            frame_surface = pygame.Surface([self.original_width, self.original_height])
            frame_surface.blit(img, [x,0])
            self.images.append(frame_surface.copy())
            x -= self.original_width
        self.image = self.images[0]
        self.current_index = 0
        self.rect=self.image.get_rect()
    def move(self, pos_X, pos_Y):
        self.rect.center = [pos_X, pos_Y]

    def change_image(self, index):
        self.current_index = index
        self.image = self.images[index]
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter
    
    def run_action(self,direction): 
        

aml = GameSprite('total_mario.bmp',7)
screen = pygame.display.set_mode((1200,800))
while True: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_RIGHT: 
                aml.change_image(2)
                screen.blit(aml.image, aml.rect)
            elif event.key == pygame.K_a: 
                aml.change_image(3)
    pygame.display.flip()
    screen.blit(aml.image, aml.rect)