from const import *
import pygame


class Button:
    def __init__(self, name, shape, pos, size,fill=False,rate=0):
        self.name = name
        self.shape = shape
        self.pos = pos
        self.size = size
        self.fill = fill
        self.color = BLACK
        self.radius = 10
        self.rate = rate

    def draw(self, win, fnt):
        if self.shape == 'circle':
            if self.fill:
                pygame.draw.circle(win, self.color, self.pos, self.radius)
            else:
                pygame.draw.circle(win, self.color, self.pos, self.radius, 1)
            text = fnt.render(self.name, 1, self.color)
            win.blit(text, (self.pos[0] + 1.5*self.radius, self.pos[1] - self.radius ))
        else:
            self.rect = (self.pos[0], self.pos[1], BUTTON_WIDTH, BUTTON_LENGTH)
            if self.fill:
                pygame.draw.rect(win, self.color, self.rect)
            else:
                pygame.draw.rect(win, self.color, self.rect, 1)
            text = fnt.render(self.name, 1, self.color)
            win.blit(text, (self.pos[0], self.pos[1] + 1.5 * BUTTON_LENGTH))
            if self.rate:
                self.rect_inside = (self.pos[0] + 2, self.pos[1] + 2, (BUTTON_WIDTH - 4) * self.rate // 100, BUTTON_LENGTH - 4)
                pygame.draw.rect(win, BLACK, self.rect_inside)

    def action(self, active=False):
        self.fill = True if active else False


class Menu:
    def __init__(self):
        self.rate = 30
        self.rect = Button('Rectangle', 'circle', (DISPLAY_WIDTH//6 * 4, DISPLAY_HEIGHT + MENU_HEIGHT//3 * 2), RADIO_RADIUS, True)
        self.diagonal = Button('Diagonal', 'circle', (DISPLAY_WIDTH//6 * 4, DISPLAY_HEIGHT + MENU_HEIGHT//3), RADIO_RADIUS)
        self.astar = Button('A*', 'circle', (DISPLAY_WIDTH//6 * 3, DISPLAY_HEIGHT + MENU_HEIGHT//4), RADIO_RADIUS)
        self.dsk = Button('Dijkstra', 'circle', (DISPLAY_WIDTH//6 * 3, DISPLAY_HEIGHT + MENU_HEIGHT//4 * 2), RADIO_RADIUS)
        self.fast = Button('Greedy', 'circle', (DISPLAY_WIDTH//6 * 3, DISPLAY_HEIGHT + MENU_HEIGHT//4 * 3), RADIO_RADIUS, True)
        self.dir1 = Button('1 Direction', 'circle', (DISPLAY_WIDTH//6 * 5, DISPLAY_HEIGHT + MENU_HEIGHT//3 * 2), RADIO_RADIUS, True)
        self.dir2 = Button('2 Direction', 'circle', (DISPLAY_WIDTH//6 * 5, DISPLAY_HEIGHT + MENU_HEIGHT//3), RADIO_RADIUS)
        self.generator = Button('Generate', 'rect', (DISPLAY_WIDTH//6 + 7 * BUTTON_LENGTH, DISPLAY_HEIGHT + MENU_HEIGHT//3), RADIO_RADIUS, False, self.rate)
        self.block = Button('Draw', 'rect', (10*BUTTON_LENGTH, DISPLAY_HEIGHT + MENU_HEIGHT//3), BUTTON_WIDTH)

    def draw(self, win, fnt):
        self.astar.draw(win, fnt)
        self.dsk.draw(win, fnt)
        self.rect.draw(win, fnt)
        self.diagonal.draw(win, fnt)
        self.dir1.draw(win, fnt)
        self.dir2.draw(win, fnt)
        self.generator.draw(win, fnt)
        self.block.draw(win, fnt)
        self.fast.draw(win, fnt)

    def help_swap(self, bt1, bt2):
        bt1.action(True)
        bt2.action(False)
        return bt1

    def swap(self, bt1, bt2, first=True):
        if first:
            return self.help_swap(bt1, bt2)
        else:
            return self.help_swap(bt2, bt1)

    def swap_button(self, bt1, bt2):
        bt1.fill = True
        bt2.fill = False

    def swap_radio(self, bt1, bt2):
        if bt1.fill:
            self.help_swap(bt2, bt1)
        else:
            self.help_swap(bt1, bt2)
    
    def swap_radio_3(self, bt1, bt2, bt3):
        bt1.action(True)
        bt2.action(False)
        bt3.action(False)

    def swap_algo(self):
        if self.astar.fill:
            self.swap_radio_3(self.dsk, self.astar, self.fast)
        elif self.dsk.fill:
            self.swap_radio_3(self.fast, self.astar, self.dsk)
        else:
            self.swap_radio_3(self.astar, self.dsk, self.fast)

    def control(self, pos):
        if pos[1] > DISPLAY_HEIGHT:
            print(self.astar.pos[0], pos[0])
            if pos[0] > self.dir2.pos[0] and pos[0] - RADIO_RADIUS and pos[0] < DISPLAY_WIDTH - 4*RADIO_RADIUS:
                if pos[1] >= self.dir2.pos[1]:
                    self.dir1.fill = True
                    self.dir2.fill = False
                else:
                    self.dir1.fill = False
                    self.dir2.fill = True
                self.block.fill = False
            elif pos[0] > self.diagonal.pos[0] - RADIO_RADIUS and pos[0] < self.dir2.pos[0] - 4*RADIO_RADIUS:
                if pos[1] >= self.rect.pos[1]:
                    self.diagonal.fill = False
                    self.rect.fill = True
                else:
                    self.diagonal.fill = True
                    self.rect.fill = False
                self.block.fill = False 
            elif pos[0] > self.astar.pos[0] - RADIO_RADIUS and pos[0] < self.diagonal.pos[0] - 4*RADIO_RADIUS:
                if pos[1] <= self.astar.pos[1] + RADIO_RADIUS:
                    self.astar.fill = True
                    self.dsk.fill = False
                    self.fast.fill = False
                elif pos[1] <= self.dsk.pos[1] + RADIO_RADIUS:
                    self.astar.fill = False
                    self.dsk.fill = True
                    self.fast.fill = False
                else:
                    self.astar.fill = False
                    self.dsk.fill = False
                    self.fast.fill = True
                self.block.fill = False
            elif pos[0] > self.generator.pos[0] and pos[0] < self.generator.pos[0] + BUTTON_WIDTH:
                if pos[1] > self.generator.pos[1] - BUTTON_LENGTH and pos[1] < self.generator.pos[1] + 4 * BUTTON_LENGTH:
                    self.generator.fill = True
                    self.block.fill = False
            elif pos[0] > self.block.pos[0] and pos[0] < self.block.pos[0] + BUTTON_WIDTH:
                if pos[1] > self.block.pos[1] - BUTTON_LENGTH and pos[1] < self.block.pos[1] + 4 * BUTTON_LENGTH:
                    self.block.fill = not self.block.fill