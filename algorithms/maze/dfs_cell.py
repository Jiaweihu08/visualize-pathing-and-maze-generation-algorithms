import pygame
from pygame import Surface

from .square_cell import SquareCell
from ..utils import Colors


class DFSMazeCell(SquareCell):
    def __init__(self, r: int, c: int, cell_size: int, num_rows: int, num_columns: int):
        SquareCell.__init__(self, r, c, cell_size, num_rows, num_columns)

        self.color: Colors = Colors.GREY
        self.lines: dict[str, (int, int)] = self._get_lines()

        self.neighbor_cells: list["DFSMazeCell"] = []
        self.reachable_cells: list["DFSMazeCell"] = []

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
        self.reachable_cells = []
        if self.x_id < self.num_rows - 1:
            self.reachable_cells.append(cells[self.x_id + 1][self.y_id])
        if self.x_id > 0:
            self.reachable_cells.append(cells[self.x_id - 1][self.y_id])
        if self.y_id < self.num_columns - 1:
            self.reachable_cells.append(cells[self.x_id][self.y_id + 1])
        if self.y_id > 0:
            self.reachable_cells.append(cells[self.x_id][self.y_id - 1])

    def remove_wall_between(self, other: "DFSMazeCell") -> None:
        """Remove the line between two adjacent cells."""
        if other.x_id == self.x_id or other.y_id == self.y_id:
            if self.y_id - other.y_id == 1:
                #   other
                #   -----
                #   self
                self.lines.pop("top", None)
                other.lines.pop("bottom", None)

            elif other.y_id - self.y_id == 1:
                #   self
                #   -----
                #   other
                self.lines.pop("bottom", None)
                other.lines.pop("top", None)

            elif self.x_id - other.x_id == 1:
                # other | self
                self.lines.pop("left", None)
                other.lines.pop("right", None)

            elif other.y_id - self.y_id == 1:
                # self | other
                self.lines.pop("right", None)
                other.lines.pop("left", None)
        else:
            return

        other.reachable_cells.remove(self)
        other.neighbor_cells.append(self)
        self.neighbor_cells.append(other)

    def enable(self) -> None:
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
