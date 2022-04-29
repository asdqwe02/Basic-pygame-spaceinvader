import pygame


formation = [
    'xxxxxxxx',
    'xxxxxxxx',
    'xxxxxxxx',
    'xxxxxxxx',
    'xxxxxxxx',
    'xxxxxxxx'
]

formation2 = [
    '   xx',
    '  xxxx',
    ' xxxxxxxx',
    'xxxxxxxxxx',
    ' xxxxxxxx',
    '  xxxx',
    '   xx'

]
class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()

        # get alien file path base on colorr
        file_path = './graphics/' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))

    def update(self,direction):
        self.rect.x+=direction

class Extra(pygame.sprite.Sprite):
    def __init__(self,side,screen_width,speed=3):
        super().__init__()
        self.image = pygame.image.load('./graphics/extra.png').convert_alpha()
        if side =='right':
            x = screen_width+50
            self.speed=-speed
        else:
            x = -50
            self.speed=speed
        self.rect = self.image.get_rect(topleft = (x,70))
    def update(self):
        self.rect.x +=self.speed