import fractions

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


def bresenham_y(coordA, coordB):
	(y0, x0), (y1, x1) = coordA, coordB
	dx = abs(x1-x0)
	dy = abs(y1-y0)
	sx = 1 if x0 < x1 else -1
	sy = 1 if y0 < y1 else -1
	err = dx - dy

	while True:
		yield y0, x0
		if x0 == x1 and y0 == y1:
			break
		e2 = 2 * err
		if e2 > -dy:
			err = err - dy
			x0 = x0 + sx
		if e2 < dx:
			err = err + dx
			y0 = y0 + sy


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


def minimize_vector(vector):
	a, b = vector
	gcd = abs(fractions.gcd(a, b))
	return a // gcd, b // gcd


def resize_vector_to_len(vector, length):
	a, b = vector
	gcd = abs(fractions.gcd(a, b))
	a, b = a // gcd, b // gcd
	n = int(length / (a ** 2 + b ** 2) ** 0.5)
	return n*a, n*b
