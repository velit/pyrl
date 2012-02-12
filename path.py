import const.debug as DEBUG
import const.colors as COLOR

from heapq import heappush, heappop
from pio import io
from generic_algorithms import chebyshev


def path(start_coord, goal_coord, neighbor_function, heuristic):
	return _iterate_path(_path(start_coord, goal_coord, neighbor_function, heuristic), start_coord, goal_coord)


def heuristic(coordA, coordB, default_movement_cost, diagonal_modifier):
	orthogonal_steps, diagonal_steps = chebyshev(coordA, coordB)
	return default_movement_cost * (orthogonal_steps + diagonal_steps * diagonal_modifier)


def _path(start, goal, neighbors, heuristic):
	if start == goal:
		return goal
	g = {}
	h = {}
	came_from = {}
	closedset = set()
	openprio = [(0, start)]
	openmember = set()
	openmember.add(start)

	g[start] = 0
	h[start] = heuristic(start, goal, start)

	while openprio[0][1] != goal:
		# Best selected node
		s = heappop(openprio)[1]
		if s in closedset:
			continue
		if DEBUG.PATH and s != start:
			io.draw_char(s, ('+', COLOR.LIGHT_BLUE))
		if DEBUG.PATH == 2:
			io.msg(str((g[s] + h[s], g[s], h[s])))
		if DEBUG.PATH == 2:
			io.getch()
		openmember.remove(s)
		closedset.add(s)

		for n, cost in neighbors(s):
			if n in closedset or n in openmember and not g[s] + cost < g[n]:
				continue

			came_from[n] = s
			g[n] = g[s] + cost
			h[n] = heuristic(n, goal, start)
			heappush(openprio, (g[n] + h[n], n))
			if DEBUG.PATH and n != goal:
				io.draw_char(n, ('?', COLOR.RED + COLOR.MAKE_REVERSE))
			openmember.add(n)

	return came_from


def _iterate_path(path, start, goal):
	"""Iterates the path structure returned by _path()."""
	cur = goal
	while cur != start:
		cur = path[cur]
		if cur != start:
			yield cur
