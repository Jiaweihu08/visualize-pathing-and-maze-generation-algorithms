import pygame
from pygame import Surface

from algorithms.utils import Colors


class SquareCell:
    # Pygame coordinate system has the origin in the top-left corner,
    # with the x-axis growing from left to right, and the y-axis from
    # top to bottom.
    def __init__(self, i: int, j: int, cell_size: int, num_cells_h: int, num_cells_v: int) -> None:
        self.x_id: int = i
        self.y_id: int = j

        self.x_coord: int = i * cell_size
        self.y_coord: int = j * cell_size

        self.cell_size: int = cell_size
        self.num_cells_h: int = num_cells_h
        self.num_cells_v: int = num_cells_v

        self.color: Colors = Colors.WHITE

        self.dist: float = float('inf')
        self.g_score: float = float('inf')
        self.h_score: float = float('inf')

        self.prev = None
        self.visited: bool = False

        self.neighbors = []

    def is_start(self) -> bool:
        return self.color == Colors.START

    def is_end(self) -> bool:
        return self.color == Colors.END

    def is_barrier(self) -> bool:
        return self.color == Colors.BLACK

    def make_start(self) -> None:
        self.color = Colors.START
        self.dist = 0
        self.g_score = 0
        self.h_score = 0

    def make_end(self) -> None:
        self.color = Colors.END

    def make_barrier(self) -> None:
        if not self.is_start() and not self.is_end():
            self.color = Colors.BLACK

    def make_frontier(self) -> None:
        self.color = Colors.OPEN

    def make_path(self) -> None:
        self.color = Colors.PATH

    def make_examined(self) -> None:
        self.color = Colors.CLOSE

    def reset(self) -> None:
        if not self.is_start() and not self.is_end():
            self.color = Colors.WHITE
        self.dist = float('inf')
        self.g_score = float('inf')
        self.h_score = float('inf')
        self.prev = None
        self.visited = False

    def draw(self, screen: Surface) -> None:
        rect = pygame.Rect(self.x_coord, self.y_coord, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, self.color.value, rect)

    def update_neighbors(self, grid) -> None:
        """Populate accessible neighbors for the current cell."""
        self.neighbors = []

        # UP
        if self.y_id > 0:
            neighbor_up = grid[self.x_id][self.y_id - 1]
            if not neighbor_up.is_barrier():
                self.neighbors.append(neighbor_up)

        # RIGHT
        if self.x_id < self.num_cells_h - 1:
            neighbor_right = grid[self.x_id + 1][self.y_id]
            if not neighbor_right.is_barrier():
                self.neighbors.append(neighbor_right)

        # DOWN
        if self.y_id < self.num_cells_v - 1:
            neighbor_down = grid[self.x_id][self.y_id + 1]
            if not neighbor_down.is_barrier():
                self.neighbors.append(neighbor_down)

        # LEFT
        if self.x_id > 0:
            neighbor_left = grid[self.x_id - 1][self.y_id]
            if not neighbor_left.is_barrier():
                self.neighbors.append(grid[self.x_id - 1][self.y_id])

    def __lt__(self, other):
        return self.dist < other.dist
