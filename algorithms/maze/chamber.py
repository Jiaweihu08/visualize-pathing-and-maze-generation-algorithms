from __future__ import annotations
from collections.abc import Callable
from collections import namedtuple
from random import choice, randint

from .square_cell import SquareCell


Door = namedtuple("Door", ["row_id", "col_id", "is_open"])
Wall = namedtuple("Wall", ["from_", "to_", "door"])


class Chamber:
    """
    This maze generation algorithm consists of recursively dividing a given chamber into four sub-chambers:
    1. Randomly select (centre_row_id, center_col_id) within the Chamber boundaries.
    2. Create a vertical and a horizontal line that intersect on (centre_row_id, center_col_id),
    dividing the chamber in four.
    3. On three out of four dividing lines for the Chamber, open a door to as to connect the sub-chambers.
    4. Repeat the process for each of the sub-chambers.
    """

    def __init__(
        self,
        row_id_min: int,
        row_id_max: int,
        col_id_min: int,
        col_id_max: int,
        row_ids_to_avoid: list[int],
        col_idx_to_avoid: list[int],
    ) -> None:
        # Set up chamber boundaries
        self.row_id_min: int = row_id_min
        self.row_id_max: int = row_id_max
        self.col_id_min: int = col_id_min
        self.col_id_max: int = col_id_max

        # Walls should not be placed on these positions
        self.row_ids_to_avoid: list[int] = row_ids_to_avoid
        self.col_ids_to_avoid: list[int] = col_idx_to_avoid
        self.is_divisible, self.center_row_id, self.center_col_id = self._select_center_ids()

    def _select_center_ids(self) -> (bool, int, int):
        row_ids_to_avoid_set = set(self.row_ids_to_avoid)
        col_ids_to_avoid_set = set(self.col_ids_to_avoid)
        row_candidate_ids = [
            row_id
            for row_id in range(self.row_id_min + 1, self.row_id_max)
            if row_id not in row_ids_to_avoid_set
        ]
        col_candidate_ids = [
            col_id
            for col_id in range(self.col_id_min + 1, self.col_id_max)
            if col_id not in col_ids_to_avoid_set
        ]
        if row_candidate_ids and col_candidate_ids:
            return True, choice(row_candidate_ids), choice(col_candidate_ids)
        else:
            return False, -1, -1

    def divide(
        self, cells: list[list[SquareCell]], draw: Callable[[], None]
    ) -> list["Chamber"]:
        if self.is_divisible:
            self._build_dividing_walls(cells, draw)
            walls = self._open_doors(cells, draw)
            sub_chambers = self._build_sub_chambers(walls)
            return sub_chambers
        else:
            return []

    def _build_dividing_walls(
        self, cells: list[list[SquareCell]], draw: Callable[[], None]
    ) -> None:
        # build horizontal wall
        for cell in cells[self.center_row_id][self.col_id_min:self.col_id_max + 1]:
            cell.make_barrier()
            draw()
        # build vertical wall
        for row in cells[self.row_id_min:self.row_id_max + 1]:
            cell = row[self.center_col_id]
            cell.make_barrier()
            draw()

    def _open_doors(
        self, cells: list[list[SquareCell]], draw: Callable[[], None]
    ) -> dict[str, Wall]:
        # Illustration for Chamber c, and its sub-chambers c1, c2, c3, and c4:
        # c:
        # -----------------------  v_upper_wall -> c1 | c2
        # |     c1   |    c2    |  v_lower_wall -> c3 | c4
        # |----------.----------|  h_left_wall -> c1 | c3
        # |     c3   |    c4    |  h_right_wall -> c2 | c4
        # -----------------------

        def get_wall(
            wall_from: int, wall_to: int, door_row_id: int, door_col_id: int, is_open: bool
        ) -> Wall:
            door = Door(door_row_id, door_col_id, is_open)
            wall = Wall(wall_from, wall_to, door)
            if is_open:  # Reset this cell on the wall as door
                cells[door_row_id][door_col_id].reset()
                draw()
            return wall

        # Randomly select a wall to keep it closed
        closed_wall = choice(
            ["v_upper_wall", "v_lower_wall", "h_left_wall", "h_right_wall"]
        )
        walls = {
            "v_upper_wall": get_wall(
                self.col_id_min,
                self.center_col_id - 1,
                self.center_row_id,
                randint(self.col_id_min, self.center_col_id - 1),
                "v_upper_wall" != closed_wall,
            ),
            "v_lower_wall": get_wall(
                self.center_col_id + 1,
                self.col_id_max - 1,
                self.center_row_id,
                randint(self.center_col_id + 1, self.col_id_max),
                "v_lower_wall" != closed_wall,
            ),
            "h_left_wall": get_wall(
                self.row_id_min,
                self.center_row_id - 1,
                randint(self.row_id_min, self.center_row_id - 1),
                self.center_col_id,
                "h_left_wall" != closed_wall,
            ),
            "h_right_wall": get_wall(
                self.center_row_id + 1,
                self.row_id_max,
                randint(self.center_row_id + 1, self.row_id_max),
                self.center_col_id,
                "h_right_wall" != closed_wall,
            ),
        }
        return walls

    def _build_sub_chambers(self, walls: dict[str, Wall]) -> list["Chamber"]:
        sub_chambers = []
        for v_w in ["v_upper_wall", "v_lower_wall"]:
            for h_w in ["h_left_wall", "h_right_wall"]:
                h_wall = walls[h_w]
                row_id_min, row_id_max = h_wall.from_, h_wall.to_

                v_wall = walls[v_w]
                col_id_min, col_id_max = v_wall.from_, v_wall.to_

                row_ids_to_avoid = []
                col_ids_to_avoid = []

                if (row_id_max - row_id_min >= 3) and (col_id_max - col_id_min >= 3):
                    for row_id in self.row_ids_to_avoid:
                        if row_id_min <= row_id <= row_id_max:
                            row_ids_to_avoid.append(row_id)

                    for col_id in self.col_ids_to_avoid:
                        if col_id_min <= col_id <= col_id_max:
                            col_ids_to_avoid.append(col_id)

                    if h_wall.door.is_open:
                        row_ids_to_avoid.append(h_wall.door.row_id)

                    if v_wall.door.is_open:
                        col_ids_to_avoid.append(v_wall.door.col_id)

                    sub_chamber = Chamber(
                        row_id_min, row_id_max, col_id_min, col_id_max, row_ids_to_avoid, col_ids_to_avoid
                    )
                    sub_chambers.append(sub_chamber)
        return sub_chambers
