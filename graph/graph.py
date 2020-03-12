import pygame, random
from const import *

class Node:
    def __init__(self, x, y):
        self.active = True
        self.x = x
        self.y = y
        self.fill = False
        self.color = BLACK
        self.f = self.g = self.h = 2**32

    def draw(self, win):
        self.rect = (self.x, self.y, CELL_SIZE, CELL_SIZE)
        if not self.fill:
            pygame.draw.rect(win, self.color, self.rect, 1)
        else:
            pygame.draw.rect(win, self.color, self.rect)

    def deactivate(self):
        self.active = False
        self.fill = True
    
    def activate(self):
        self.active = True
        self.fill = False

    def choose(self, color, fill=True):
        self.color = color
        self.fill = fill

    def __lt__(self, other):
        return self.f < other.f

    def __str__(self):
        return str(self.x) + ':' + str(self.y)

class Graph:
    def __init__(self):
        self.nodes = [Node(CELL_SIZE*x, CELL_SIZE*y) for x in range(DISPLAY_WIDTH//CELL_SIZE) for y in range(DISPLAY_HEIGHT//CELL_SIZE)]

    def draw(self, win):
        for node in self.nodes:
            node.draw(win)

    def find_node(self, x, y):
        for i, node in enumerate(self.nodes):
            if node.x == x and node.y == y:
                return i
        return None

    def neighbors(self, node, diagonal=False):
        result = set()
        if self.find_node(node.x, node.y+CELL_SIZE) is not None and self.nodes[self.find_node(node.x, node.y+CELL_SIZE)].active:
            result.add(self.nodes[self.find_node(node.x, node.y+CELL_SIZE)])
        if self.find_node(node.x+CELL_SIZE, node.y) is not None and self.nodes[self.find_node(node.x+CELL_SIZE, node.y)].active:
            result.add(self.nodes[self.find_node(node.x+CELL_SIZE, node.y)])
        if self.find_node(node.x, node.y-CELL_SIZE) is not None and self.nodes[self.find_node(node.x, node.y-CELL_SIZE)].active:
            result.add(self.nodes[self.find_node(node.x, node.y-CELL_SIZE)])
        if self.find_node(node.x-CELL_SIZE, node.y) is not None and self.nodes[self.find_node(node.x-CELL_SIZE, node.y)].active:
            result.add(self.nodes[self.find_node(node.x-CELL_SIZE, node.y)])
        if diagonal:
            if self.find_node(node.x+CELL_SIZE, node.y+CELL_SIZE) is not None and self.nodes[self.find_node(node.x+CELL_SIZE, node.y+CELL_SIZE)].active:
                result.add(self.nodes[self.find_node(node.x+CELL_SIZE, node.y+CELL_SIZE)])
            if self.find_node(node.x+CELL_SIZE, node.y-CELL_SIZE) is not None and self.nodes[self.find_node(node.x+CELL_SIZE, node.y-CELL_SIZE)].active:
                result.add(self.nodes[self.find_node(node.x+CELL_SIZE, node.y-CELL_SIZE)])
            if self.find_node(node.x-CELL_SIZE, node.y+CELL_SIZE) is not None and self.nodes[self.find_node(node.x-CELL_SIZE, node.y+CELL_SIZE)].active:
                result.add(self.nodes[self.find_node(node.x-CELL_SIZE, node.y+CELL_SIZE)])
            if self.find_node(node.x-CELL_SIZE, node.y-CELL_SIZE) is not None and self.nodes[self.find_node(node.x-CELL_SIZE, node.y-CELL_SIZE)].active:
                result.add(self.nodes[self.find_node(node.x-CELL_SIZE, node.y-CELL_SIZE)])
        return result

# (x*30 + y)//20