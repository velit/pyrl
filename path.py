import debug
import const.colors as COLOR

from main import io
from heapq import heappush, heappop
from generic_algorithms import chebyshev


def path(start_coord, goal_coord, neighbor_function, heuristic):
    return _iterate_path(_a_star(start_coord, goal_coord, neighbor_function, heuristic), start_coord, goal_coord)


def heuristic(coordA, coordB, default_movement_cost, diagonal_modifier):
    orthogonal_steps, diagonal_steps = chebyshev(coordA, coordB)
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
            if debug.path and origin != start:
                io.draw_char(origin, ('+', COLOR.LIGHT_BLUE))
            openmember.remove(origin)
            closedset.add(origin)

            for node, cost in neighbors(origin):
                if node not in closedset and (node not in openmember or g[origin] + cost < g[node]):
                    came_from[node] = origin
                    g[node] = g[origin] + cost
                    heappush(openprio, (g[node] + heuristic(node, goal, start), node))
                    if debug.path and node != goal:
                        io.draw_char(node, ('?', COLOR.YELLOW))
                    openmember.add(node)
            if debug.path_step:
                io.get_key()
    else:
        raise Exception("No possible paths between arguments start:{} goal:{}".format(start, goal))


def _iterate_path(came_from, start, goal):
    """Iterates the path structure returned by _path()."""
    cur = start
    while cur != goal:
        cur = came_from[cur]
        yield cur
