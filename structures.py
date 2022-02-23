from copy import deepcopy
from random import randrange

import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[pygame.color.Color(0, 0, 0)] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.figures = []
    
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        return self
    
    def render(self, surface):
        self.render_colors()
        for i, j in enumerate(self.board):
            for k, m in enumerate(j):
                pygame.draw.rect(surface, "white", (self.left + self.cell_size * k, self.top + self.cell_size * i,
                                                    self.cell_size, self.cell_size), 1)
                if m:
                    pygame.draw.rect(surface, m,
                                     (self.left + self.cell_size * k + 1, self.top + self.cell_size * i + 1,
                                      self.cell_size - 2, self.cell_size - 2))
    
    def get_cell(self, mouse_pos):
        x_pos = mouse_pos[0] // self.cell_size - 2
        y_pos = mouse_pos[1] // self.cell_size - 2
        if x_pos > self.width - 1 or mouse_pos[0] < self.left or y_pos > self.height - 1 or mouse_pos[1] < self.top:
            return None
        return x_pos, y_pos
    
    def on_click(self, cell_coords):
        if cell_coords[0] > self.width or cell_coords[1] > self.height:
            raise ValueError
    
    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if not cell:
            return None
        self.on_click(cell)
        
    def generate_figures_map(self, this):
        f_map = [[0] * self.width for _ in range(self.height)]
        for i in self.figures:
            if this != i:
                for j in i.coords:
                    f_map[j[1]][j[0]] = 1
        return f_map
                    
    def render_colors(self):
        self.board = [[pygame.color.Color(0, 0, 0)] * self.width for _ in range(self.height)]
        for i in self.figures:
            i.draw()


class Figure:
    def __init__(self, parent: Board, *coords: list, color: pygame.color.Color = None):
        self.coords = list(deepcopy(coords))
        self.color = color if color else pygame.color.Color(randrange(256), randrange(256), randrange(256))
        self.parent = parent
        self.active = True
        parent.figures.append(self)
        
    def draw(self):
        for i in self.coords:
            self.parent.board[i[1]][i[0]] = self.color
            
    def move(self, x: int = 0, y: int = 0):
        m = self.parent.generate_figures_map(self)
        for i in self.coords:
            if i[0] + x > self.parent.width - 1 or i[0] + x < 0 or\
                    i[1] + y > self.parent.height - 1 or i[1] + y < 0:
                return False
            if m[i[1] + y][i[0] + x]:
                return False
        for i in self.coords:
            i[0] += x
            i[1] += y
        return True
