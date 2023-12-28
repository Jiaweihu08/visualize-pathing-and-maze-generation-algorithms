from collections import deque
from random import randint, shuffle
from typing import Callable

from .square_cell import SquareCell
from .dfs_cell import DFSMazeCell
from .chamber import Chamber
from ..utils import should_quit


def update_all_neighbors(
    cells: list[list[SquareCell]], draw: Callable[[None], None]
) -> None:
    for column_cells in cells:
        for cell in column_cells:
            cell.update_neighbors(cells)


def dfs_maze(
    cells: list[list[DFSMazeCell]], draw: Callable[[None], None]
) -> list[list[DFSMazeCell]]:
    for column_cells in cells:
        for cell in column_cells:
            cell.update_reachable_cells(cells)

    root = cells[0][0]
    root.enable()

    stack = deque()
    stack.append(root)

    while stack:
        should_quit()

        curr = stack.pop()
        curr.reachable_cells = [cand for cand in curr.reachable_cells if not cand.visited]

        if curr.reachable_cells:
            stack.append(curr)
            idx = randint(0, len(curr.reachable_cells) - 1)
            candidate = curr.reachable_cells.pop(idx)

            curr.remove_wall_between(candidate)
            candidate.enable()
            stack.append(candidate)

        draw()

    return cells


def recursive_space_division(
    cells: list[list[SquareCell]], draw: Callable[[None], None]
) -> list[list[SquareCell]]:
    num_cells_h, num_cells_v = len(cells), len(cells[0])
    root = Chamber(0, num_cells_h - 1, 0, num_cells_v - 1, [], [])
    stack = deque([root])
    while stack:
        curr_chamber = stack.pop()
        sub_chambers = curr_chamber.divide(cells, draw)
        stack.extend(sub_chambers)
    update_all_neighbors(cells, draw)
    return cells


def random_barriers(
    cells: list[list[SquareCell]], draw: Callable[[None], None]
) -> list[list[SquareCell]]:
    """Generate random barriers"""
    num_cells_v = len(cells)
    num_barriers_per_col = int(num_cells_v * 0.08)
    for column_cells in cells:
        num_barriers = randint(num_barriers_per_col - 3, num_barriers_per_col)
        barrier_idx_candidates = list(range(0, num_cells_v))[:num_barriers]
        shuffle(barrier_idx_candidates)
        for idx in barrier_idx_candidates:
            column_cells[idx].make_barrier()
            draw()
    update_all_neighbors(cells, draw)
    return cells
