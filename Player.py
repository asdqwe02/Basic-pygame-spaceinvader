import pygame
# from debug import debug
from Laser import Laser
class Player(pygame.sprite.Sprite): # Inherit from Sprite class
    '''
    Class to represent the player playing the game, return an instance of the player\n
    Attributes:
        image:              use to draw the player sprite on screen    
        rect:               object for storing rectangular coordinates
        speed:              speed the player travel at
        max_x_constraint:   the constaint to contain the player inside the screen
        ready:              bool value to determine laser readiness and if player can shoot laser
        laser_time:         time get from the last time the player shoot the laser
        laser_cd:           laser cooldown (basically laser fire for the player)
        lasers:             the object to contain the information of lasers shot out by the player 
        playerHP:           player health point
        laser_sound:        the sound the laser make whenn player shoot a laser
    '''
    def __init__(self,pos,constraint,speed,hp=3):
        '''
        input:
            pos:            initial spawn location of the player
            constraint:     width constraint to contain the player inside the screen
            speed:          player initial speed
            hp:             player initial health point default is 3
        output: construct the Player instance 
        '''
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
        '''
        input:
            
        output: get player key press then process it to perform player movement and attack 
        '''
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
        '''
        input:
            damage: the damage the player going to take
        output: decrease the player health point base on the damage 
        '''
        self.playerHP-=damage

    def update(self):
        '''
        input:

        output: update the player sprite, player's laser sprite and state in the game
        '''
        self.get_input()
        self.checkBoundary()
        self.lasers.update()

    def checkBoundary(self):
        '''
        input:

        output: check the boundary to contain the player inside the screen
        '''
        # debug('Player position x:{}'.format(self.rect.x))
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
        if self.rect.left < 0:
            self.rect.left = 0 

    def shoot_laser(self):
        '''
        input:

        output: shoot out the player's laser
        '''
        # can use self.rect.bottom because player conveniently is at the bottom of screen
        self.lasers.add(Laser(self.rect.center,8,1,self.rect.bottom))
        self.laser_sound.play()
    
    def recharge(self):
        '''
        input:

        output: recharge the player laser time
        '''
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cd:
                self.ready=True   