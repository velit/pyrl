from __future__ import absolute_import, division, print_function, unicode_literals

import const.game as GAME
import const.generated_level_types as LEVEL_TYPE
import templates.tiles as TILE

from random import randrange as rr, random as rand
from templates.tiles import WALL as W
from templates.tiles import ROCK as R
from templates.tiles import FLOOR as F


def generate_tilemap_template(level_template, level_type=LEVEL_TYPE.ARENA):
    if level_type == LEVEL_TYPE.DUNGEON:
        if level_template.tilemap_template is None:
            _init_tilemap_template(level_template)
            _make_initial_room(level_template)

        for x in range(GAME.RDG_LEVEL_PASSES):
            if rand() < 0.30:
                _attempt_corridor(level_template)
            else:
                _attempt_room(level_template)

    elif level_type == LEVEL_TYPE.ARENA:
        _init_tilemap_template(level_template)
        _make_room(level_template, 0, 0, level_template.rows, level_template.cols)

    if GAME.PASSAGE_UP not in level_template.passage_locations:
        add_passageway(level_template, GAME.PASSAGE_UP, TILE.STAIRS_UP)
    if GAME.PASSAGE_DOWN not in level_template.passage_locations:
        add_passageway(level_template, GAME.PASSAGE_DOWN, TILE.STAIRS_DOWN)


def get_free_coord(level_template):
    while True:
        y, x = get_random_coord(level_template)
        if level_template.get_tile_from_coord(y, x).is_passable:
            return y, x


def get_random_coord(level_template):
    return rr(level_template.rows), rr(level_template.cols)


def add_passageway(level_template, passage, passage_tile_id):
    while True:
        y, x = get_free_coord(level_template)
        g = level_template.get_tile_handle
        if g(y - 1, x) == F and g(y + 1, x) == F \
                and g(y, x - 1) == F and g(y, x + 1) == F and g(y, x) == F:
            break

    level_template.set_tile_handle(y, x, passage_tile_id)
    level_template.passage_locations[passage] = y, x


def _init_tilemap_template(level_template):
    level_template.tilemap_template = [R for x in range(level_template.rows * level_template.cols)]


def _make_initial_room(level_template):
    while True:
        height, width = rr(5, 11), rr(7, 14)
        if height * width <= 8 * 8:
            break
    while True:
        y_scale = level_template.rows - height - 1 - 1
        x_scale = level_template.cols - width - 1 - 1
        y, x = rr((y_scale // 8) * 3, (y_scale // 8) * 5), rr((x_scale // 8) * 3, (x_scale // 8) * 5)
        if _rect_diggable(level_template, y, x, height, width):
            break

    _make_room(level_template, y, x, height, width)
    level_template.set_tile_handle(y + 2, x + 2, TILE.BLACK_FLOOR)


def _get_wall_coord(level_template):
    while True:
        y, x = get_random_coord(level_template)
        dir = _is_wall(level_template, y, x)
        if dir[0]:
            return y, x, dir[1]


def _is_wall(level_template, y, x):
    g = level_template.get_tile_handle
    if y in (0, level_template.rows - 1) or x in (0, level_template.cols - 1):
        return False, ""
    if g(y - 1, x) == W and g(y + 1, x) == W:
        if g(y, x - 1) == F and g(y, x + 1) == R:
            return True, "right"
        elif g(y, x - 1) == R and g(y, x + 1) == F:
            return True, "left"
    elif g(y, x - 1) == W and g(y, x + 1) == W:
        if g(y - 1, x) == F and g(y + 1, x) == R:
            return True, "down"
        elif g(y - 1, x) == R and g(y + 1, x) == F:
            return True, "up"
    return False, ""


def _rect_diggable(level_template, y0, x0, height, width):
    if y0 < 0 or x0 < 0 or y0 + height >= level_template.rows \
            or x0 + width >= level_template.cols:
        return False
    for y in range(y0, y0 + height):
        for x in range(x0, x0 + width):
            if level_template.get_tile_handle(y, x) != R and \
                    level_template.get_tile_handle(y, x) != W:
                return False
    return True


def _attempt_room(level_template):
    y0, x0, dir = _get_wall_coord(level_template)
    height, width = rr(5, 11), rr(7, 14)
    ypos, xpos = rr(height - 2), rr(width - 2)

    if dir == "left":
        y = y0 - 1 - ypos
        x = x0 - width + 1
    elif dir == "right":
        y = y0 - 1 - ypos
        x = x0
    elif dir == "up":
        y = y0 - height + 1
        x = x0 - 1 - xpos
    elif dir == "down":
        y = y0
        x = x0 - 1 - xpos

    if _rect_diggable(level_template, y, x, height, width):
        _make_room(level_template, y, x, height, width)
        level_template.set_tile_handle(y0, x0, F)


def _make_room(level_template, y0, x0, height, width):
    for y in range(y0, y0 + height):
        for x in range(x0, x0 + width):
            if y in (y0, y0 + height - 1) or x in (x0, x0 + width - 1):
                level_template.set_tile_handle(y, x, W)
            else:
                level_template.set_tile_handle(y, x, F)


def _dig_rect(level_template, y0, x0, tile, height=1, width=1):
    for y in range(y0, y0 + height):
        for x in range(x0, x0 + width):
            level_template.set_tile_handle(y, x, tile)


def _turn_rock_to_wall(level_template):
    level_template.tilemap_template = [W if x == R else x for x in level_template.tilemap_template]


def _attempt_corridor(level_template):
    y, x, dir = _get_wall_coord(level_template)
    len = rr(7, 20)
    if dir == "up" and _rect_diggable(level_template, y - len, x - 1, len, 3) or \
            dir == "down" and _rect_diggable(level_template, y + 1, x - 1, len, 3) or \
            dir == "left" and _rect_diggable(level_template, y - 1, x - len, 3, len) or \
            dir == "right" and _rect_diggable(level_template, y - 1, x + 1, 3, len):
        _make_corridor(level_template, y, x, dir, len)
        return True


def _make_corridor(level_template, y0, x0, dir, len):
    if dir in ("up", "down"):
        fhei = whei = len
        fwid = 1
        wwid = 3
        fx = x0
        wx = x0 - 1
        if dir == "up":
            fy = y0 - len + 1
            wy = fy - 1
        else:
            fy = y0
            wy = fy + 1

    elif dir in ("left", "right"):
        fwid = wwid = len
        fhei = 1
        whei = 3
        fy = y0
        wy = y0 - 1
        if dir == "left":
            fx = x0 - len + 1
            wx = fx - 1
        else:
            fx = x0
            wx = fx + 1

    _dig_rect(level_template, wy, wx, W, whei, wwid)
    _dig_rect(level_template, fy, fx, F, fhei, fwid)
