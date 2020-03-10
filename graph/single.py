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
                posi = pos[0]//CELL_SIZE*(DISPLAY_HEIGHT//CELL_SIZE) + pos[1]//CELL_SIZE
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
                posi = pos[0]//CELL_SIZE*(DISPLAY_HEIGHT//CELL_SIZE) + pos[1]//CELL_SIZE
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
    nodes.clear()
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
            if current_node != src:
                current_node.choose(LIGHTGRAY, False)
            for node in g.neighbors(current_node, DIAGONAL):
                f = distance[current_node]
                if DIAGONAL:
                    f += (current_node.x - node.x)**2 + (current_node.y - node.y)**2
                if ASTAR:
                    f += (dst.y - node.y)**2 + (dst.x - node.x)**2
                else:
                    f += 1
                if node not in distance or distance[node] > f:
                    if not ((node.x == dst.x) and (node.y == dst.y)):
                        node.choose(YELLOW)
                    distance[node] = f
                    previous[node] = current_node
                    heapq.heappush(nodes, (distance[node], node))
                if dst in distance:
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
                    counting = False 
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
        text = str(round(time_current - time_start, 2))
        text = fnt.render(text, 1, RED)
        win.blit(text, (720, 10))
        pygame.display.update()
        clock.tick(60)