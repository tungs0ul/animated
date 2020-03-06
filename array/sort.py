import pygame
from pygame.locals import *
from const import *
from num import *
import sys
import random
import time

pygame.init()
pygame.font.init()
win = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()

fnt = pygame.font.SysFont("comicsans", 40)

running = True

while running:
    sorting = True
    a = Nums()
    p_low = Pointer(POINTER_X - 5, POINTER_Y, POINTER_WIDTH, POINTER_HEIGHT, RED)
    p_high = Pointer(POINTER_X + 5, POINTER_Y, POINTER_WIDTH, POINTER_HEIGHT, BLACK)
    p_min = Pointer(POINTER_X, POINTER_Y, POINTER_WIDTH, POINTER_HEIGHT, BLUE)
    time = 0
    changed = True
    min_found = False
    min = 9
    while sorting:
        win.fill(WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[K_RETURN] and p_low.posi == 9:
            sorting = False
        if keys[K_ESCAPE] and p_low.posi == 9:
            sorting = False
            running = False
        time += 1
        if time == 30:
            p_low.activate()
            p_high.activate()
            p_min.activate()
        if p_low.posi > 8:
            text = fnt.render("press enter to do again, escape to exit", 1, RED)
            win.blit(text, (125, 100))
        if (not time%10)and (time>30):
            if not min_found:
                min = a.nums[p_low.posi]
                min_found = True
            if changed:
                if p_low.posi < 9:
                    if p_high.posi < 9:
                        p_high.move(left=False)
                        p_high.posi += 1
                        if a.nums[p_high.posi] < min:
                            min = a.nums[p_high.posi]
                            p_min.posi = p_high.posi
                            p_min.x = p_high.x - 5
                    else:
                        changed = False
                        min_found = True
            else:
                tmp = a.nums[p_low.posi].num
                if (a.nums[p_low.posi].x != a.nums[p_min.posi].x_start) and (a.nums[p_low.posi].y == a.nums[p_min.posi].y_start):
                    if a.nums[p_low.posi].y == a.nums[p_low.posi].y_start:
                        a.nums[p_min.posi].move_down()
                        a.nums[p_low.posi].move_down()
                elif (a.nums[p_low.posi].x != a.nums[p_min.posi].x_start) and (a.nums[p_low.posi].y != a.nums[p_min.posi].y_start):
                    a.nums[p_min.posi].move_left()
                    a.nums[p_low.posi].move_right()
                elif (a.nums[p_low.posi].y != a.nums[p_min.posi].y_start):
                    a.nums[p_min.posi].move_up()
                    a.nums[p_low.posi].move_up()
                else:
                    changed = True
                    a.nums[p_low.posi].num = a.nums[p_min.posi].num
                    a.nums[p_min.posi].num = tmp
                    a.nums[p_low.posi].reset()
                    a.nums[p_low.posi].change_color(GREEN)
                    a.nums[p_min.posi].reset()
                    p_low.posi += 1
                    p_low.move(left=False)
                    p_min.posi = p_high.posi = p_low.posi
                    p_high.x = p_low.x + 10
                    p_min.x = p_low.x + 5
                    min_found = False
                    for i in range(p_low.posi + 1, len(a.nums)):
                        a.nums[i].hiding()
                    if p_low.posi == 9:
                        a.nums[9].change_color(GREEN)
            a.nums[p_low.posi].discovered()
            a.nums[p_high.posi].discovered()
        a.draw(win)
        p_high.draw(win)
        p_low.draw(win)
        p_min.draw(win)
        pygame.display.update()
        clock.tick(30)
