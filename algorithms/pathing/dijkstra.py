from collections.abc import Callable

from algorithms.utils import set_caption, should_quit
from algorithms.maze import SquareCell


def dijkstra(start: SquareCell, end: SquareCell, draw: Callable[[None], None]):
    """Dijkstra Algorithm"""
    set_caption(dijkstra.__doc__)

    q = set()
    q.add(start)

    while q:
        should_quit()

        curr = min(q)
        q.remove(curr)

        if curr == end:
            while curr.prev != start:
                curr = curr.prev
                curr.make_path()
                draw(None)
            set_caption(dijkstra.__doc__ + "- Path Found!")
            return True

        for neighbor in curr.neighbors:
            new_dist = curr.dist + 1
            if neighbor.dist > new_dist:
                neighbor.dist = new_dist
                neighbor.prev = curr

                if neighbor != end:
                    neighbor.make_frontier()

                q.add(neighbor)

        if curr != start:
            curr.make_examined()

        draw(None)
    set_caption(dijkstra.__doc__ + "- No Path Found.")
    return False
