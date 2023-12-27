import pygame
from pygame import Surface

from square_cell import SquareCell
from algorithms.utils import Colors


class DFSMazeCell(SquareCell):
    def __init__(self, i: int, j: int, cell_size: int, num_cells_h: int, num_cells_v: int):
        SquareCell.__init__(self, i, j, cell_size, num_cells_h, num_cells_v)

        self.color = Colors.GREY
        self.lines = self.get_lines()

        self.neighbor_cells = []
        self.reachable_cells = []

    def get_lines(self):
        # Relative point positions:
        #   p1 - p2
        #   |    |
        #   p4 - p3
        p1 = (self.x_coord, self.y_coord)
        p2 = (self.x_coord + self.cell_size, self.y_coord)
        p3 = (self.x_coord + self.cell_size, self.y_coord + self.cell_size)
        p4 = (self.x_coord, self.y_coord + self.cell_size)

        lines = {'top': (p1, p2), 'bottom': (p3, p4), 'left': (p1, p4), 'right': (p2, p3)}
        return lines

    def get_reachable_cells(self, grid):
        self.reachable_cells = []
        if self.x_id < self.num_cells_h - 1:
            self.reachable_cells.append(grid[self.x_id + 1][self.y_id])
        if self.x_id > 0:
            self.reachable_cells.append(grid[self.x_id - 1][self.y_id])
        if self.y_id < self.num_cells_v - 1:
            self.reachable_cells.append(grid[self.x_id][self.y_id + 1])
        if self.y_id > 0:
            self.reachable_cells.append(grid[self.x_id][self.y_id - 1])

    def enable(self):
        if not self.is_start() and not self.is_end():
            self.color = Colors.WHITE
        self.visited = True

    def reset(self):
        if not self.is_start() and not self.is_end():
            self.color = Colors.BLACK

        self.dist = float('inf')
        self.g_score = float('inf')
        self.h_score = float('inf')
        self.prev = None

    def _draw_lines(self, screen: Surface):
        for line in self.lines.values():
            start_pos, end_pos = line
            pygame.draw.line(screen, Colors.BLACK.value, start_pos, end_pos, 3)

    def _pint(self, screen):
        rect = pygame.Rect(self.x_coord, self.y_coord, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, self.color.value, rect)

    def draw(self, screen: Surface):
        self._pint(screen)
        self._draw_lines(screen)
