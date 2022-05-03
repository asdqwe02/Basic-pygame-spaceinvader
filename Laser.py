
from email.mime import audio
import pygame

'''
Laser modulee
'''

class Laser(pygame.sprite.Sprite):
    '''
    This class is use to represent the small laser that player and aliens shoot out\n
    Attributes:
        type:                   use to differentiate player's laser and alien lasers to play animation
                                    and load sprites
        image:                  use to display sprite on the screen
        alien_laser_sprites:    Hold the sprites for image to load on screen
        current_sprite:         index of current sprite to load on screen
        next_frame_time:        time when the last sprite was drawn on screen
        time_per_frame:         time between each frame of animation
        rect:                   object for storing rectangular coordinates
        speed:                  the speed of the laser
        direction:              direction the laser going to travel
        height_y_constraint:    y constraint to delete laser when it travel out of bound
    '''
    def __init__(self,pos,speed,direction,screen_height,type=0):
        '''
        input: 
            pos:            initial position of the laser
            speed:          speed of the laser
            direction:      direction the laser going to go
            screen_height:  screen height of the game to assign height_y_constraint
            type:           type of laser 0 by default is player 
        output: construct the Laser 
        '''
        super().__init__()
        self.type = type
        if type == 0:
            self.image = pygame.Surface((4,20))
            self.image.fill('white')
        else: 
            self.alien_laser_sprites = []
            self.alien_laser_sprites.append(pygame.image.load('./graphics/alien_laser1.png').convert_alpha())
            self.alien_laser_sprites.append(pygame.image.load('./graphics/alien_laser2.png').convert_alpha())
            self.alien_laser_sprites.append(pygame.image.load('./graphics/alien_laser3.png').convert_alpha())
            self.current_sprite = 0
            self.image = self.alien_laser_sprites[self.current_sprite]
            self.next_frame_time = pygame.time.get_ticks()
            # self.time_per_frame = 1000 * 1/ (len(self.alien_laser_sprites)*3)
            self.time_per_frame = 200


        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.direction = direction
        self.height_y_constraint = screen_height
        # destroy self after a certain amount of time  OBSOLETE
        # self.init_time = pygame.time.get_ticks() 
        # self. desroy_time = 2500 # 2.5s can add parameter to change this later

    def animate(self):
        '''
        input:

        output: switch the frame to display on screen
        '''
        if pygame.time.get_ticks() - self.next_frame_time >= self.time_per_frame:
            self.current_sprite += 1
            if self.current_sprite >= len(self.alien_laser_sprites):
                self.current_sprite=0
            self.image = self.alien_laser_sprites[self.current_sprite]
            self.next_frame_time += self.time_per_frame

    def update(self):
        '''
        input:

        output: method to control sprite behavior, update the laser to move it 
                in the game and animate it, destroy the laser when needed 
        '''
        if self.type != 0:
            self.animate()

        if self.direction==1:
            self.rect.y-=self.speed
        else: self.rect.y+=self.speed
        self.destroy()
    def destroy(self):
        '''
        input:

        output: destroy the laser if the laser reach the boundary
        '''
        if self.rect.y<=-50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()
        # destroy the game object after a certain amount of time it's kinda obsolete
        # global_time = pygame.time.get_ticks()
        # if global_time - self.init_time >= self.desroy_time:
        #     self.kill()

class ChargeLaser(pygame.sprite.Sprite):
    '''
    This class is use to represent big charge laser the boss alien use. The laser is instant and has no speed\n
    Attributes:
        pos:                    poisition x,y to fire the laser can be update over time 
        image:                  use to display sprite on the screen
        sprites                 Hold the sprites for image to load on screen
        current_sprite:         index of current sprite to load on screen
        next_frame_time:        time when the last sprite was drawn on screen
        time_per_frame:         time between each frame of animation
        rect:                   object for storing rectangular coordinates
        fire_time:              time the laser firing for default 500 miliseconds
        charge_time:            charge up time for the laser default 2000 milisecs
        charge_timer:           timer to charge the laser default value is the time the laser is created
        fire_timer:             timer to determine the amount of time the laser has been firing 
                                    value depend on when the laser fired
        fired:                  bool to check if the laser has fired
        charge_laser_sound:     sound for the laser beam when it charge and shoot
    '''
    def __init__(self,pos):
        '''
        input: 
            pos: position to spawn the laser

        output: construct the ChargeLaser
        '''
        super().__init__()
        self.pos = pos
        self.sprites = []
        self.sprites.append(pygame.image.load('./graphics/laser_charge1.png').convert_alpha())
        self.sprites.append(pygame.image.load('./graphics/laser_charge2.png').convert_alpha())
        self.sprites.append(pygame.image.load('./graphics/laser_charge3.png').convert_alpha())
        self.sprites.append(pygame.image.load('./graphics/laser_charge2.png').convert_alpha())
        self.sprites.append(pygame.image.load('./graphics/laser_charge1.png').convert_alpha())

        # self.sprites.append(pygame.image.load('./graphics/laser_beam.png').convert_alpha())
        self.sprites.append(pygame.image.load('./graphics/laser_beam2.png').convert_alpha())


        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.next_frame_time = pygame.time.get_ticks()
       
        # time
        self.time_per_frame = 100  # self.time_per_frame = 1000 * 1/ (len(self.sprites))
        self.fire_time = 500
        self.charge_time = 2000
        
        self.charge_timer = pygame.time.get_ticks()
        self.fire_timer = 0 
        self.fired = False
        self.rect = self.image.get_rect(center = pos)
        
        self.charge_laser_sound = pygame.mixer.Sound('./audio/charge laser and shoot.wav')
        self.charge_laser_sound.set_volume(1)
        self.charge_laser_sound.play()

    def animate(self):
        '''
        input:

        output: Switching frame to animate the ChargeLaser
        '''
        if pygame.time.get_ticks() - self.next_frame_time >= self.time_per_frame and not self.fired:
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites) -1:
                self.current_sprite=0
            self.image = self.sprites[self.current_sprite]
            self.next_frame_time += self.time_per_frame

            if pygame.time.get_ticks() - self.charge_timer >= self.charge_time:
                self.current_sprite = len(self.sprites) -1
                self.image = self.sprites[self.current_sprite]
                self.rect=self.image.get_rect(midtop = self.pos)
                self.fired=True
                self.fire_timer = pygame.time.get_ticks()
       
    def update(self,pos):
        '''
        input:  
            pos: (tuple) position x,y to update the charge laser position on screen
        output: Update the charge laser postiion, animate it and destroy the laser after 
                it has fired a certain amount of time 
        '''
        self.move_laser(pos)
        self.animate()
        if self.fired:
            if pygame.time.get_ticks() - self.fire_timer >=self.fire_time:
                self.kill()
    def move_laser(self,pos):
        '''
        input:
            pos: (tuple) position x,y to update the charge laser position on screen
        output: change the postion of the charge laser
        '''
        self.pos = pos
        self.rect.midtop = self.pos