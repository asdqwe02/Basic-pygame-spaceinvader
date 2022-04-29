
import pygame
# DEBUG
pygame.init()
font = pygame.font.Font(None,25)
def debug(info, y =10, x=10):
    display_surf=pygame.display.get_surface()
    
    # Note: can't write in parameter antialias= True 
    debug_surf = font.render(str(info),True,'White')
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    display_surf.blit(debug_surf,debug_rect)