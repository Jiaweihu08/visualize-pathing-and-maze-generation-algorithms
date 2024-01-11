from collections.abc import Callable
from heapq import heappop, heappush

from algorithms.pathing.build_path import build_path
from algorithms.utils import set_caption, should_quit
from algorithms.maze import SquareCell


def dijkstra(start: SquareCell, end: SquareCell, draw: Callable[[], None]):
    """Dijkstra's Algorithm"""
    set_caption(dijkstra.__doc__)

    q = [start]
    while q:
        should_quit()
        curr = heappop(q)

        # Completed, begin rebuilding the path
        if curr == end:
            build_path(curr, start, draw)
            set_caption(dijkstra.__doc__ + "- Path Found!")
            return True

        # Update neighbor dist
        new_dist = curr.dist + 1
        for neighbor in curr.neighbors:
            if neighbor.dist > new_dist:
                neighbor.dist = new_dist
                neighbor.prev = curr
                if neighbor != end:
                    neighbor.make_frontier()
                heappush(q, neighbor)
        if curr != start:
            curr.make_examined()
        draw()
    set_caption(dijkstra.__doc__ + "- No Path Found.")
    return False
