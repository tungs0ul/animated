import pygame
from const import *

class Node:
    def __init__(self, x, y):
        self.active = True
        self.x = x
        self.y = y
        self.fill = False
        self.color = BLACK

    def draw(self, win):
        self.rect = (self.x, self.y, 20, 20)
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

    def choose(self, color):
        self.color = color
        self.fill = True

    def __lt__(self, other):
        return self.x**2 + self.y**2 < other.x**2 + self.y**2

    def __str__(self):
        return str(self.x) + ':' + str(self.y)

class Graph:
    def __init__(self):
        self.nodes = [Node(20*x, 20*y) for x in range(40) for y in range(30)]

    def draw(self, win):
        for node in self.nodes:
            node.draw(win)

    def find_node(self, x, y):
        for i, node in enumerate(self.nodes):
            if node.x == x and node.y == y:
                return i
        return None

    def neighbors(self, node):
        result = set()
        if self.find_node(node.x, node.y+20) and self.nodes[self.find_node(node.x, node.y+20)].active:
            result.add(self.nodes[self.find_node(node.x, node.y+20)])
        if self.find_node(node.x+20, node.y) and self.nodes[self.find_node(node.x+20, node.y)].active:
            result.add(self.nodes[self.find_node(node.x+20, node.y)])
        if self.find_node(node.x, node.y-20) and self.nodes[self.find_node(node.x, node.y-20)].active:
            result.add(self.nodes[self.find_node(node.x, node.y-20)])
        if self.find_node(node.x-20, node.y) and self.nodes[self.find_node(node.x-20, node.y)].active:
            result.add(self.nodes[self.find_node(node.x-20, node.y)])
        return result

# (x*30 + y)//20