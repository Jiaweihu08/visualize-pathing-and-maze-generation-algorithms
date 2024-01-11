from collections import deque
from random import randint, shuffle, choice
from typing import Callable

from .square_cell import SquareCell
from .dfs_cell import DFSMazeCell
from .chamber import Chamber
from ..utils import should_quit


def update_all_neighbors(
    cells: list[list[SquareCell]], draw: Callable[[None], None]
) -> None:
    for rows in cells:
        for cell in rows:
            cell.update_neighbors(cells)


def dfs_maze(
    cells: list[list[DFSMazeCell]], draw: Callable[[None], None]
) -> list[list[DFSMazeCell]]:
    for rows in cells:
        for cell in rows:
            cell.update_reachable_cells(cells)

    row_id = randint(0, len(cells) - 1)
    col_id = randint(0, len(cells[0]) - 1)
    root = cells[row_id][col_id]
    root.make_maze_path()

    stack = deque()
    stack.append(root)
    while stack:
        should_quit()
        current_maze_cell = stack.pop()
        next_maze_cell = current_maze_cell.get_next_maze_cell()
        if next_maze_cell is not None:
            current_maze_cell.remove_wall_between(next_maze_cell)
            next_maze_cell.make_maze_path()
            if current_maze_cell.has_maze_cell_candidates():
                stack.append(current_maze_cell)
            stack.append(next_maze_cell)

        draw(None)

    return cells


def recursive_space_division(
    cells: list[list[SquareCell]], draw: Callable[[None], None]
) -> list[list[SquareCell]]:
    num_rows, num_columns = len(cells), len(cells[0])
    root = Chamber(0, num_rows - 1, 0, num_columns - 1, [], [])
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
    """Generate random barriers for each column from left to right."""
    num_rows, num_columns = len(cells), len(cells[0])
    max_num_barriers_per_column = int(num_columns * 0.08)
    # create barriers for each column by randomly selecting rows
    for column_id in range(num_columns):
        num_barriers = randint(
            max_num_barriers_per_column - 3, max_num_barriers_per_column
        )
        row_candidate_ids = list(range(0, num_rows))
        shuffle(row_candidate_ids)
        row_barrier_idx = row_candidate_ids[:num_barriers]
        for row_id in row_barrier_idx:
            cells[row_id][column_id].make_barrier()
            draw(None)
    update_all_neighbors(cells, draw)
    return cells
