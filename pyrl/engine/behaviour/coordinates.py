from __future__ import annotations

import math
from decimal import Decimal
from typing import Iterable, TypeGuard

from pyrl.engine.enums.directions import Direction, Dir, Coord, DirectionUnit

def resize_range[N: (int, float, Decimal)](number: N, old_range: range, new_range: range = range(2)) -> N:
    """Resize given number from the old_range to the new_range.

    If the input number is a float or decimal then the return value will also be and might include fractions
    For example resize_range(1.0, range(3)) == 0.5 because 1 is in the middle of range(3)"""
    t = type(number)
    assert number in old_range, f"Value '{number}' is not inside {old_range}"
    assert len(old_range) > 1, f"Number {old_range.start} is not a range"
    old_min, old_max = t(old_range.start), t(old_range.stop - 1)
    new_min, new_max = t(new_range.start), t(new_range.stop - 1)
    return t((((t(number) - t(old_min)) * (t(new_max) - t(new_min))) / (t(old_max) - t(old_min))) + t(new_min))

def bresenham(coord_a: Coord, coord_b: Coord) -> Iterable[Coord]:
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

def bresenham_old(coord_a: Coord, coord_b: Coord, include_last: bool = True) -> Iterable[Coord]:
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
    y_range = range(ay, by + include_last) if ay < by else range(by, ay + include_last)[::-1]
    for y in y_range:
        yield (x, y) if steep else (y, x)
        error -= deltax
        if error < 0:
            x += xstep
            error += deltay

def chebyshev_distance(coord_a: Coord, coord_b: Coord) -> Coord:
    ay, ax = coord_a
    by, bx = coord_b
    diagonal_steps = min(abs(ay - by), abs(ax - bx))
    orthogonal_steps = abs(ay - by) + abs(ax - bx) - 2 * diagonal_steps
    return orthogonal_steps, diagonal_steps

def cross_product(line_start_coord: Coord, wild_coord: Coord, line_finish_coord: Coord) -> int:
    start_y, start_x = line_start_coord
    wild_y, wild_x = wild_coord
    finish_y, finish_x = line_finish_coord
    return abs((start_x - wild_x) * (finish_y - wild_y) - (finish_x - wild_x) * (start_y - wild_y))

def minimize_vector(vector: Coord) -> Coord:
    a, b = vector
    gcd = abs(math.gcd(a, b))
    return a // gcd, b // gcd

def resize_vector_to_len(vector: Coord, length: int) -> Coord:
    a, b = vector
    gcd = abs(math.gcd(a, b))
    a, b = a // gcd, b // gcd
    n = int(length / (a ** 2 + b ** 2) ** 0.5)
    return n * a, n * b

def get_vector(origin: Coord, target: Coord) -> Coord:
    return target[0] - origin[0], target[1] - origin[1]

def vector_is_direction(vector: Coord) -> TypeGuard[Direction]:
    return vector in Dir.AllPlusStay

def vector_within_distance(origin: Coord, target: Coord, distance: int) -> bool:
    cy, cx = origin
    ty, tx = target
    return (cy - ty) ** 2 + (cx - tx) ** 2 <= distance ** 2

def add_vector(vector_a: Coord, vector_b: Coord) -> Coord:
    return vector_a[0] + vector_b[0], vector_a[1] + vector_b[1]

def scalar_mult(scalar: int, vector: Coord) -> Coord:
    return scalar * vector[0], scalar * vector[1]

def reverse[I: (int, DirectionUnit)](vector: tuple[I, I]) -> tuple[I, I]:
    return -vector[0], -vector[1]

def clockwise_90[I: (int, DirectionUnit)](vector: tuple[I, I]) -> tuple[I, I]:
    return vector[1], -vector[0]

def anticlockwise_90[I: (int, DirectionUnit)](vector: tuple[I, I]) -> tuple[I, I]:
    return -vector[1], vector[0]

def clockwise_45(direction: Direction) -> Direction:
    return Dir.clockwise(direction)

def anticlockwise_45(direction: Direction) -> Direction:
    return Dir.counter_clockwise(direction)
