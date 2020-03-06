from const import *
import pygame, sys
from pygame.locals import *
from graph import *
import heapq
import time, datetime

pygame.init()
pygame.font.init()
win = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()

fnt = pygame.font.SysFont("comicsans", 40)
playing = True

while playing: 
    running = True
    g = Graph()
    start = True
    src = False
    dst = False
    while start:
        win.fill(WHITE)
        g.draw(win)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                posi = pos[0]//20*30 + pos[1]//20
                if event.button == 1 and not src:
                    g.nodes[posi].choose(RED)
                    src = True
                    src_posi = posi
                if event.button == 3 and not dst:
                    g.nodes[posi].choose(BLUE)
                    dst = True
                    dst_posi = posi
                if src and dst:
                    start = False
        pygame.display.update()
        clock.tick(60)
    drawing = True
    cleaning = False
    g.nodes[src_posi].choose(RED)
    g.nodes[dst_posi].choose(BLUE)
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
    src = g.nodes[src_posi]
    dst = g.nodes[dst_posi]
    distance[src] = 0
    nodes = []
    heapq.heapify(nodes)
    heapq.heappush(nodes, (distance[src], src))
    show = False
    time_start = time.time()
    counting = True
    while finding:
        if counting:
            time_current = time.time()
        win.fill(WHITE)
        if len(nodes):
            current_node = heapq.heappop(nodes)[1]
            for node in g.neighbors(current_node):
                f = 1 + distance[current_node] # + (dst.y - node.y)**2 + (dst.x - node.x)**2
                if node not in distance or distance[node] > f:
                    if not ((node.x == dst.x) and (node.y == dst.y)):
                        node.choose(LIGHTGRAY)
                    distance[node] = f
                    previous[node] = current_node
                    heapq.heappush(nodes, (distance[node], node))
                if node.x == dst.x and node.y == dst.y:
                    nodes.clear()
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
                    counting = False
        g.draw(win)
        text = str(int(time_current - time_start))
        text = fnt.render(text, 1, RED)
        win.blit(text, (750, 10))
        pygame.display.update()
        clock.tick(60)
                       