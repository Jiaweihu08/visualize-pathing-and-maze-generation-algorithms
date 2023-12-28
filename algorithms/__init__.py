from collections import namedtuple
from collections.abc import Callable

from .maze import (
    update_all_neighbors,
    recursive_space_division,
    dfs_maze,
    DFSMazeCell,
    random_barriers,
)
from .maze import SquareCell
from .pathing import astar
from .pathing import dfs
from .pathing import dijkstra

PathingAlgorithm = Callable[[SquareCell, SquareCell, Callable[[None], None]], bool]
pathing_algorithms: dict[str, PathingAlgorithm] = {
    "a*": astar,
    "dijkstra": dijkstra,
    "dfs": dfs,
}

BarrierSpecs = namedtuple(
    "BarrierSpecs", ("cell_type", "barrier_generation", "duration")
)
barriers: dict[str, BarrierSpecs] = {
    "diy": BarrierSpecs(SquareCell, update_all_neighbors, 0),
    "recursive_division_maze": BarrierSpecs(SquareCell, recursive_space_division, 0),
    "dfs": BarrierSpecs(DFSMazeCell, dfs_maze, 0),
    "random": BarrierSpecs(SquareCell, random_barriers, 0),
}


def get_pathing_algorithm(name: str) -> PathingAlgorithm:
    _name = name.lower().rstrip()
    if _name in pathing_algorithms:
        return pathing_algorithms[_name]
    else:
        raise ValueError(f"Pathing algorithm {name} not found!")


def get_barrier(name: str) -> BarrierSpecs:
    _name = name.lower()
    if _name in barriers:
        return barriers[_name]
    else:
        raise ValueError(f"Barrier {name} not found!")
