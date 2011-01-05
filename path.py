from heapq import heappush, heappop
from pio import io
from constants import DEBUG

def path(start, goal, level):
	"""A* search algorithm. Parameters are squares."""
	return _iterate_path(_path(start, goal, level), start, goal)

def _path(start, goal, level):
	"""A* search algorithm implementation. Parameters are squares."""
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
	h[start] = _h(start, start, goal)

	while openprio[0][1] != goal:
		# Best selected node
		s = heappop(openprio)[1]
		if s in closedset:
			continue
		if DEBUG and s != start: io.drawblock(s)
		if DEBUG == 2: io.msg(str((g[s]+h[s], g[s], h[s])))
		if DEBUG == 2: io.getch()
		openmember.remove(s)
		closedset.add(s)

		for n in level.neighbor_nodes(s.y, s.x):
			if n in closedset or n in openmember \
					and not g[s] + _dist(n, s) < g[n]:
				continue

			came_from[n] = s
			g[n] = g[s] + _dist(n, s)
			h[n] = _h(n, start, goal)
			heappush(openprio, (g[n] + h[n], n))
			if DEBUG and n != goal: io.drawblock(n, "green")
			openmember.add(n)

	return came_from

def _iterate_path(path, start, goal):
	"""Iterates the path structure returned by _path()."""
	cur = goal
	while cur != start:
		cur = path[cur]
		if cur != start:
			yield cur

def _dist(a, b):
	"""Used by path(). Returns the path cost between a and b."""
	y = abs(a.x - b.x)
	x = abs(a.y - b.y)
	diagonal = min(y,x)
	straight = y+x
	return 1415*diagonal + 1000 * (straight - 2*diagonal)

def _h(cur, start, goal):
	"""A* pathing heuristic."""
	#return max(abs(a.y - b.y), abs(a.x - b.x))
	y = abs(cur.y - goal.y)
	x = abs(cur.x - goal.x)
	dx1 = cur.y - goal.y
	dy1 = cur.x - goal.x
	dx2 = start.y - goal.y
	dy2 = start.x - goal.x
	cross = abs(dy1*dx2 - dy2*dx1)
	diagonal = min(y,x)
	straight = y+x
	#io.msg(str(cross/10.0))
	return (1415*diagonal + 1000 * (straight - 2*diagonal)) + cross/10.0
