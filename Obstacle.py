import pygame

class Block(pygame.sprite.Sprite):
    '''
    Represent the obstacles in the game\n
    Attributes:
        image:      draw the sprite on screen
        rect:       object for storing rectangular coordinates
    '''
    def __init__(self,size,color,x,y):
        '''
        input:

        output: construct the Block
        '''
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))



# each x is a block with the size = Block's size
shape = [
'  xxxxxxx',
' xxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxx     xxx',
'xx       xx',
]