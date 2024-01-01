from __future__ import annotations

from time import sleep

import pygame
from pygame import Surface

from algorithms.maze import SquareCell
from algorithms import (
    PathingAlgorithm,
    BarrierSpecs,
    get_pathing_algorithm,
    get_barrier,
)


class Grid:
    """2D SquareCell matrix:
    e.g. Grid cells with num_rows=4, num_columns=3:
    [
        [_, _, _], # row0
        [_, _, _], # row1
        [_, x, _], # row2
        [_, _, _]  # row3
    ]
    x here can be accessed through cells[2][1]
    """

    def __init__(
        self,
        cells: list[list[SquareCell]],
        pathing: PathingAlgorithm,
        barrier_spec: BarrierSpecs,
        num_rows: int,
        num_columns: int,
        cell_size: int,
    ) -> None:
        self.cells: list[list[SquareCell]] = cells
        self.pathing: PathingAlgorithm = pathing
        self.barrier_spec: BarrierSpecs = barrier_spec
        self.num_rows: int = num_rows
        self.num_columns: int = num_columns
        self.cell_size: int = cell_size

        self.start: SquareCell | None = None
        self.end: SquareCell | None = None

    @classmethod
    def create(
        cls,
        pathing_name: str,
        barrier_name: str,
        num_rows: int,
        num_columns: int,
        cell_size: int,
    ) -> "Grid":
        pathing = get_pathing_algorithm(pathing_name)
        barrier_specs = get_barrier(barrier_name)
        cells = _get_cells(barrier_specs.cell_type, num_rows, num_columns, cell_size)
        return cls(cells, pathing, barrier_specs, num_rows, num_columns, cell_size)

    def process_click(self, pos: (int, int)) -> None:
        r, c = self._get_clicked_cell_id(pos)
        cell = self.cells[r][c]
        if not self.start and cell != self.end:
            # Set starting point
            cell.make_start()
            self.start = cell
        elif not self.end and cell != self.start:
            # Set end point
            cell.make_end()
            self.end = cell
        elif cell != self.start and cell != self.end:
            # Create barrier
            cell.make_barrier()

    def _get_clicked_cell_id(self, pos: (int, int)) -> (int, int):
        x, y = pos
        col_id = x // self.cell_size
        row_id = y // self.cell_size
        return row_id, col_id

    def draw(self, screen: Surface, duration: int = 0):
        for row in self.cells:
            for cell in row:
                cell.draw(screen)

        pygame.display.update()
        if duration > 0:
            sleep(duration)

    def generate_barriers(self, screen: Surface) -> None:
        self.barrier_spec.barrier_generation(self.cells, lambda: self.draw(screen))

    def find_path(self, screen: Surface) -> None:
        self.pathing(self.start, self.end, lambda _: self.draw(screen))

    def reset(self) -> None:
        self.start = None
        self.end = None
        for row in self.cells:
            for cell in row:
                cell.reset()

    def is_ready(self) -> bool:
        return self.start is not None and self.end is not None


def _get_cells(
    cell_cls: SquareCell.__class__, num_rows: int, num_columns: int, cell_size: int
) -> list[list[SquareCell]]:
    cells = []
    for r in range(num_rows):
        row = []
        for c in range(num_columns):
            cell = cell_cls(r, c, cell_size, num_rows, num_columns)
            row.append(cell)
        cells.append(row)
    return cells


if __name__ == "__main__":
    num_rows_ = 3
    num_cols_ = 5
    grid = Grid.create("a*", "diy", num_rows_, num_cols_, 2)
    assert len(grid.cells) == num_rows_
    assert len(grid.cells[0]) == num_cols_
