import pygame
from graph import *
from menu import *
from graphic import *

def main():
    pygame.init()
    pygame.font.init()

    win = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT + MENU_HEIGHT))
    fnt = pygame.font.SysFont("comicsans", 25)
    clock = pygame.time.Clock()
    
    g = Graphic()
    while True:
        g.setup(win, fnt, clock)
        g.showing(win, fnt, clock)


if __name__ == '__main__':
    main()