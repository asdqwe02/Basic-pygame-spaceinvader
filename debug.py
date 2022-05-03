
import pygame
# DEBUG
pygame.init()
font = pygame.font.Font(None,25)
def debug(info, y =10, x=10):
    ''' 
    input: 
        info:   information to print
        x:      position of the x axis on screen
        y:      position of the y axis on screen
    output: info is print at position x,y on screen
    '''

    display_surf=pygame.display.get_surface()
    # Note: can't write in parameter antialias= True 
    debug_surf = font.render(str(info),True,'White')
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    display_surf.blit(debug_surf,debug_rect)