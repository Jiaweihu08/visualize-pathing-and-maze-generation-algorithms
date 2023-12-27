from collections.abc import Callable
from collections import namedtuple
from random import choice, randint
from typing import Self

from algorithms.maze import SquareCell


Door = namedtuple("Door", ['x', 'y', 'is_open'])
Wall = namedtuple("Wall", ['from_', 'to_', 'door'])


class Chamber:
    """
    This maze generation algorithm relies on recursively dividing the chamber into four sub-chambers:
    1. Randomly select (centre_x, center_y) within the Chamber boundaries.
    2. Create a vertical and a vertical lines that intersect on (center_x, center_y), to divide the Chamber in four.
    3. On three out of four dividing lines for the Chamber, open a door to as to connect the sub-chambers.
    4. Repeat the process for each of the sub-chambers.
    """
    def __init__(self, x_min: int, x_max: int, y_min: int, y_max: int, x_to_avoid: list[int], y_to_avoid: list[int]):
        # Set up chamber boundaries
        self.x_min: int = x_min
        self.x_max: int = x_max
        self.y_min: int = y_min
        self.y_max: int = y_max

        # Walls should not be placed on these positions
        self.x_to_avoid: list[int] = x_to_avoid
        self.y_to_avoid: list[int] = y_to_avoid

        x_to_avoid = set(self.x_to_avoid)
        y_to_avoid = set(self.y_to_avoid)
        x_candidates = [x for x in range(self.x_min + 1, self.x_max) if x not in x_to_avoid]
        y_candidates = [y for y in range(self.y_min + 1, self.y_max) if y not in y_to_avoid]
        if x_candidates and y_candidates:
            self.is_qualified = True
            self.center_x = choice(x_candidates)
            self.center_y = choice(y_candidates)
        else:
            self.is_qualified = False
            self.center_x = -1
            self.center_y = -1

    def divide(self, cells: list[list[SquareCell]], draw: Callable[None, None]) -> list[Self]:
        if self.is_qualified:
            self._build_dividing_walls(cells, draw)
            walls = self._open_doors(cells, draw)
            sub_chambers = self._build_sub_chambers(walls)
            return sub_chambers
        else:
            return []

    def _build_dividing_walls(self, cells: list[list[SquareCell]], draw: Callable[None, None]) -> None:
        for cell in cells[self.center_x][self.y_min:self.y_max + 1]:
            cell.make_barrier()
            draw()
        for col in cells[self.x_min:self.x_max + 1]:
            cell = col[self.center_y]
            cell.make_barrier()
            draw()

    def _open_doors(self, cells: list[list[SquareCell]], draw: Callable[None, None]) -> dict[str, Wall]:
        # Illustration for Chamber and sub-chambers c1, c2, c3, and c4.
        # -----------------------  v_upper_wall -> c1 | c2
        # |     c1   |    c2    |  v_lower_wall -> c3 | c4
        # |---------------------|  h_left_wall -> c1 | c3
        # |     c3   |    c4    |  h_right_wall -> c2 | c4
        # -----------------------

        def get_walls_and_doors(wall_from: int, wall_to: int, door_x: int, door_y: int, is_open: bool) -> Wall:
            door = Door(door_x, door_y, is_open)
            wall = Wall(wall_from, wall_to, door)
            if is_open:  # Reset this cell on the wall as door
                cells[door.x][door.y].reset()
                draw()
            return wall

        # Randomly select a wall to keep it closed
        closed_wall = choice(['v_upper_wall', 'v_lower_wall', 'h_left_wall', 'h_right_wall'])
        walls_and_doors = {
            'v_upper_wall': get_walls_and_doors(
                self.y_min, self.center_y - 1,
                self.center_x, randint(self.y_min, self.center_y - 1), 'v_upper_wall' == closed_wall),
            'v_lower_wall': get_walls_and_doors(
                self.center_y + 1, self.y_max,
                self.center_x, randint(self.center_y + 1, self.y_max), 'v_lower_wall' == closed_wall),
            'h_left_wall': get_walls_and_doors(
                self.x_min, self.center_x - 1,
                randint(self.x_min, self.center_x - 1), self.center_y, 'h_left_wall' == closed_wall),
            'h_right_wall': get_walls_and_doors(
                self.center_x + 1, self.x_max,
                randint(self.center_x + 1, self.x_max), self.center_y, 'h_right_wall' == closed_wall)
        }
        return walls_and_doors

    def _build_sub_chambers(self, walls_and_doors: dict[str, Wall]) -> list[Self]:
        sub_chambers = []
        for v_w in ['v_upper_wall', 'v_lower_wall']:
            for h_w in ['h_left_wall', 'h_right_wall']:
                h_wall = walls_and_doors[h_w]
                x_min, x_max = h_wall.from_, h_wall.to_

                v_wall = walls_and_doors[v_w]
                y_min, y_max = v_wall.from_, v_wall.to_

                x_to_avoid = [h_wall.door.x]
                y_to_avoid = [v_wall.door.y]

                if (x_max - x_min >= 3) and (y_max - y_min >= 3):
                    for x in self.x_to_avoid:
                        if x is not None and (x_min <= x <= x_max):
                            x_to_avoid.append(x)
                    for y in self.y_to_avoid:
                        if y is not None and (y_min <= y <= y_max):
                            y_to_avoid.append(y)

                    sub_chamber = Chamber(x_min, x_max, y_min, y_max, x_to_avoid, y_to_avoid)
                    sub_chambers.append(sub_chamber)
        return sub_chambers
