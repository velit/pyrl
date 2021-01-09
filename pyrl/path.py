from heapq import heappush, heappop

from pyrl.generic_algorithms import chebyshev

class PathException(Exception):
    pass

def path(start_coord, goal_coord, neighbor_function, heuristic):
    return _iterate_path(_a_star(start_coord, goal_coord, neighbor_function, heuristic), start_coord, goal_coord)

def distance(coord_a, coord_b, default_movement_cost, diagonal_modifier):
    orthogonal_steps, diagonal_steps = chebyshev(coord_a, coord_b)
    return default_movement_cost * (orthogonal_steps + diagonal_steps * diagonal_modifier)

def _a_star(start, goal, neighbors, heuristic):
    start, goal = goal, start
    came_from = {}
    closedset = set()
    openmember = set()
    openmember.add(start)

    g = {start: 0}
    openprio = []
    heappush(openprio, (0, start))

    while openprio:
        if openprio[0][1] == goal:
            return came_from
        origin = heappop(openprio)[1]
        if origin not in closedset:
            openmember.remove(origin)
            closedset.add(origin)

            for node, cost in neighbors(origin):
                if node not in closedset and (node not in openmember or g[origin] + cost < g[node]):
                    came_from[node] = origin
                    g[node] = g[origin] + cost
                    heappush(openprio, (g[node] + heuristic(node, goal, start), node))
                    openmember.add(node)
    else:
        raise PathException(f"No possible paths between {start=} and {goal=}")

def _iterate_path(came_from, start, goal):
    """Iterate the path structure returned by _path()."""
    cur = start
    while cur != goal:
        cur = came_from[cur]
        yield cur
