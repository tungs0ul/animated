import pygame, random, math, heapq, time, sys
from const import *
from pygame.locals import *
from graph import *
from menu import *


class Graphic:
    def __init__(self):
        self.src = self.dst = None
        self.astar = False
        self.diagonal = False
        self.single = True
        self.map = Graph()
        self.menu = Menu()
        self.src = None
        self.dst = None
        self.last_time = None
        self.last_visited = None
        self.last_path = None

    def draw(self, win, fnt):
        self.map.draw(win)
        self.menu.draw(win, fnt)

    def random_map(self, rate):
        for node in self.map.nodes:
            if node.color == BLACK:
                node.activate()
                if random.randint(1, 99) > 99 - rate:
                    node.deactivate()
        if not self.src:
            self.src = self.map.nodes[random.randint(0, (DISPLAY_HEIGHT//CELL_SIZE * DISPLAY_WIDTH//CELL_SIZE - 1))]  
            self.src.choose(RED)
        if not self.dst:  
            self.dst = self.map.nodes[random.randint(0, (DISPLAY_HEIGHT//CELL_SIZE * DISPLAY_WIDTH//CELL_SIZE - 1))]
            self.dst.choose(BLUE)    

    def setup(self, win, fnt, clock):
        setting = True
        clean = False
        while setting:
            win.fill(WHITE)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    pygame.quit()
                keys = pygame.key.get_pressed()
                pos = pygame.mouse.get_pos()
                if event.type == MOUSEBUTTONDOWN:
                    if not self.menu.block.fill:
                        if pos[1] <= DISPLAY_HEIGHT:
                            if event.button == 1 and not self.menu.block.fill:
                                posi = pos[0]//CELL_SIZE*(DISPLAY_HEIGHT//CELL_SIZE) + pos[1]//CELL_SIZE
                                if self.src:
                                    self.src.color = BLACK
                                    self.src.fill = False
                                self.src = self.map.nodes[posi]
                                self.src.choose(RED)
                            if event.button == 3 and not self.menu.block.fill:
                                    posi = pos[0]//CELL_SIZE*(DISPLAY_HEIGHT//CELL_SIZE) + pos[1]//CELL_SIZE
                                    if self.dst:
                                        self.dst.color = BLACK
                                        self.dst.fill = False
                                    self.dst = self.map.nodes[posi]
                                    self.dst.choose(BLUE)
                    if pos[1] > DISPLAY_HEIGHT:
                        if event.button == 1:
                            self.menu.control(pos)
                        if self.menu.generator.fill:
                            self.random_map(self.menu.generator.rate)
                            self.menu.generator.fill = False
                    else:
                        if event.button == 1:
                            clean = False
                        elif event.button == 3:
                            clean = True
                if event.type == MOUSEMOTION and self.menu.block.fill:
                    pos = pygame.mouse.get_pos()
                    if pos[1] <= DISPLAY_HEIGHT:
                        posi = pos[0]//CELL_SIZE*(DISPLAY_HEIGHT//CELL_SIZE) + pos[1]//CELL_SIZE
                        if self.map.nodes[posi].color == BLACK:
                            if clean:
                                self.map.nodes[posi].activate()
                            else:
                                self.map.nodes[posi].deactivate()
                if (keys[K_RIGHT] or keys[K_d]) and self.menu.generator.rate < 100:
                    self.menu.generator.rate += 5
                    self.menu.block.fill = False
                if (keys[K_LEFT] or keys[K_a]) and self.menu.generator.rate > 0:
                    self.menu.generator.rate -= 5
                    self.menu.block.fill = False
                if (keys[K_RETURN]) and self.src and self.dst:
                    setting = False
                    self.menu.block.fill = False
                if keys[K_1]:
                    self.menu.block.fill = not self.menu.block.fill
                if keys[K_2]:
                    self.random_map(self.menu.generator.rate)
                    self.menu.block.fill = False
                if keys[K_3]:
                    self.menu.swap_algo()
                    self.menu.block.fill = False
                if keys[K_4]:
                    self.menu.swap_radio(self.menu.diagonal, self.menu.rect)
                    self.menu.block.fill = False
                if keys[K_5]:
                    self.menu.swap_radio(self.menu.dir1, self.menu.dir2)
                    self.menu.block.fill = False
                if keys[K_ESCAPE]:
                    for node in self.map.nodes:
                        if node.color == BLACK:
                            node.activate()
            if self.last_time:
                text = fnt.render(self.last_time, 1, BLACK)
                win.blit(text, (100, 610))
                text = fnt.render(self.last_visited, 1, BLACK)
                win.blit(text, (100, 640))
                text = fnt.render(self.last_path, 1, BLACK)
                win.blit(text, (100, 670))
            self.draw(win, fnt)
            pygame.display.update()
            clock.tick(60)

    def showing(self, win, fnt, clock):
        self.src.active = True
        self.dst.active = True
        finding = True
        counting = True
        time_start = time.time()

        nodes_src = []
        distance_src  = {}
        distance_src[self.src] = 0
        previous_src = {}
        heapq.heapify(nodes_src)
        heapq.heappush(nodes_src, (distance_src[self.src], self.src))
        current_from_src = self.src

        nodes_dst = []
        distance_dst = {}
        distance_dst[self.dst] = 0
        previous_dst = {}
        heapq.heapify(nodes_dst)
        heapq.heappush(nodes_dst, (distance_dst[self.dst], self.dst))
        current_from_dst = self.dst
        self.found_src = self.found_dst = None
        self.src.h = self.src.g = self.src.f = 0
        self.dst.h = self.dst.g = self.dst.f = 0
        visited = 0
        path = set()
        i = 0
        while finding:
            if counting:
                time_end = time.time()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    pygame.quit()
                keys = pygame.key.get_pressed()
            win.fill(WHITE)
            if len(nodes_src):
                current_from_src = heapq.heappop(nodes_src)[1]
                if current_from_src != self.src:
                    current_from_src.choose(LIGHTRED, False)
                for node in self.map.neighbors(current_from_src, self.menu.diagonal.fill):
                    f = distance_src[current_from_src] + math.sqrt((current_from_src.x - node.x)**2 + (current_from_src.y - node.y)**2)
                    if (node not in distance_src) or (distance_src[node] > f):
                        node.g = current_from_src.g + 1
                        node.h = f
                        node.f = node.g + node.h
                        visited += 1
                        if node != self.dst:
                            node.choose(YELLOW)
                        distance_src[node] = f
                        previous_src[node] = current_from_src
                        if self.menu.astar.fill:
                            heapq.heappush(nodes_src, (node.f + math.sqrt((self.dst.x - node.x)**2 + (self.dst.y - node.y)**2), node))
                        elif self.menu.fast.fill:
                            heapq.heappush(nodes_src, (distance_src[node] + (node.x - self.dst.x)**2 + (node.y - self.dst.y)**2, node))
                        else:
                            heapq.heappush(nodes_src, (distance_src[node], node))
                    if node in distance_dst:
                        nodes_dst.clear()
                        nodes_src.clear()
                        self.found_dst = node
                        self.found_src = node 
                if self.dst in distance_src:
                    nodes_src.clear()
                    self.found_dst = previous_src[self.dst]
                if self.menu.dir2.fill:
                    if len(nodes_dst):
                        current_from_dst = heapq.heappop(nodes_dst)[1]
                        if current_from_dst != self.dst:
                            current_from_dst.choose(LIGHTBLUE, False)
                        for node in self.map.neighbors(current_from_dst, self.menu.diagonal.fill):
                            f = distance_dst[current_from_dst] + math.sqrt((current_from_dst.x - node.x)**2 + (current_from_dst.y - node.y)**2)
                            if (node not in distance_dst) or (distance_dst[node] > f):
                                node.g = current_from_dst.g + 1
                                node.h = f
                                node.f = node.g + node.h
                                visited += 1
                                if node != self.src:
                                    node.choose(YELLOW)
                                distance_dst[node] = f
                                previous_dst[node] = current_from_dst
                                if self.menu.astar.fill:
                                    heapq.heappush(nodes_dst, (node.f + math.sqrt((self.src.x - node.x)**2 + (self.src.y - node.y)**2), node))
                                elif self.menu.fast.fill:
                                    heapq.heappush(nodes_dst, (distance_dst[node] + (node.x - self.src.x)**2 + (node.y - self.src.y)**2, node))
                                else:
                                    heapq.heappush(nodes_dst, (distance_dst[node], node))
                        if current_from_dst in distance_src:
                            nodes_dst.clear()
                            nodes_src.clear()
                            self.found_dst = current_from_dst
                            self.found_src = current_from_dst
                    else:
                        nodes_src.clear()
            else:
                if self.found_dst:
                    if self.found_dst != self.src:
                        self.found_dst.choose(GREEN)
                        self.found_dst = previous_src[self.found_dst]
                        path.add(self.found_dst)
                    if self.found_src != self.dst:
                        self.found_src.choose(GREEN)
                        self.found_src = previous_dst[self.found_src]
                        path.add(self.found_src)
                    else:
                        counting = False
                        if keys[K_SPACE]:
                            self.last_time = str(round(time_end - time_start, 2)) + 's'
                            self.last_visited = str(visited)
                            self.last_path = str(len(path)) if self.menu.dir1.fill else str(len(path) - 1)
                            finding = False
                            for node in self.map.nodes:
                                if (not node.fill) or (node.color in (YELLOW, GREEN)):
                                    node.choose(BLACK, False)
                        if keys[K_ESCAPE]:
                            pygame.quit()          
                else:
                    if keys[K_SPACE]:
                        self.last_path = self.last_visited = self.last_time = None
                        finding = False
                        for node in self.map.nodes:
                            if (not node.fill) or (node.color in (YELLOW, GREEN)):
                                node.choose(BLACK, False)
                    if keys[K_ESCAPE]:
                        pygame.quit()
                        counting = False
            text = str(round(time_end - time_start, 2)) + 's'
            text = fnt.render(text, 1, RED)  
            win.blit(text, (20, 610))
            text = fnt.render(str(visited), 1, ORANGE)  
            win.blit(text, (20, 640))
            if self.last_time:
                text = fnt.render(self.last_time, 1, BLACK)
                win.blit(text, (100, 610))
                text = fnt.render(self.last_visited, 1, BLACK)
                win.blit(text, (100, 640))
                text = fnt.render(self.last_path, 1, BLACK)
                win.blit(text, (100, 670))
            if len(path):
                text = fnt.render(str(len(path)), 1, GREEN) if self.menu.dir1.fill else fnt.render(str(len(path) - 1), 1, GREEN)
                win.blit(text, (20, 670))
            self.draw(win, fnt)
            pygame.display.update()
            clock.tick(60)