def bresenham(coord_a, coord_b, includelast=True):
	(ay, ax), (by, bx) = coord_a, coord_b
	steep = abs(bx - ax) > abs(by - ay)
	if steep:
		ay, ax = ax, ay
		by, bx = bx, by
	if ay > by:
		ay, by = by, ay
		ax, bx = bx, ax
	deltay = by - ay
	deltax = abs(bx - ax)
	error = deltay / 2
	x = ax
	xstep = 1 if ax < bx else -1
	for y in range(ay, by + includelast):
		yield (x, y) if steep else (y, x)
		error -= deltax
		if error < 0:
			x += xstep
			error += deltay


def chebyshev(coordA, coordB):
	ay, ax = coordA
	by, bx = coordB
	diagonal_steps = min(abs(ay - by), abs(ax - bx))
	orthogonal_steps = abs(ay - by) + abs(ax - bx) - 2 * diagonal_steps
	return orthogonal_steps, diagonal_steps


def cross_product(line_start_coord, wild_coord, line_finish_coord):
	start_y, start_x = line_start_coord
	wild_y, wild_x = wild_coord
	finish_y, finish_x = line_finish_coord
	return abs((start_x - wild_x) * (finish_y - wild_y) - (finish_x - wild_x) * (start_y - wild_y))
