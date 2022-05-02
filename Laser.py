
from email.mime import audio
import pygame



class Laser(pygame.sprite.Sprite):
    def __init__(self,pos,speed,direction,screen_height,type=0):
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
        # destroy self after a certain amount of time 
        # self.init_time = pygame.time.get_ticks() 
        # self. desroy_time = 2500 # 2.5s can add parameter to change this later


    def animate(self):
        if pygame.time.get_ticks() - self.next_frame_time >= self.time_per_frame:
            self.current_sprite += 1
            if self.current_sprite >= len(self.alien_laser_sprites):
                self.current_sprite=0
            self.image = self.alien_laser_sprites[self.current_sprite]
            self.next_frame_time += self.time_per_frame

    def update(self):
        if self.type != 0:
            self.animate()

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

class ChargeLaser(pygame.sprite.Sprite):
    def __init__(self,pos,speed,direction,screen_height):
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
        self.speed = speed
        self.direction = direction
        self.height_y_constraint = screen_height

        # audio for charge laser
        # self.laser_beam_sound = pygame.mixer.Sound('./audio/fast laser beam.wav')
        # self.laser_beam_sound.set_volume(0.5)
        # self.laser_charge_sound = pygame.mixer.Sound('./audio/laser charge.wav')
        # self.laser_charge_sound.set_volume(0.5)

        self.charge_laser_sound = pygame.mixer.Sound('./audio/charge laser and shoot.wav')
        self.charge_laser_sound.set_volume(1)
        self.charge_laser_sound.play()

    def animate(self):
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
                

        if self.fired:
            if pygame.time.get_ticks() - self.fire_timer >=self.fire_time:
                self.kill()
    def update(self,pos):
        self.move_laser(pos)
        self.animate()
    def move_laser(self,pos):
        self.pos = pos
        self.rect.midtop = self.pos