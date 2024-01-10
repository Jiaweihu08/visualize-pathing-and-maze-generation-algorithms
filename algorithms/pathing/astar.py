from queue import PriorityQueue
from collections.abc import Callable

from ..utils import set_caption, should_quit
from ..maze import SquareCell


def astar(start: SquareCell, end: SquareCell, draw: Callable[[None], None]) -> bool:
    """A* Algorith"""
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
            while curr.prev != start:
                curr = curr.prev
                curr.make_path()
                draw(None)
            set_caption(astar.__doc__ + "- Path Found!")
            return True

        for neigh in curr.neighbors:
            new_g_score = curr.g_score + 1
            if neigh.g_score > new_g_score:
                neigh.g_score = new_g_score
                neigh.h_score = compute_h_score(neigh, end)
                neigh.dist = neigh.g_score + neigh.h_score
                neigh.prev = curr

                if neigh not in q_set:
                    if neigh != end:
                        neigh.make_frontier()

                    count += 1
                    q.put((neigh.dist, count, neigh))
                    q_set.add(neigh)

        if curr != start:
            curr.make_examined()

        draw(None)
    set_caption(astar.__doc__ + "- No Path Found!")
    return False


def compute_h_score(cell: SquareCell, end: SquareCell) -> int:
    return abs(cell.row_id - end.row_id) + abs(cell.col_id - end.col_id)
