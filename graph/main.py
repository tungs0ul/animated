from const import *
import pygame, sys
from pygame.locals import *
from graph import *
import heapq

pygame.init()
pygame.font.init()
win = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()

fnt = pygame.font.SysFont("comicsans", 40)
playing = True

while playing: 
    running = True
    g = Graph()
    drawing = True
    cleaning = False
    g.nodes[0].choose(RED)
    g.nodes[1199].choose(BLUE)
    while running:
        win.fill(WHITE)
        g.draw(win)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    cleaning = False
                    drawing = not drawing
                if event.button == 3:
                    drawing = True
                    cleaning = not cleaning
            if event.type == MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                posi = pos[0]//20*30 + pos[1]//20
                if not drawing:
                    if g.nodes[posi].color == BLACK:
                        g.nodes[posi].deactivate()
                if cleaning:
                    if g.nodes[posi].color == BLACK:
                        g.nodes[posi].activate()
            if keys[K_RETURN]:
                running = False
        pygame.display.update()
        clock.tick(60)
    finding = True
    result = []
    distance = {}
    previous = {}
    src = g.nodes[0]
    dst = g.nodes[1199]
    distance[src] = 0
    nodes = []
    heapq.heapify(nodes)
    heapq.heappush(nodes, (distance[src], src))
    show = False
    while finding:
        win.fill(WHITE)
        if len(nodes):
            current_node = heapq.heappop(nodes)[1]
            for node in g.neighbors(current_node):
                if node not in distance or distance[node] > 1 + distance[current_node]:
                    if not ((node.x == dst.x) and (node.y == dst.y)):
                        node.choose(LIGHTGRAY)
                    distance[node] = 1 + distance[current_node]
                    previous[node] = current_node
                    heapq.heappush(nodes, (distance[node], node))
        else:
            if not show:
                if dst in previous:
                    show = True
                    node = previous[dst]
                else:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        keys = pygame.key.get_pressed()
                        if keys[K_RETURN]:
                            finding = False     
                        if keys[K_ESCAPE]:
                            finding = False
                            playing = False    
            else:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    keys = pygame.key.get_pressed()
                if node != src:
                    node.choose(GREEN)
                    node = previous[node]
                else:
                    if keys[K_RETURN]:
                        finding = False     
                    if keys[K_ESCAPE]:
                        finding = False
                        playing = False           
        g.draw(win)
        pygame.display.update()
        clock.tick(60)
                       