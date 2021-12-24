from __future__ import annotations

import math
from decimal import Decimal
from typing import Type, TypeVar

from pyrl.constants import dir
from pyrl.constants.coord import Coord

N = TypeVar('N', int, float, Decimal)
def resize_range(number: N, old_range: range, new_range: range = range(2)) -> N:
    n_t: Type[N] = type(number)
    assert number in old_range, f"Value '{number}' is not inside {old_range}"
    assert len(old_range) > 1, f"Number {old_range.start} is not a range"
    old_min, old_max = n_t(old_range.start), n_t(old_range.stop - 1)
    new_min, new_max = n_t(new_range.start), n_t(new_range.stop - 1)
    return (((n_t(number) - n_t(old_min)) * (n_t(new_max) - n_t(new_min)))
            / (n_t(old_max) - n_t(old_min))) + n_t(new_min)

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
    y_range = range(ay, by + includelast) if ay < by else range(by, ay + includelast)[::-1]
    for y in y_range:
        yield (x, y) if steep else (y, x)
        error -= deltax
        if error < 0:
            x += xstep
            error += deltay

def chebyshev(coord_a, coord_b):
    ay, ax = coord_a
    by, bx = coord_b
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
    gcd = abs(math.gcd(a, b))
    return a // gcd, b // gcd

def resize_vector_to_len(vector, length):
    a, b = vector
    gcd = abs(math.gcd(a, b))
    a, b = a // gcd, b // gcd
    n = int(length / (a ** 2 + b ** 2) ** 0.5)
    return n * a, n * b

def get_vector(origin, target):
    return target[0] - origin[0], target[1] - origin[1]

def add_vector(vector_a: Coord, vector_b: Coord) -> Coord:
    return vector_a[0] + vector_b[0], vector_a[1] + vector_b[1]

def scalar_mult(scalar, vector):
    return scalar * vector[0], scalar * vector[1]

def reverse_vector(vector):
    return -vector[0], -vector[1]

def clockwise(vector):
    return vector[1], -vector[0]

def anticlockwise(vector):
    return -vector[1], vector[0]

def anticlockwise_45(direction):
    return dir.counter_clockwise(direction)

def clockwise_45(direction):
    return dir.clockwise(direction)
