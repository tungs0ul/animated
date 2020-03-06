class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = BLACK
        self.active = True
        self.g = self.h = self.f


class Graph:
    def __init__(self):
        self.nodes = []