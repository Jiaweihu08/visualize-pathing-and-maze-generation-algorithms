from typing import Callable

from algorithms import SquareCell


def build_path(curr: SquareCell, start: SquareCell, draw: Callable[[], None]) -> None:
    while curr.prev != start:
        curr = curr.prev
        curr.make_path()
        draw()
