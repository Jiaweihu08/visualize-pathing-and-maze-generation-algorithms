from random import randint
from typing import Optional

import pygame
from pygame import Surface

from .square_cell import SquareCell
from ..utils import Colors


class DFSMazeCell(SquareCell):
    def __init__(self, r: int, c: int, cell_size: int, num_rows: int, num_columns: int):
        SquareCell.__init__(self, r, c, cell_size, num_rows, num_columns)

        self.color: Colors = Colors.GREY
        self.lines: dict[str, (int, int)] = self._get_lines()

        self.next_maze_cell_candidates: list["DFSMazeCell"] = []

    def _get_lines(self) -> dict[str, (int, int)]:
        # Relative point positions:
        #   p1 - p2
        #   |    |
        #   p4 - p3
        p1 = (self.x_coord, self.y_coord)
        p2 = (self.x_coord + self.cell_size, self.y_coord)
        p3 = (self.x_coord + self.cell_size, self.y_coord + self.cell_size)
        p4 = (self.x_coord, self.y_coord + self.cell_size)

        lines = {
            "top": (p1, p2),
            "bottom": (p3, p4),
            "left": (p1, p4),
            "right": (p2, p3),
        }
        return lines

    def update_reachable_cells(self, cells: list[list["DFSMazeCell"]]) -> None:
        self.update_neighbors(cells)
        self.next_maze_cell_candidates = self.neighbors
        self.neighbors = []

    def get_next_random_dfs_maze_cell(self) -> Optional["DFSMazeCell"]:
        unvisited_candidates = [c for c in self.next_maze_cell_candidates if not c.visited]
        self.next_maze_cell_candidates = unvisited_candidates
        if len(unvisited_candidates) > 0:
            idx = randint(0, len(unvisited_candidates) - 1)
            return unvisited_candidates[idx]
        else:
            return None

    def remove_wall_between(self, other: "DFSMazeCell") -> None:
        """Remove the line between two adjacent cells."""
        if other.row_id == self.row_id or other.col_id == self.col_id:
            if self.row_id - other.row_id == 1:
                #   other
                #   -----
                #   self
                self.lines.pop("top", None)
                other.lines.pop("bottom", None)

            elif other.row_id - self.row_id == 1:
                #   self
                #   -----
                #   other
                self.lines.pop("bottom", None)
                other.lines.pop("top", None)

            elif self.col_id - other.col_id == 1:
                # other | self
                self.lines.pop("left", None)
                other.lines.pop("right", None)

            elif other.col_id - self.col_id == 1:
                # self | other
                self.lines.pop("right", None)
                other.lines.pop("left", None)
        else:
            return

        # self and other are now reachable during path finding
        if other not in self.neighbors:
            self.neighbors.append(other)
        if self not in other.neighbors:
            other.neighbors.append(self)

        # self and other are now not reachable during maze building
        if other in self.next_maze_cell_candidates:
            self.next_maze_cell_candidates.remove(other)
        if self in other.next_maze_cell_candidates:
            other.next_maze_cell_candidates.remove(self)

    def make_visited_during_maze_generation(self) -> None:
        if not self.is_start() and not self.is_end():
            self.color = Colors.WHITE
        self.visited = True

    # def reset(self) -> None:
    #     if not self.is_start() and not self.is_end():
    #         self.color = Colors.BLACK
    #
    #     self.dist = float("inf")
    #     self.g_score = float("inf")
    #     self.h_score = float("inf")
    #     self.prev = None

    def draw(self, screen: Surface) -> None:
        rect = pygame.Rect(self.x_coord, self.y_coord, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, self.color.value, rect)

        for line in self.lines.values():
            start_pos, end_pos = line
            pygame.draw.line(screen, Colors.BLACK.value, start_pos, end_pos, 3)
