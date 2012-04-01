from __future__ import division
import fractions


def bresenham(coord_a, coord_b):
	(ay, ax), (by, bx) = coord_a, coord_b
	dx = abs(bx - ax)
	dy = abs(by - ay)
	sx = 1 if ax < bx else -1
	sy = 1 if ay < by else -1
	err = dx - dy
	while True:
		yield ay, ax
		if ax == bx and ay == by:
			break
		e2 = 2 * err
		if e2 > -dy:
			err = err - dy
			ax = ax + sx
		if e2 < dx:
			err = err + dx
			ay = ay + sy

def bresenham_old(coord_a, coord_b, includelast=True):
	(ay, ax), (by, bx) = coord_a, coord_b
	steep = abs(bx - ax) > abs(by - ay)
	if steep:
		ay, ax = ax, ay
		by, bx = bx, by
	deltay = abs(by - ay)
	deltax = abs(bx - ax)
	error = deltay // 2
	x = ax
	xstep = 1 if ax < bx else -1
	y_range = xrange(ay, by + includelast) if ay < by else range(by, ay + includelast)[::-1]
	for y in y_range:
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

def minimize_vector(vector):
	a, b = vector
	gcd = abs(fractions.gcd(a, b))
	return a // gcd, b // gcd

def get_vector(origin, target):
	return target[0] - origin[0], target[1] - origin[1]

def add_vector(coord, vector):
	return coord[0] + vector[0], coord[1] + vector[1]

def reverse_vector(vector):
	return -vector[0], -vector[1]

def anticlockwise(vector):
	return -vector[1], vector[0]

def clockwise(vector):
	return vector[1], -vector[0]

def anticlockwise_45(vector):
	turn = {
		(1, 0):    (1, 1),
		(1, 1):    (0, 1),
		(0, 1):    (-1, 1),
		(-1, 1):   (-1, 0),
		(-1, 0):   (-1, -1),
		(-1, -1):  (0, -1),
		(0, -1):   (1, -1),
		(1, -1):   (1, 0),
	}
	return turn[vector]

def clockwise_45(vector):
	turn = {
		(1, 0):    (1, -1),
		(1, 1):    (1, 0),
		(0, 1):    (1, 1),
		(-1, 1):   (0, 1),
		(-1, 0):   (-1, 1),
		(-1, -1):  (-1, 0),
		(0, -1):   (-1, -1),
		(1, -1):   (0, -1),
	}
	return turn[vector]

def resize_vector_to_len(vector, length):
	a, b = vector
	gcd = abs(fractions.gcd(a, b))
	a, b = a // gcd, b // gcd
	n = int(length / (a ** 2 + b ** 2) ** 0.5)
	return n*a, n*b
