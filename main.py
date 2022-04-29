from random import randint, random
from re import purge
from secrets import choice
import pygame,sys
from Laser import Laser
from debug import debug
from Player import Player
import Obstacle
import Alien


class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player((screen_width/2,screen_height),screen_width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Score
        self.highscore = 0

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
        self.alien_formation = Alien.formation
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group() # alien lasers

        # Extra alien setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400,800) 

        # self.alien_setup(0,50,100,150,200,formation= self.alien_cols,x_start = 0,y_start =180)
        # self.alien_setup(*self.alien_x_offset,formation= self.alien_cols,x_start = 0,y_start =180)
        self.alien_setup(self.alien_formation)



    def create_obstacle(self,x_start, y_start,offset_x):
        for row_index, row in enumerate(self.shape):
            for column_index, col in enumerate(row):
                if col == 'x':
                    x = x_start  + column_index * self.block_size + offset_x
                    y = y_start + row_index  * self.block_size
                    block = Obstacle.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)

    def create_mutiple_obstacles(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_obstacle(x_start,y_start,offset_x)

    def alien_setup(self,formation,x_distance=40,y_distance=48,offset_x=10,offset_y=100):
        color = {
            1:'red',
            2:'yellow',
            3:'green',
        }

        # 40 is the width of the alien | space between alien is 20 -> 60
        # alien amount = count 'x' in the formation
        # x_start = (screen_width / alien_amount*60) / 2
        alien_amount = []
        x_start = [
            num for num in range(self.obstacle_amount) 
        ]
        for row_index,row in enumerate(formation):
            # random alien color on each row
            c = color[randint(1,3)]
            for columnn_index, col in enumerate(row):
                if col =='x':
                    x = columnn_index*x_distance + offset_x
                    y = row_index*y_distance + offset_y
                    # random alien color
                    # c = color[randint(1,3)] 
                    alien_sprite = Alien.Alien(c,x,y)
                    self.aliens.add(alien_sprite)

    # This is in main.py because it need to check out all the aliens which is being
    # setup in the main.py file
    # really want to put these alien control block inside the alien class but idk how
    def alien_side_pos_checker(self):
        for alien in self.aliens.sprites():
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            if alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)
    def alien_move_down(self,distance):
        if self.aliens: # avoid null ref
            for alien in self.aliens.sprites():
                alien.rect.y += distance
    def alien_shoot(self):
        if self.aliens.sprites(): # to avoid null ref
            #choose random in collections
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,speed=10,direction=0,screen_height=screen_height)
            self.alien_lasers.add(laser_sprite)
    

    # Extra alien methods
    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            # default speed for extra is 3
            print(self.extra_spawn_time) # debug
            self.extra.add(Alien.Extra(choice(['right','left']),screen_width=screen_width))
            self.extra_spawn_time = randint(400,800)


    # Collision
    def collision_checks(self):

        # player's lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacles collions
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                # aliens collisions
                if pygame.sprite.spritecollide(laser,self.aliens,True):
                    self.highscore+=10
                    laser.kill()

                # extra collisions
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    self.highscore+=100
                    laser.kill()

        # alien's laser
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacles collisions
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                # player collisions
                if pygame.sprite.spritecollide(laser,self.player,False):
                    print('alien\'s laser hit player')
                    laser.kill()
                    self.player.sprite.getHit()


        if self.aliens:
            for alien in self.aliens:
                if pygame.sprite.spritecollide(alien,self.player,False):
                    print('alien hit player')


    def run(self):

        # Debug
        if self.player.sprite.playerHP > 0:
            debug('Player HP: {}'.format(self.player.sprite.playerHP),y=40)
        else: debug('Player died',y=40)

        debug('Score: {}'.format(self.highscore),y=75)
        
        # update and draw all sprites groups
        
        # Colision 
        self.collision_checks()

        # Player update
        self.player.update()

        # Aliens update
        self.alien_side_pos_checker()
        # self.aliens.update(self.alien_direction)
        self.alien_lasers.update()
        
        self.extra_alien_timer()
        self.extra.update()

        # draw player
        self.player.draw(screen)

        # draw lasers
        self.player.sprite.lasers.draw(screen)

        # draw obstacles
        self.blocks.draw(screen)

        # draw alien
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)

if __name__  == '__main__':
    pygame.init()
    pygame.font.init()
    screen_width = 600
    screen_height = 600

    screen = pygame.display.set_mode((600,600))
    clock = pygame.time.Clock()

    game = Game() # create an instance of the game

    # The UserEvent will be sent out as an event signal
    # , repeated periodically after the specified time interval
    ALIENLASER = pygame.USEREVENT + 1 # EVENT ID 25
    pygame.time.set_timer(ALIENLASER,800)


    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot() # alien shooting laser
        screen.fill((30,30,30))

        game.run() #run the game and update game objects
        pygame.display.flip()
        clock.tick(60)