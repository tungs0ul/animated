import pygame
from pygame.locals import *
from const import *
from num import *
import sys
import random

pygame.init()
pygame.font.init()
win = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()

fnt = pygame.font.SysFont("comicsans", 40)

running = True
exit_text = fnt.render("press enter to play again, escape to exit", 1, BLACK)


while running:
    menu = True
    binary = False
    time = 0

    while menu:
        win.fill(WHITE)
        text = fnt.render("press b for binary, l for linear", 1, RED)
        win.blit(text, (200, 50))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            if keys[K_b]:
                binary = True
                menu = False
            if keys[K_l]:
                menu = False
        clock.tick(30)
        pygame.display.update()

    a = Nums(binary)
    p_low = Pointer(POINTER_X - 5, POINTER_Y, POINTER_WIDTH, POINTER_HEIGHT, RED)
    p_high = Pointer(POINTER_X + 5, POINTER_Y, POINTER_WIDTH, POINTER_HEIGHT, BLACK, 9)
    p_high.move(left=False, step=9)
    p_mid = Pointer(POINTER_X, POINTER_Y, POINTER_WIDTH, POINTER_HEIGHT, BLUE, 4)
    p_mid.move(left=False, step=4)
    x = random.randint(0, 9)

    searching = True
    while searching:
        time += 1
        if time == 2:
                p_low.activate()
                if binary:
                    p_high.activate()
                    p_mid.activate()
        if not time % 30:
            win.fill(WHITE)
            if not binary:
                if p_low.posi <= p_high.posi:
                    a.nums[p_low.posi].discovered()
                    if a.nums[p_low.posi].num != x:
                        a.nums[p_low.posi].move_down()
                        p_low.move(left=False)
                        p_low.posi += 1
                    else:
                        a.nums[p_low.posi].color = GREEN
                        p_low.deactivate()
                        text = fnt.render(str(x) + f" found at index {p_low.posi}.", 1, RED)
                        win.blit(text, (250, 100))
                        win.blit(exit_text, (150, 25))
                else:
                    text = fnt.render(str(x) + " not found!", 1, RED)
                    win.blit(text, (300, 100))
                    win.blit(exit_text, (150, 25))
            else:
                if p_low.posi <= p_high.posi:
                    p_mid.posi = (p_high.posi + p_low.posi) // 2
                    a.nums[p_mid.posi].discovered()
                    if a.nums[p_mid.posi].num < x:
                        p_low.move(left=False, step=(p_mid.posi + 1 - p_low.posi))
                        p_low.posi = p_mid.posi + 1
                        p_mid.move(left=False, step=(p_high.posi + p_low.posi) // 2 - p_mid.posi)
                    elif a.nums[p_mid.posi].num > x:
                        p_high.move(step=(p_high.posi - p_mid.posi + 1))
                        p_high.posi = p_mid.posi - 1
                        p_mid.move(step=p_mid.posi - (p_high.posi + p_low.posi) // 2)
                    else:
                        text = fnt.render(str(x) + f" found at index {p_mid.posi}.", 1, RED)
                        win.blit(text, (250, 100))
                        win.blit(exit_text, (150, 25))
                else:
                    text = fnt.render(str(x) + " not found!", 1, RED)
                    win.blit(text, (300, 100))
                    win.blit(exit_text, (150, 25))
        pygame.draw.rect(win, GREEN, (369, 500, 60, 60), 3)
        text = fnt.render(str(x), 1, RED)
        win.blit(text, (390, 515))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            if keys[K_RETURN]:
                searching = False
            if keys[K_ESCAPE]:
                searching = False
                running = False
        a.draw(win)
        p_low.draw(win)
        p_high.draw(win)
        p_mid.draw(win)
        pygame.display.update()
        clock.tick(30)