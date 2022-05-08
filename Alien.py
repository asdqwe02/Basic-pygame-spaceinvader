from random import randint

import pygame
from Laser import ChargeLaser,Laser


CHARGELASER = pygame.USEREVENT + 2 # EVENT ID 26


testformation = [
    'x'
]
formation1 = [
    'xxxxxxxx',
    'xxxxxxxx',
    'xxxxxxxx',
    'xxxxxxxx',
    'xxxxxxxx',
    'xxxxxxxx'
]

formation2 = [
    'xxxx',
    'xxxxx',
    'xxxxxxx',
    'xxxxxxx',
    'xxxxxxx',
    'xxxxx',
    'xxxx',
]

formation3 = [
    'xxxxx',        #  xxxxx
    'x x x',        #  x x x
    'x x x',        #  x x x
    'xxxxxxx',      # xxxxxxx
    'x x x',        #  x x x
    'x  x',         #   x x
    'x'             #    x
]

formation4 = [
    'x',
    'xxx',
    'xxxx',
    'xxxxxx',
    'xxxxxxxx',
    'xxx x xxx'
]

formation5 = [
    'xxx x xxx',
    'xxxxxxxx',
    'xxxxxx',
    'xxxx',
    'xxx',
    'x',
]

formation6 = [
    'xx   xx',
    'xx   xx',
    'xxxxxxx',
    'xxxxxx',
    'xxxxxxx',
    'xx  xx',
    'xx  xx',
]

formation7 = [
    'xx x xx',
    'xx x xx',
    'xxxxxxx',
    'xx x xx',
    'xxx xxx',
    'xx x xx',
    'xxxxxxx',
]

formation8 = [
    'xx',
    'xxx',
    'xxxx',
    'xxxxxxxx',
    'xxxxxxxx',
    'xxxxx',
    'xxx xxx',
    'xx   xx',
]

formation_array = [formation1,formation2,formation3,formation4,
                    formation5,formation6,formation7,formation8]

class Alien(pygame.sprite.Sprite):
    '''
    This class represent the small alien in the game control their movement and animation\n
    Attributes:
        sprites:            hold the frame of animation of the alien to load on the screen
        current_sprite:     current sprite to draw on the screen
        die_sprite:         die sprite display when the alien die
        image:              use to draw the sprite on screen
        next_frame_time:    time when the last frame was on screen
        rect:               object for storing rectangular coordinates
        speed:              speed the alien travel at
        hit_time:           the time when the alien was hit, use to delay the destruction of the alien
                            instance so that its die sprite is draw on screen nfor a certain amount of time
        time_per_frame:     time between each frame

    '''
    def __init__(self,color,x,y,speed=1):
        '''
        input:  
            color:      color of the alien use to determine which sprite file to load
            x:          initial position x of the alien
            y:          initial position y of the alien
            speed:      initial speed of the alien
        output: construct the Alien
        '''
        super().__init__()
        # get alien file path base on colorr
        file_path = './graphics/' + color # + '.png'
        self.sprites = []
        self.sprites.append(pygame.image.load(file_path + '.png').convert_alpha())
        self.sprites.append(pygame.image.load(file_path + '2.png').convert_alpha())
        self.current_sprite = 0
        self.die_sprite = pygame.image.load(file_path + '_explode.png').convert_alpha()
        self.image = self.sprites[self.current_sprite]
        self.next_frame_time = pygame.time.get_ticks()

        # self.image = pygame.image.load(file_path+'.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.speed = speed

        self.hit_time = 0
        self.time_per_frame = 1000 * 1/len(self.sprites) # should be 500 milisecond

    def setspeed(self,speed):
        '''
        input:
            speed:      the speed to set for the alien
        output: set the speed of the alien
        '''
        self.speed = speed

    def update(self,direction):
        '''
        input:
            direction:  direction to move the alien down
        output: update the alien animation frame and move the alien sideway depend on the direction, 
                check if the alien is hit to kill it after a certain amount of time

        '''
        self.rect.x += (direction*self.speed)
        self.animate()
        if self.hit_time != 0:
            self.kill_after()

    def animate(self):
        '''
        input:

        output: change the frame of animation for the alien and update current frame index
        '''
        if pygame.time.get_ticks() - self.next_frame_time >= self.time_per_frame and self.hit_time==0:
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite=0
            self.image = self.sprites[self.current_sprite]
            self.next_frame_time += self.time_per_frame
    def die(self):
        '''
        input:

        output: set sprite to die sprite and get the hit_time of the alien
        '''
        self.image = self.die_sprite
        self.hit_time = pygame.time.get_ticks()
    def kill_after(self,time=200):
        '''
        input:
            time:   the time to kill the instance after the time is up
        output: kill the instance of the class after a certain amount of time
        '''
        if pygame.time.get_ticks()-self.hit_time>=time:
            self.kill()

class BossAlien(pygame.sprite.Sprite):
    '''
    This class represent the Boss Alien, control its movement, behavior and attacks\n
    Attributes:
        sprites:                hold the frame of animation of the boss alien to load on the screen
        die_sprite:             die sprite display when the boss alien die
        time_per_frame:         time between each frame
        current_sprite:         current sprite to draw on the screen
        next_frame_time:        time when the last frame was on screen
        image:                  use to draw sprite on screen
        rect:                   object for storing rectangular coordinates
        speed:                  speed the boss alien travel at
        hp:                     boss alien health point
        baseHP:                 boss alien base health point to switch phase
        die_time:               the time when the alien boss start to die 
        x_constraint:           x constraint to check the boss alien poisition on screen 
                                    and move its position down when the boss alien reach the boundary
        y_constraint:           y constraintn to pass into the boss alien's lasers
        direction:              direction sideway the boss alien going
        lasers:                 lasers shoot out from the boss alien
        laser_beam:             laser beam fire by the boss alien
        laser_ready:            bool to check the readiness of the lasers
        laser_beam_ready:       bool to check the readiness of the laser beam
        laser_cd:               lasers cool down use to recharge the lasers
        laser_beam_cd:          laser beam cool down use to recharge the laser beam
        wait_time:              wait time when the boss alien fire out the laser beam
        wait_timer:             wait timer to determine the amount of time the boss has waitd 
                                    for the laser beam to shoot
        laser_time:             laser timer to set laser_ready
        laser_beam_time:        laser beam timer to set laser_beam_ready
        entrance:               check if the boss is entering the scene
        wait:                   bool to check if the boss alien need to stop its sideway movement
        laser_sound:            sound to play when the boss shoot out the small lasers
    '''
    def __init__(self,x,y,speed=1,screen_width=600,screen_height=600,hp=20) -> None:
        '''
        input:
            x:              boss alien's spawn position x
            y:              boss alien's spawn position y
            speed:          boss alien's initial speed
            screen_width:   screen width to set x constraint
            screen_height:  screen height to set y constraint
            hp:             boss alien's initial hp
        output: construct BossAlien
        '''
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('./graphics/boss_alien1.png').convert_alpha())
        self.sprites.append(pygame.image.load('./graphics/boss_alien2.png').convert_alpha())
        self.die_sprite = pygame.image.load('./graphics/boss_alien_explode.png').convert_alpha()

        self.time_per_frame = 1000 * 1/len(self.sprites) # should be 500 milisecond

        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]
        self.next_frame_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect(midtop=(x,y))

        self.speed = speed
        self.hp = hp
        self.baseHP = self.hp
        self.die_time = 0

        self.x_constraint = screen_width
        self.y_constraint = screen_height
        self.direction = 1

        # laser setup for boss alien
        self.lasers=pygame.sprite.Group() 
        self.laser_beam = pygame.sprite.GroupSingle()
        self.laser_ready = True
        self.laser_beam_ready = True
        self.laser_cd = 250
        self.laser_beam_cd = 5000 # actually cd: 5000 - 2500 = 2500 milisec or 2.5 sec
        self.wait_time = 500 # = charge laser fire time


        self.wait_timer = 0
    
        self.laser_time = pygame.time.get_ticks()
        self.laser_beam_time = pygame.time.get_ticks()


        self.entrance = True
        self.wait = False
        

        # audio
        self.laser_sound = pygame.mixer.Sound('./audio/Laser_shoot 84.wav')
        self.laser_sound.set_volume(0.25)

    def animate(self):
        '''
        input:

        output: change the frame of animation and update the current frame index
        '''
        if pygame.time.get_ticks() - self.next_frame_time >= self.time_per_frame and self.die_time==0:
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite=0
            self.image = self.sprites[self.current_sprite]
            self.next_frame_time += self.time_per_frame

    def update(self):
        '''
        input:

        output: update the BossAlien behavior, movement, attacks, 
        check if the boss die eand destroy it after a certain amout of time
        '''

        self.check_wait()

        if self.entrance:
            self.entering()

        if not self.entrance and not self.wait:  
            self.move_sideway()
        self.check_pos()
        self.animate()

        # if self.laser_beam.sprite:
        #     self.laser_beam.sprite.move_laser(self.rect.midbottom)
        self.recharge_laser()
        self.recharge_laser_beam()

        if self.laser_ready:
            self.shoot_lasers()
        if self.laser_beam_ready and not self.entrance:
            self.shoot_laser_beam()

        self.laser_beam.update(self.rect.midbottom)
        self.lasers.update()

        self.checkHP()
        
    def check_pos(self):
        '''
        input:

        output: check the boss alien position if the boss reach the boundary change the direction 
        and move the boss down a certain distance
        '''
        if self.rect.right >= self.x_constraint:
            self.direction = -1
            self.move_down()
        if self.rect.left <= 0:
            self.direction = 1
            self.move_down()

    def getHit(self):
        '''
        input:

        output: decrease the boss hp by a certain amount when called
        '''
        self.hp-=1

    def die(self):
        '''
        input:

        output: change the current sprite to die sprite and get die time
        '''
        self.image = self.die_sprite
        self.die_time = pygame.time.get_ticks()

    def kill_after(self,time=200):
        '''
        input:
        
        output: kill the BossAlien instance after a certain amount of time
        '''
        if pygame.time.get_ticks()-self.die_time>=time:
            self.kill()
    
    def checkHP(self):
        '''
        input:

        output: check the boss hp to change and to know if the boss hp <= 0 to trigger die method
        '''
        if self.hp/self.baseHP <= 0.5:
            self.speed = 4
        if self.hp <= 0 and self.die_time==0:
            self.die()
        elif self.die_time!=0: self.kill_after()

    def move_down(self):
        '''
        input:

        output: move the boss alien down a certain amount of distance
        '''
        self.rect.y+=4
    
    def move_sideway(self):
        '''
        input:

        output: move the boss alien sideway a certain amount of distance depend on the speed
        '''
        self.rect.x += (self.direction*self.speed)
    
    def entering(self):
        '''
        input:

        output: move the boss down a certain amount of distance from the spawn point, 
        make the move_sideway method wait until the entering process is done
        '''
        self.rect.y+=2
        if self.rect.bottom>=self.y_constraint/4:
            self.entrance=False

    def shoot_lasers(self):
        '''
        input: 

        output: boss alien shoot out lasers
        '''
        offset = self.rect.width/2
        offset_x = randint(-offset,offset)
        laser_pos = [self.rect.midbottom[0] + offset_x,self.rect.midbottom[1]]
        
        self.lasers.add(Laser(laser_pos,8,-1,self.y_constraint,type=1))
        self.laser_ready = False
        self.laser_time = pygame.time.get_ticks()
        self.laser_sound.play()

    def shoot_laser_beam(self):
        '''
        input:
        
        output: boss alien shoot out laser beam
        '''
        offset_y = 20
        laser_pos = [self.rect.midbottom[0],self.rect.midbottom[1]+offset_y]
        self.laser_beam.add(ChargeLaser(laser_pos))
        self.laser_beam_ready=False
        self.laser_beam_time = pygame.time.get_ticks()
        pygame.time.set_timer(CHARGELASER,2000,1)

    def recharge_laser(self):
        '''
        input:

        output: recharge the laser time depend on laser cooldown
        '''
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cd:
                self.laser_ready=True   
    
    def recharge_laser_beam(self):
        '''
        input:

        output: recharge the laser beam time depend on laser beam cooldown
        '''
        if not self.laser_beam_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_beam_time >=self.laser_beam_cd:
                self.laser_beam_ready=True

    def set_wait_timer(self,time):
        '''
        input: 
            time: the amount of time to wait 
        output: set the wait_timer 
        '''
        self.wait_timer=time
    
    def check_wait(self):
        '''
        input:

        output: check if the wait time ended and flip the wait bool value to false
        '''
        if self.wait==True:
            if  pygame.time.get_ticks() - self.wait_timer >= self.wait_time:
                self.wait=False

class Extra(pygame.sprite.Sprite):
    '''
    Extra alien for the player to kill and get bonus point\n
    Attributes:
        image:      use to draw sprite on screen
        speed:      speed the extra alien travel at
        rect:       object for storing rectangular coordinates
    '''
    def __init__(self,side,screen_width,speed=3):
        '''
        input:
            side:               side the extra alien going from
            screen_width:       screen width to set spawn point of extra aliien
            speed:              speed the extra alien travel at
        '''
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
        '''
        input:

        output: update the position of the extra alien on the screen base on its speed
        '''
        self.rect.x +=self.speed
