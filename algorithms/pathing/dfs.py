from collections.abc import Callable
from collections import deque

from algorithms.pathing.build_path import build_path
from algorithms.utils import set_caption, should_quit
from algorithms.maze import SquareCell


def dfs(start: SquareCell, end: SquareCell, draw: Callable[[], None]) -> bool:
    """Depth First Search Algorithm"""
    set_caption(dfs.__doc__)

    stack = deque()
    stack.append(start)
    while stack:
        should_quit()
        curr = stack.pop()

        if curr == end:
            build_path(curr, start, draw)
            set_caption(dfs.__doc__ + "- Path Found!")
            return True

        next_step_candidates = [c for c in curr.neighbors if not c.visited]
        curr.neighbors = next_step_candidates
        if next_step_candidates:
            neighbor = curr.neighbors.pop()
            if curr.neighbors:
                stack.append(curr)
            neighbor.visited = True
            neighbor.prev = curr
            if neighbor != end and neighbor != start:
                neighbor.make_frontier()
            stack.append(neighbor)

        if curr != start:
            curr.make_examined()

        draw()
    set_caption(dfs.__doc__ + "- No Path Found.")
    return False
