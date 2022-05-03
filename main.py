from genericpath import exists
import json
from random import randint, random
from secrets import choice
import pygame,sys,time
from Laser import Laser
# from debug import debug
from Player import Player
import Obstacle
import Alien

class Game:
    '''
    The game instance to play the game \n
    Attributes:
        restart:                bool to let the game restart when press "R" key
        pause:                  bool to pause the game
        player:                 player object to contain the player sprite annd its information
        score:                  hold the score value
        font:                   font use in the game
        live_surf:              the sprite that show player lives on top right of the screen
        live_x_start_pos:       start position x for the live_surf  
        shape:                  shape of the obstacles to draw
        block_size:             the size of individual block that made up the obstacles
        blocks:                 object to contain all the individual blocks of the obstacles
        obstacle_amount:        amount of obstacles in the game
        ostable_x_positions:    start position x for the obstacles
        aliens:                 the object to contain a group of aliens and its information
        alien_formation:        formation of the small aliens to set up in the game
        alien_direction:        initial sideway direction for the aliens to go
        alien_down_distance:    the distance for the group of aliens to move down when they reach boundary
        alien_lasers:           object to contain lasers the group of aliens shoot out 
        base_aliens_amount:     the initial amount of aliens in the group to calculate the ratio of aliens
        alien_ratio:            ratio of alien = current amount of alien / base_aliens_amount - to change aliens speed and down distance
        extra:                  object to contain the extra alien and its information
        extra_spawn_time:       extra alien spawn time (random value from 400 to 800)
        boss_alien:             object to contain the boss alien sprite and its information
        boss_spawned:           bool to determine if the boss has spawned or not 
        music:                  music array to hold all the music tracks use in the game
        current_music_track:    current music track index to play
        laser_sound:            sound of the laser shoot out by player and small aliene
        explosion_sound:        sound when the player's laser hit the small aliens or boss alien
    '''
    def __init__(self):
        '''
        input:

        output: construct the game instance
        '''
        self.restart = False
        self.pause = False

        self.hi_score  = 0
        if exists('./save/save_file.txt'):
            with open('./save/save_file.txt') as save_file:
                data = json.load(save_file)
            self.hi_score = data['High Score'] 
        
        # Player setup
        player_sprite = Player((screen_width/2,screen_height),screen_width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Score and Font setup
        self.score = 0
        self.font=pygame.font.Font('./font/Pixeled.ttf',15)

        
        # Player lives display setup
        self.live_surf = pygame.image.load('./graphics/heart.png').convert_alpha()
        self.live_surf = pygame.transform.scale(self.live_surf,(40,35))
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0]*self.player.sprite.playerHP + 30)
        

        # Obstacles setup
        self.shape = Obstacle.shape
        self.block_size = 6 # size of individual block
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.ostable_x_positions = [num * (screen_width/self.obstacle_amount) for num in range(self.obstacle_amount)]
        # * is unpacking operator
        self.create_mutiple_obstacles(*self.ostable_x_positions,x_start=screen_width/15,y_start=480)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        # self.alien_formation = Alien.testformation # spawn boss right away
        self.alien_formation = choice(Alien.formation_array)

        self.alien_direction = 1
        self.alien_down_distance = 1
        self.alien_lasers = pygame.sprite.Group() # alien lasers
        self.base_aliens_amount = self.alien_setup(self.alien_formation)
        self.alien_ratio = len(self.aliens.sprites())/self.base_aliens_amount
        # print(self.base_aliens_amount) #debug


        # Extra alien setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400,800) 

        # Boss alien setup
        self.boss_alien = pygame.sprite.GroupSingle()
        self.boss_spawned = False

        # Audio setup
        self.music = []
        self.music.append(pygame.mixer.Sound('./audio/music.wav'))                                 # music track 0
        self.music.append(pygame.mixer.Sound('./audio/8-Bit Boss Battle- 4 - By EliteFerrex.wav')) # music track 1
        self.music[0].set_volume(0.25)
        self.music[0].play(loops=-1)

        self.current_music_track = 0

        self.laser_sound = pygame.mixer.Sound('./audio/laser.wav')
        self.laser_sound.set_volume(0.2)
        self.explosion_sound = pygame.mixer.Sound('./audio/explosion.wav')
        self.explosion_sound.set_volume(0.3)

    def create_obstacle(self,x_start, y_start,offset_x):
        '''
        intput:
            x_start:    start position x of the block
            y_start:    start position y of the block
            offset_x:   off set between each obstacle
        ouput: create individual block in an obstacle base on the shape
        '''
        for row_index, row in enumerate(self.shape):
            for column_index, col in enumerate(row):
                if col == 'x':
                    x = x_start  + column_index * self.block_size + offset_x
                    y = y_start + row_index  * self.block_size
                    block = Obstacle.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)

    def create_mutiple_obstacles(self,*offset,x_start,y_start):
        '''
        intput:
            x_start:    start position x of the onstacle
            y_start:    start position y of the onstacle
            offset_x:   off set between each obstacle
        output: create multiple obstacles
        '''
        for offset_x in offset:
            self.create_obstacle(x_start,y_start,offset_x)
    
    def alien_setup(self,formation,x_distance=60,y_distance=48,offset_x=10,offset_y=85):
        '''
        input:
            formation:      alien formation randomly chosen when initialize
            x_distance:     distance between each alien
            y_distance:     distance between each row of the alien
            offset_x:       use to set the offset x distance but no longer in use atm 
            offset_y:       start distance of the alien formation from the top of the screen
        output: return the length the aliens group, set up the alien base on the formation of the alien
        '''
        color = {
            1:'red',
            2:'yellow',
            3:'green',
        }

        # ( 40 is the width of the alien | space between alien is 20 ) -> 60
        # alien amount = count 'x' in the formation
        # x_start = (screen_width - (alien_amount*60)) / 2
        space_on_row = []
        for row_formation in self.alien_formation: # coun the amount of alien on each rows
            # temp = row_formation.count('x')
            temp = len(row_formation)
            space_on_row.append(temp)
        x_start = [
            (screen_width-(num*60))/2 for num in space_on_row 
        ]
        for row_index,row in enumerate(formation):
            # random alien color on each row
            c = color[randint(1,3)]
            for columnn_index, col in enumerate(row):
                if col =='x':
                    # x = columnn_index*x_distance + offset_x
                    x = columnn_index * x_distance + x_start[row_index]
                    y = row_index*y_distance + offset_y
                    # random alien color
                    # c = color[randint(1,3)] 
                    alien_sprite = Alien.Alien(c,x,y)
                    self.aliens.add(alien_sprite)
        return len(self.aliens)
    
    # should put these in the alien module
    def alien_side_pos_checker(self):
        '''
        input:

        output: check if any of the aliens in the alien group hit the side of the screen boundary 
                then move the group of aliens down by a certain amount of distance
        '''
        for alien in self.aliens.sprites():
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(self.alien_down_distance)
            if alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(self.alien_down_distance)
    def alien_move_down(self,distance):
        '''
        input:
            distance:   the amount of distance to moove the alien group down
        output: move the alien group down by distance
        '''
        if self.aliens: # avoid null ref
            for alien in self.aliens.sprites():
                alien.rect.y += distance
    def alien_shoot(self):
        '''
        input:

        output: one of the alien in the alien group shoot out a laser and the laser sound is played
        '''
        if self.aliens.sprites(): # to avoid null ref
            #choose random in collections
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,speed=8,direction=0,screen_height=screen_height,type=1)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()
    def alien_check_remain(self): # increase speed when certain amount of alien die sidenote: this look bad for performance
        '''
        input:
        
        output: check the amount of remain alien to increase the alien group speed and down distance
        '''
        # trying to optimize it a bit
        current_aliens_amount =  len(self.aliens.sprites())
        ratio = current_aliens_amount/self.base_aliens_amount
        if current_aliens_amount>=1 and ratio!=self.alien_ratio: 
            self.alien_ratio=ratio
            for alien in self.aliens.sprites():
                if 0.5 < current_aliens_amount/self.base_aliens_amount <= 0.75:
                    alien.setspeed(2)
                if 0.25 < current_aliens_amount/self.base_aliens_amount <= 0.50:
                    alien.setspeed(3)
                if current_aliens_amount/self.base_aliens_amount <= 0.25:
                    alien.setspeed(4)
                    self.alien_down_distance = 3
                if current_aliens_amount == 1:
                    self.alien_down_distance = 5
                    alien.setspeed(8)   
        # spawn boss alien when there are no more aliens in list                    
        if current_aliens_amount == 0 and len(self.boss_alien.sprites())==0 and not self.boss_spawned:
            self.boss_alien.add(Alien.BossAlien(screen_width/2,-240,speed=2))
            self.boss_spawned=True    
            self.music[self.current_music_track].fadeout(2000) # fade out old music track over 2 seconds
            self.next_music_track = 1
            pygame.time.set_timer(PLAYENEXTMUSICTRACK,2000,1) # set timer to play the next music track in 2 seconds
                
    # Extra alien methods
    def extra_alien_timer(self):
        '''
        input:

        output: check the extra alien timer and spawn the extra alien when the tim is <=0
        '''
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            # default speed for extra is 3
            # print(self.extra_spawn_time) # debug
            self.extra.add(Alien.Extra(choice(['right','left']),screen_width=screen_width))
            self.extra_spawn_time = randint(400,800)

    # Collision
    def collision_checks(self):
        '''
        input:

        output: process the collision in the game and act accordingly
        '''
        # player's lasers
        if self.player.sprite and self.player.sprite.lasers :
            for laser in self.player.sprite.lasers:
                # obstacles collions
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                    pass
                # aliens collisions
                collided_alien = pygame.sprite.spritecollide(laser,self.aliens,False) # get collided object
                if collided_alien:
                    for alien in collided_alien:
                        self.score+=10
                        alien.die()
                    laser.kill()
                    self.explosion_sound.play()
                # boss alien collisions
                if pygame.sprite.spritecollide(laser,self.boss_alien,False):
                    laser.kill()
                    self.boss_alien.sprite.getHit()
                    self.score +=50
                    self.explosion_sound.play()
                # extra collisions
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    self.score+=100
                    laser.kill()
                    self.explosion_sound.play()

        # alien's laser
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacles collisions
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                # player collisions
                if pygame.sprite.spritecollide(laser,self.player,False):
                    # print('alien\'s laser hit player')
                    laser.kill()
                    self.player.sprite.getHit()

        # boss alien
        if self.boss_alien.sprite:
            # boss alien's lasers
            if self.boss_alien.sprite.lasers:
                for laser in self.boss_alien.sprite.lasers:
                    # collide with obstacles
                    if pygame.sprite.spritecollide(laser,self.blocks,True):
                        laser.kill()
                    # collide with player
                    if pygame.sprite.spritecollide(laser,self.player,False):
                        laser.kill()
                        self.player.sprite.getHit()
            if self.boss_alien.sprite.laser_beam: # boss's laser beam
                for laser_beam in self.boss_alien.sprite.laser_beam:
                    pygame.sprite.spritecollide(laser_beam,self.blocks,True)
                    if pygame.sprite.spritecollide(laser_beam,self.player,False):
                        self.player.sprite.getHit(3)

            # boss alien body collide with player or obstacles
            pygame.sprite.spritecollide(self.boss_alien.sprite,self.blocks,True)
            if pygame.sprite.spritecollide(self.boss_alien.sprite,self.blocks,False):
                self.player.sprite.getHit(3)

        # aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)
                if pygame.sprite.spritecollide(alien,self.player,False):
                    # print('alien hit player')
                    self.player.sprite.getHit(3)
                    
    # DISPLAY FUNCTIONS

    # display score function
    def display_score(self):
        '''
        input:

        output: display the current score and high score on the top left of the screen
        '''
        score_surf = self.font.render('score: {}'.format(self.score),False,'white')
        score_rect = score_surf.get_rect(topleft = (20,6))
        hi_score_surf = self.font.render('Hi-score: {}'.format(self.hi_score),False,'white')
        hi_score_rect = hi_score_surf.get_rect(topleft = (score_rect.right+20,6))
        screen.blit(score_surf,score_rect)
        screen.blit(hi_score_surf,hi_score_rect)
    # display player livies function
    def display_player_lives(self):
        '''
        input:

        output: display the player lives on the top right of the screen
        '''
        for live in range(self.player.sprite.playerHP):
            x = self.live_x_start_pos + (live*(self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf,(x,10))
            pass

    # Adio function
    def play_music_track(self,track_number,volume):
        '''
        input:
            track_number:   the music track index to play
            volume:         the volume to play the music
        output: play the music track
        '''
        #loading in music while playing can cause delay in game :| idk how to fix
        self.music[self.current_music_track].stop()
        self.current_music_track = track_number
        self.music[track_number].set_volume(volume)
        self.music[track_number].play(loops=-1)
    
    def run(self):
        '''
        input:

        output: process all the game information, update and draw sprite on screen
        '''
        # Debug
        # if self.player.sprite.playerHP > 0:
        #     debug('Player HP: {}'.format(self.player.sprite.playerHP),y=40)
        # else: debug('Player died',y=40)
        
        # UPDATE
        
        # Colision 
        self.collision_checks()

        # Player update
        self.player.update()

        # Aliens update
        self.alien_side_pos_checker() # check the boundary and move alien down
        self.aliens.update(self.alien_direction) # update for alien
        self.alien_lasers.update() # aliens laser update

        self.alien_check_remain() # check remain to spawn boss and increase speed

        self.extra_alien_timer() # timer for extra alien    
        self.extra.update() # update for extra alien
       
        #DRAWda

        # draw player
        self.player.draw(screen)

        # draw lasers
        self.player.sprite.lasers.draw(screen) # player laser

        # boss alien and its lasers draw and upadte
        if self.boss_alien.sprite:
            self.boss_alien.sprite.lasers.draw(screen) 
            self.boss_alien.sprite.laser_beam.draw(screen)   
            self.boss_alien.draw(screen)
            self.boss_alien.update()

        self.alien_lasers.draw(screen) # aliens laser

        # draw obstacles
        self.blocks.draw(screen)

        # draw alien
        self.aliens.draw(screen)
        self.extra.draw(screen)

        # DISPLAY
        self.display_score()
        self.display_player_lives()


        # note: display victory and game over message in pause 
        self.victory_message()
        self.game_over_message()
   
    def game_end_message(self,message,offset_x=0,offxet_y=0):
        '''
        input:
            message:    message to display on screen at the end of the game
            offset_x:   the offset x to display thte message
            offxet_y:   the offset y to display thte message
        output: display the message at the end of the game, save highscore, set restart bool value to True
                        set timer to pause the game after 200 miliseconds
        '''
        message_surf = self.font.render(message,False,'white')
        message_rect = message_surf.get_rect(center = (screen_width/2 + offset_x,screen_height/2+offxet_y))
        screen.blit(message_surf,message_rect)
        self.restart=True
        self.restart_message()

        if self.hi_score <= self.score:
            save_data = {
                'High Score':self.score
            }
            with open('./save/save_file.txt','w') as save_file:
                json.dump(save_data,save_file)


        if not self.pause:
            self.pause = True
            # print('pause')
            pygame.time.set_timer(PAUSE,200,1)

    def victory_message(self):
        '''
        input:

        output: check if the player win and display "YOU WIN" message on screen
        '''
        if (not self.aliens.sprites() and 
            not self.boss_alien.sprite and 
            not self.player.sprite.playerHP <=0):
            self.game_end_message('YOU WIN')
    def game_over_message(self):
        '''
        input:

        output: check if the player win and display "YOU LOSE" message on screen
        '''
        if self.player.sprite and self.player.sprite.playerHP <=0:
           self.game_end_message('YOU LOSE :(')
    def restart_message(self):
        '''
        input:

        output: display the restart message on screen when the restart bool value is True
        '''
        if self.restart:
            restart_surf = self.font.render('PRESS "R" KEY TO RESTART',False,'white')
            restart_rect = restart_surf.get_rect(center = (screen_width/2,screen_height/2+50))
            screen.blit(restart_surf,restart_rect)
            
    def restart_game(self):
        '''
        input:

        output: reset all the game value to default
        '''
        self.restart = False
        self.pause = False

        self.hi_score  = 0
        if exists('./save/save_file.txt'):
            with open('./save/save_file.txt') as save_file:
                data = json.load(save_file)
            self.hi_score = data['High Score'] 

        # stop all previously playing music
        # for music in self.music:
        #     music.stop()
        pygame.mixer.stop()

        # Player setup
        player_sprite = Player((screen_width/2,screen_height),screen_width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        # Score and Font setup
        self.score = 0
        # Player lives display setup
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0]*self.player.sprite.playerHP + 30)
        # Obstacles setup
        self.shape = Obstacle.shape
        self.block_size = 6 # size of individual block
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.ostable_x_positions = [num * (screen_width/self.obstacle_amount) for num in range(self.obstacle_amount)]
        # * is unpacking operator
        self.create_mutiple_obstacles(*self.ostable_x_positions,x_start=screen_width/15,y_start=480)
        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_formation = choice(Alien.formation_array)
        self.alien_direction = 1
        self.alien_down_distance = 1
        self.alien_lasers = pygame.sprite.Group() # alien lasers
        self.base_aliens_amount = self.alien_setup(self.alien_formation)
        self.alien_ratio = len(self.aliens.sprites())/self.base_aliens_amount
        # Extra alien setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400,800) 
        # Boss alien setup
        self.boss_alien = pygame.sprite.GroupSingle()
        self.boss_spawned = False
        self.music[0].play(loops=-1) # play main theme again
        self.current_music_track = 0
    def paused(self):
        '''
        input:

        output: pause the game until the player press "ESC" key unless the game ended
        '''
        self.pause=True
        crt.draw(True)
        while self.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_r] and game.restart:
                        self.pause=False
                        game.restart_game()
                    if keys[pygame.K_ESCAPE] and not self.restart:
                        self.pause = not self.pause

            if not self.restart:
                pause_surf = self.font.render('PAUSE ... ',False,'white')
                pause_rect = pause_surf.get_rect(center = (screen_width/2,screen_height/2))
                screen.blit(pause_surf,pause_rect)
            pygame.display.flip()
            clock.tick(30)
           
# CRT filter note: only to look a bit cool doesn't do much
class CRT:
    '''
    Class to make a CRT filter on screen to make the game look a bit cooler\n
    Attributes:
        tv:     the sprite asset to draw on the crt filter on screen
    '''
    def __init__(self) -> None:
        '''
        input:

        output: construct the instance of CRT 
        '''
        self.tv = pygame.image.load('./graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv,(screen_width,screen_height))
    def create_crt_lines(self):
        '''
        input:

        output: draw the crt lines on screen with opacity base on the tv variable opacity
        '''
        line_height = 3 
        line_amount = int(screen_height/line_height)
        for line in range(line_amount):
            y_pos = line *line_height
            # draw on tv so it have the same opacity
            pygame.draw.line(self.tv,'black',(0,y_pos),(screen_width,y_pos),1) 
    def draw(self,pause=False):
        '''
        input:
            pause:  bool value to know if the game is pause
        output: draw the crt filter on screen with the opacity range from 65 to 90 when the game not paused 
                and 200 when the game is paused
        '''
        if not pause:
            self.tv.set_alpha(randint(65,90))
        else: 
            self.tv.set_alpha(200)
        self.create_crt_lines()
        screen.blit(self.tv,(0,0))
if __name__  == '__main__':
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.font.init()
    screen_width = 600
    screen_height = 600
    game_icon = pygame.image.load('./graphics/icon.png')
    pygame.display.set_icon(game_icon)
    pygame.display.set_caption('basic pygame Space invader')
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()

    game = Game() # create an instance of the game
    crt = CRT()
    # The UserEvent will be sent out as an event signal
    # , repeated periodically after the specified time interval
    ALIENLASER = pygame.USEREVENT + 1           # EVENT ID 25
    CHARGELASER = pygame.USEREVENT + 2          # EVENT ID 26
    PLAYENEXTMUSICTRACK = pygame.USEREVENT + 3  # EVENT ID 27
    PAUSE = pygame.USEREVENT + 4                # EVENT ID 28
    pygame.time.set_timer(ALIENLASER,800)
    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot() # alien shooting laser
            if event.type == CHARGELASER and game.boss_alien.sprite:
                game.boss_alien.sprite.wait=True
                game.boss_alien.sprite.set_wait_timer(pygame.time.get_ticks())
            if event.type == PLAYENEXTMUSICTRACK and game:
                game.play_music_track(game.next_music_track,volume= 0.5)
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r] and game.restart:
                    game.restart_game()
                if keys[pygame.K_ESCAPE]:
                    game.paused()
            if event.type == PAUSE:
                game.paused()
            
        screen.fill((30,30,30))

        game.run() #run the game and update game objects
        crt.draw()
        pygame.display.flip()
        clock.tick(60)