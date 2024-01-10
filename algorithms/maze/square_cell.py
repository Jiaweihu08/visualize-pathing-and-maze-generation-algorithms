from __future__ import annotations
import pygame
from pygame import Surface

from ..utils import Colors


class SquareCell:
    # Pygame coordinate system has the origin in the top-left corner,
    # with the x-axis growing from left to right, and the y-axis from
    # top to bottom.
    def __init__(
        self, r: int, c: int, cell_size: int, num_rows: int, num_columns: int
    ) -> None:
        self.row_id: int = r
        self.col_id: int = c

        self.x_coord: int = c * cell_size
        self.y_coord: int = r * cell_size

        self.cell_size: int = cell_size
        self.num_rows: int = num_rows
        self.num_columns: int = num_columns

        self.color: Colors = Colors.WHITE

        self.dist: float = float("inf")
        self.g_score: float = float("inf")
        self.h_score: float = float("inf")

        self.prev: SquareCell | None = None
        self.visited: bool = False

        self.neighbors: list[SquareCell] = []

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
        # if not self.is_start() and not self.is_end():
        self.color = Colors.WHITE
        self.dist = float("inf")
        self.g_score = float("inf")
        self.h_score = float("inf")
        self.prev = None
        self.visited = False

    def draw(self, screen: Surface) -> None:
        rect = pygame.Rect(self.x_coord, self.y_coord, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, self.color.value, rect)

    def update_neighbors(self, cells: list[list[SquareCell]]) -> None:
        """Populate accessible neighbors for the current cell."""
        self.neighbors = []

        # Add left neighbor
        if self.col_id > 0:
            neighbor_up = cells[self.row_id][self.col_id - 1]
            if not neighbor_up.is_barrier():
                self.neighbors.append(neighbor_up)

        # Add right neighbor
        if self.col_id < self.num_columns - 1:
            neighbor_down = cells[self.row_id][self.col_id + 1]
            if not neighbor_down.is_barrier():
                self.neighbors.append(neighbor_down)

        # Add up neighbor
        if self.row_id > 0:
            neighbor_left = cells[self.row_id - 1][self.col_id]
            if not neighbor_left.is_barrier():
                self.neighbors.append(cells[self.row_id - 1][self.col_id])

        # Add down neighbor
        if self.row_id < self.num_rows - 1:
            neighbor_right = cells[self.row_id + 1][self.col_id]
            if not neighbor_right.is_barrier():
                self.neighbors.append(neighbor_right)

    def __lt__(self, other) -> bool:
        return self.dist < other.dist

    def __hash__(self) -> int:
        return hash((self.row_id, self.col_id))
