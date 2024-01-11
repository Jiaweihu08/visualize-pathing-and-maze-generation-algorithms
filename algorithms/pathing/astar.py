from queue import PriorityQueue
from collections.abc import Callable

from .build_path import build_path
from ..utils import set_caption, should_quit
from ..maze import SquareCell


def astar(start: SquareCell, end: SquareCell, draw: Callable[[], None]) -> bool:
    """A* Algorithm"""
    set_caption(astar.__doc__)

    q = PriorityQueue()
    q_set = set()

    count = 0
    q.put((start.dist, count, start))
    q_set.add(start)

    while q_set:
        should_quit()
        curr = q.get()[-1]
        q_set.remove(curr)

        if curr == end:
            build_path(curr, start, draw)
            set_caption(astar.__doc__ + "- Path Found!")
            return True

        new_g_score = curr.g_score + 1
        for neighbor in curr.neighbors:
            if neighbor.g_score > new_g_score:
                neighbor.g_score = new_g_score
                neighbor.h_score = compute_h_score(neighbor, end)
                neighbor.dist = neighbor.g_score + neighbor.h_score
                neighbor.prev = curr

                if neighbor not in q_set:
                    if neighbor != end:
                        neighbor.make_frontier()

                    count += 1
                    q.put((neighbor.dist, count, neighbor))
                    q_set.add(neighbor)

        if curr != start:
            curr.make_examined()

        draw()
    set_caption(astar.__doc__ + "- No Path Found!")
    return False


def compute_h_score(cell: SquareCell, end: SquareCell) -> int:
    return abs(cell.row_id - end.row_id) + abs(cell.col_id - end.col_id)
