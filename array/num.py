import random
from const import *
import pygame
from pygame.locals import *

class Num:
    def __init__(self, num, x, y, width=NUM_BOX_WIDTH, height=NUM_BOX_HEIGHT):
        self.num = num
        self.x = self.x_start = x
        self.y = self.y_start = y
        self.width = width
        self.height = height
        self.color = BLACK
        self.hide = True

    def reset(self):
        self.x = self.x_start
        self.y = self.y_start

    def hiding(self):
        self.hide = True

    def discovered(self):
        self.hide = False

    def change_color(self, color):
        self.color = color

    def move_down(self):
        self.y += 90
    
    def move_left(self):
        self.x -= 82

    def move_right(self):
        self.x += 82
    
    def move_up(self):
        self.y -= 90

    def draw(self, win):
        self.rect = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, self.color, self.rect, 3)
        if not self.hide:
            fnt = pygame.font.SysFont("comicsans", 40)
            text = fnt.render(str(self.num), 1, BLUE)
            win.blit(text, (self.x + 20, self.y + 15))

    def __lt__(self, other):
        return self.num < other.num

    def __str__(self):
        return str(self.num)


class Nums:
    def __init__(self, binary=False):
        nums = [random.randint(0, 9) for i in range(10)]
        if binary:
            nums.sort()
        self.nums = [Num(nums[i], (NUM_BOX_WIDTH + NUM_BOX_GAP) * i, NUM_BOX_Y) for i in range(10)]

    def __str__(self):
        result = ""
        for num in self.nums:
            result += ' ' + str(num.num)
        return result

    def draw(self, win):
        for num in self.nums:
            num.draw(win)


class Pointer:
    def __init__(self, x, y, width, height, color, posi=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.active = False
        self.posi = posi

    def activate(self):
        self.active = True

    def draw(self, win):
        self.rect = (self.x, self.y, self.width, self.height)
        if self.active:
            pygame.draw.rect(win, self.color, self.rect)
    
    def move(self,left=True,step=1):
        if left:
            self.x -= step * (NUM_BOX_GAP + NUM_BOX_WIDTH)
        else:
            self.x += step * (NUM_BOX_GAP + NUM_BOX_WIDTH)

    def deactivate(self):
        self.active = False