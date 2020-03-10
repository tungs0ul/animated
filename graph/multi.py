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
    distance_1 = {}
    previous = {}
    previous_1 = {}
    src = g.nodes[src_posi]
    dst = g.nodes[dst_posi]

    distance[src] = 0
    nodes = []
    nodes.clear()
    heapq.heapify(nodes)
    heapq.heappush(nodes, (distance[src], src))

    nodes_1 = []
    distance_1[dst] = 0
    nodes_1.clear()
    heapq.heapify(nodes_1)
    heapq.heappush(nodes_1, (distance_1[dst], dst))


    show = False
    time_start = time.time()
    counting = True
    finish = False
    found = False
    while finding:
        if counting:
            time_current = time.time()
        win.fill(WHITE)
        if len(nodes_1):
            current_node_1 = heapq.heappop(nodes_1)[1]
            if current_node_1 != dst:
                current_node_1.choose(LIGHTGRAY, False)
            for node in g.neighbors(current_node_1, DIAGONAL):
                f = distance_1[current_node_1]
                if DIAGONAL:
                    f += (current_node_1.x - node.x)**2 + (current_node_1.y - node.y)**2
                if ASTAR:
                    f += (src.y - node.y)**2 + (src.x - node.x)**2
                else:
                    f += 1
                if node not in distance_1 or distance_1[node] > f:
                    if not ((node.x == src.x) and (node.y == src.y)):
                        node.choose(YELLOW)
                    distance_1[node] = f
                    previous_1[node] = current_node_1
                    heapq.heappush(nodes_1, (distance_1[node], node))
            if current_node_1 in distance:
                nodes.clear()
                nodes_1.clear()
                finish = True
                my_node = current_node_1
                my_node_1 = current_node_1
                found = True
                counting = False

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
                if current_node in distance_1:
                    nodes.clear()
                    nodes_1.clear()
                    finish = True
                    my_node = current_node
                    my_node_1 = current_node
                    found = True
                    counting = False
                    
        if not len(nodes) and (not len(nodes_1)):
            finish = True
        
        if finish:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                keys = pygame.key.get_pressed()
                if show:
                    if keys[K_RETURN]:
                        finding = False     
                    if keys[K_ESCAPE]:
                        finding = False
                        playing = False
                    counting = False
            if found:
                if my_node != src:
                    my_node.choose(GREEN)
                    my_node = previous[my_node]
                if my_node_1 != dst:
                    my_node_1.choose(GREEN)
                    my_node_1 = previous_1[my_node_1]
                if my_node == src and my_node_1 == dst:
                    show = True
            else:  
                text = str("No path found!")
                text = fnt.render(text, 1, RED)
                win.blit(text, (200, 400))
                show = True
        g.draw(win)
        text = str(round(time_current - time_start, 2))
        text = fnt.render(text, 1, RED)
        win.blit(text, (720, 10))
        pygame.display.update()
        clock.tick(60)
                       