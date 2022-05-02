import pygame
from debug import debug
from Laser import Laser
class Player(pygame.sprite.Sprite): # Inherit from Sprite class
    def __init__(self,pos,constraint,speed,hp=3):
        super().__init__()

        # Convert Alpha for transparent sprites/images
        self.image = pygame.image.load('./graphics/player.png').convert_alpha() 
    
        # Position is a tuple midBottom = pos
        self.rect = self.image.get_rect(midbottom = pos)

        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0 
        self.laser_cd = 600 # milisecond
        self.lasers=pygame.sprite.Group() # player laser
        self.playerHP = hp

        # Audio
        self.laser_sound = pygame.mixer.Sound('./audio/laser.wav')
        self.laser_sound.set_volume(0.2)


    #process input   
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed


        self.recharge()
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def getHit(self,damage=1):
        self.playerHP-=damage

    def update(self):
        self.get_input()
        self.checkBoundary()
        self.lasers.update()

    def checkBoundary(self):
        # debug('Player position x:{}'.format(self.rect.x))
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
        if self.rect.left < 0:
            self.rect.left = 0 

    def shoot_laser(self):
        # can use self.rect.bottom because player conveniently is at the bottom of screen
        self.lasers.add(Laser(self.rect.center,8,1,self.rect.bottom))
        self.laser_sound.play()
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cd:
                self.ready=True   