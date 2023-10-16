from __future__ import annotations

from collections.abc import Iterable, Callable
from heapq import heappush, heappop

from pyrl.engine.behaviour.coordinates import chebyshev_distance
from pyrl.engine.enums.directions import Coord

NeighborCall = Callable[[Coord], Iterable[tuple[Coord, int]]]
HeuristicCall = Callable[[Coord, Coord, Coord], float]

def path(start: Coord, goal: Coord, neighbours: NeighborCall, heuristic: HeuristicCall) -> Iterable[Coord]:
    return _iterate_path(_a_star(start, goal, neighbours, heuristic), start, goal)

def distance(coord_a: Coord, coord_b: Coord, default_movement_cost: int, diagonal_modifier: float) -> float:
    orthogonal_steps, diagonal_steps = chebyshev_distance(coord_a, coord_b)
    return default_movement_cost * (orthogonal_steps + diagonal_steps * diagonal_modifier)

def _a_star(start: Coord, goal: Coord, neighbors: NeighborCall, heuristic: HeuristicCall) -> dict[Coord, Coord]:
    start, goal = goal, start
    came_from: dict[Coord, Coord] = {}
    closedset = set()
    openmember = set()
    openmember.add(start)

    cheap = {start: 0}  # Current cheapest cost to coord
    openprio: list[tuple[float, Coord]] = []
    heappush(openprio, (0, start))

    while openprio:
        if openprio[0][1] == goal:
            return came_from
        origin = heappop(openprio)[1]
        if origin not in closedset:
            openmember.remove(origin)
            closedset.add(origin)

            for node, cost in neighbors(origin):
                if node not in closedset and (node not in openmember or cheap[origin] + cost < cheap[node]):
                    came_from[node] = origin
                    cheap[node] = cheap[origin] + cost
                    estimate = cheap[node] + heuristic(node, goal, start)
                    heappush(openprio, (estimate, node))
                    openmember.add(node)
    else:
        raise ValueError(f"No possible paths between {start=} and {goal=}")

def _iterate_path(came_from: dict[Coord, Coord], start: Coord, goal: Coord) -> Iterable[Coord]:
    """Iterate the path structure returned by _path()."""
    cur = start
    while cur != goal:
        cur = came_from[cur]
        yield cur
