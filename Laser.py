from cmath import rect
from turtle import speed
import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos,speed,direction,screen_height):
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.direction = direction
        self.height_y_constraint = screen_height
        # destroy self after a certain amount of time 
        # self.init_time = pygame.time.get_ticks()
        # self. desroy_time = 2500 # 2.5s can add parameter to change this later


    def update(self):
        if self.direction==1:
            self.rect.y-=self.speed
        else: self.rect.y+=self.speed
        self.destroy()
    def destroy(self):
        if self.rect.y<=-50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

        # destroy the game object after a certain amount of time it's kinda obsolete
        # global_time = pygame.time.get_ticks()
        # if global_time - self.init_time >= self.desroy_time:
        #     self.kill()