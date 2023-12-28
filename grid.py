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
    def __init__(
        self,
        cells: list[list[SquareCell]],
        pathing: PathingAlgorithm,
        barrier_spec: BarrierSpecs,
        num_cells_h: int,
        num_cells_v: int,
        cell_size: int,
    ) -> None:
        self.cells: list[list[SquareCell]] = cells
        self.pathing: PathingAlgorithm = pathing
        self.barrier_spec: BarrierSpecs = barrier_spec
        self.num_cells_h: int = num_cells_h
        self.num_cells_v: int = num_cells_v
        self.cell_size: int = cell_size

        self.start: SquareCell | None = None
        self.end: SquareCell | None = None

    @classmethod
    def create(
        cls,
        pathing_name: str,
        barrier_name: str,
        num_cells_h: int,
        num_cells_v: int,
        cell_size: int,
    ) -> "Grid":
        pathing = get_pathing_algorithm(pathing_name)
        barrier_specs = get_barrier(barrier_name)
        cells = _get_cells(barrier_specs.cell_type, num_cells_h, num_cells_v, cell_size)
        return cls(cells, pathing, barrier_specs, num_cells_h, num_cells_v, cell_size)

    def process_click(self, pos: (int, int)) -> None:
        i, j = self._get_clicked_cell_id(pos)
        cell = self.cells[i][j]
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
        x_id = x // self.cell_size
        y_id = y // self.cell_size
        return x_id, y_id

    def draw(self, screen: Surface, duration: int = 0):
        for column_cells in self.cells:
            for cell in column_cells:
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
        for column_cells in self.cells:
            for cell in column_cells:
                cell.reset()

    def is_ready(self) -> bool:
        return self.start is not None and self.end is not None


def _get_cells(
    cell_cls: SquareCell.__class__, num_cells_h: int, num_cells_v: int, cell_size: int
) -> list[list[SquareCell]]:
    cells = []
    for i in range(num_cells_h):
        column_cells = []
        for j in range(num_cells_v):
            cell = cell_cls(i, j, cell_size, num_cells_h, num_cells_v)
            column_cells.append(cell)
        cells.append(column_cells)
    return cells


if __name__ == "__main__":
    grid = Grid.create("a*", "diy", 10, 10, 2)
    assert len(grid.cells) == 10
    assert len(grid.cells[0]) == 10
