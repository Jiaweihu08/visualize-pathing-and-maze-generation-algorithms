from collections.abc import Callable
from collections import deque

from algorithms.utils import set_caption, should_quit
from algorithms.maze import SquareCell


def dfs(start: SquareCell, end: SquareCell, draw: Callable[None, None]) -> bool:
    """Depth First Search Algorithm"""
    set_caption(dfs.__doc__)

    stack = deque()
    stack.append(start)

    while stack:
        should_quit()

        curr = stack.pop()

        if curr.neighbors:
            stack.append(curr)
            neighbor = curr.neighbors.pop(0)

            if neighbor == end:
                while curr.prev != start:
                    curr = curr.prev
                    curr.make_path()
                    draw()
                set_caption(dfs.__doc__ + '- Path Found!')
                return True

            if not neighbor.visited:
                neighbor.visited = True
                neighbor.prev = curr

                if neighbor != end:
                    neighbor.make_frontier()

                stack.append(neighbor)

        if curr != start:
            curr.make_examined()

        draw()
    set_caption(dfs.__doc__ + '- No Path Found.')
    return False
