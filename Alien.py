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
    'xxx',
    'xxxx',
    'xxxxxx',
    'xxxxxx',
    'xxxxxx',
    'xxxx',
    'xxx',
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
    def __init__(self,color,x,y,speed=1):
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
        self.speed = speed

    def update(self,direction):
        self.rect.x += (direction*self.speed)
        self.animate()
        if self.hit_time != 0:
            self.kill_after()

        
    def animate(self):
        if pygame.time.get_ticks() - self.next_frame_time >= self.time_per_frame and self.hit_time==0:
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite=0
            self.image = self.sprites[self.current_sprite]
            self.next_frame_time += self.time_per_frame
    def die(self):
        self.image = self.die_sprite
        self.hit_time = pygame.time.get_ticks()
    def kill_after(self,time=200):
        if pygame.time.get_ticks()-self.hit_time>=time:
            self.kill()

class BossAlien(pygame.sprite.Sprite):
    def __init__(self,x,y,speed=1,screen_width=600,screen_height=600,hp=20) -> None:
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

        if pygame.time.get_ticks() - self.next_frame_time >= self.time_per_frame and self.die_time==0:
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite=0
            self.image = self.sprites[self.current_sprite]
            self.next_frame_time += self.time_per_frame

    def update(self):

        # for event in pygame.event.get():

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
        if self.rect.right >= self.x_constraint:
            self.direction = -1
            self.move_down()
        if self.rect.left <= 0:
            self.direction = 1
            self.move_down()

    def getHit(self):
        self.hp-=1

    def die(self):
        self.image = self.die_sprite
        self.die_time = pygame.time.get_ticks()

    def kill_after(self,time=200):
        if pygame.time.get_ticks()-self.die_time>=time:
            self.kill()
    def checkHP(self):
        if self.hp/self.baseHP <= 0.5:
            self.speed = 4
        if self.hp <= 0 and self.die_time==0:
            self.die()
        elif self.die_time!=0: self.kill_after()

    def move_down(self):
        self.rect.y+=4
    def move_sideway(self):
        self.rect.x += (self.direction*self.speed)
    def entering(self):
        self.rect.y+=2
        if self.rect.bottom>=self.y_constraint/4:
            self.entrance=False

    def shoot_lasers(self):
        offset = self.rect.width/2
        offset_x = randint(-offset,offset)
        laser_pos = [self.rect.midbottom[0] + offset_x,self.rect.midbottom[1]]
        
        self.lasers.add(Laser(laser_pos,8,-1,self.y_constraint,type=1))
        self.laser_ready = False
        self.laser_time = pygame.time.get_ticks()
        self.laser_sound.play()

    def shoot_laser_beam(self):
        offset_y = 20
        laser_pos = [self.rect.midbottom[0],self.rect.midbottom[1]+offset_y]
        self.laser_beam.add(ChargeLaser(laser_pos,speed=3, direction=-1,screen_height=self.y_constraint))
        self.laser_beam_ready=False
        self.laser_beam_time = pygame.time.get_ticks()
        pygame.time.set_timer(CHARGELASER,2000,1)


    def recharge_laser(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cd:
                self.laser_ready=True   
    def recharge_laser_beam(self):
        if not self.laser_beam_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_beam_time >=self.laser_beam_cd:
                self.laser_beam_ready=True


    def set_wait_timer(self,time):
        self.wait_timer=time
    def check_wait(self):
        if self.wait==True:
            if  pygame.time.get_ticks() - self.wait_timer >= self.wait_time:
                self.wait=False

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
