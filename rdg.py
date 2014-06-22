from __future__ import absolute_import, division, print_function, unicode_literals

from random import randrange, random

import const.game as GAME
import templates.tiles as TILE
from templates.tiles import WALL as W, ROCK as R, FLOOR as F
from const.directions import NORTH, SOUTH, WEST, EAST


DUNGEON = "GENERATED_LEVEL_TYPE_DUNGEON"
ARENA = "GENERATED_LEVEL_TYPE_ARENA"


def generate_tilemap_template(level_template, level_type=ARENA):
    return RDG().generate_tilemap_template(level_template, level_type)


class RDG(object):

    def generate_tilemap_template(self, level_template, level_type=ARENA):
        self.level_template = level_template
        self.rows = level_template.rows
        self.cols = level_template.cols

        if level_type == DUNGEON:
            if self.level_template.tilemap_template is None:
                self.init_tilemap_template()
                self.make_initial_room()

            for x in range(GAME.RDG_LEVEL_PASSES):
                if random() < 0.30:
                    self.attempt_corridor()
                else:
                    self.attempt_room()

        elif level_type == ARENA:
            self.init_tilemap_template()
            self.make_room(0, 0, self.rows, self.cols)

        if GAME.PASSAGE_UP not in self.level_template.passage_locations:
            self.add_passageway(GAME.PASSAGE_UP, TILE.STAIRS_UP)
        if GAME.PASSAGE_DOWN not in self.level_template.passage_locations:
            self.add_passageway(GAME.PASSAGE_DOWN, TILE.STAIRS_DOWN)

    def init_tilemap_template(self):
        self.level_template.tilemap_template = [R for x in range(self.rows * self.cols)]

    def get_free_coord(self):
        while True:
            y, x = self.get_random_coord()
            if self.level_template.get_tile_from_coord(y, x).is_passable:
                return y, x

    def get_random_coord(self):
        return randrange(self.rows), randrange(self.cols)

    def add_passageway(self, passage, passage_tile_id):
        while True:
            y, x = self.get_free_coord()
            g = self.level_template.get_tile_handle
            if g(y - 1, x) == F and g(y + 1, x) == F \
                    and g(y, x - 1) == F and g(y, x + 1) == F and g(y, x) == F:
                break

        self.level_template.set_tile_handle(y, x, passage_tile_id)
        self.level_template.passage_locations[passage] = y, x

    def make_initial_room(self):
        while True:
            height, width = randrange(5, 11), randrange(7, 14)
            if height * width <= 8 * 8:
                break
        while True:
            y_scale = self.rows - height - 1 - 1
            x_scale = self.cols - width - 1 - 1
            y = randrange((y_scale // 8) * 3, (y_scale // 8) * 5)
            x = randrange((x_scale // 8) * 3, (x_scale // 8) * 5)
            if self.rect_diggable(y, x, height, width):
                break

        self.make_room(y, x, height, width)
        self.level_template.set_tile_handle(y + 2, x + 2, TILE.BLACK_FLOOR)

    def get_wall_coord(self):
        while True:
            y, x = self.get_random_coord()
            direction = self.is_edge(y, x)
            if direction is not None:
                return y, x, direction

    def is_edge(self, y, x):
        """ Returns a valid direction if the coordinate is an edge with a
        buildable direction. """

        # Exclude map border squares
        if y in (0, self.rows - 1) or x in (0, self.cols - 1):
            return None

        get = self.level_template.get_tile_handle

        matrix = up, down, left, right = (get(y - 1, x),
                                          get(y + 1, x),
                                          get(y, x - 1),
                                          get(y, x + 1))
        if matrix == (R, F, W, W):
            return NORTH
        elif matrix == (F, R, W, W):
            return SOUTH
        elif matrix == (W, W, R, F):
            return WEST
        elif matrix == (W, W, F, R):
            return EAST

        return None

    def rect_diggable(self, y0, x0, height, width):
        if y0 < 0 or x0 < 0 or y0 + height >= self.rows or x0 + width >= self.cols:
            return False
        for y in range(y0, y0 + height):
            for x in range(x0, x0 + width):
                if self.level_template.get_tile_handle(y, x) != R and \
                        self.level_template.get_tile_handle(y, x) != W:
                    return False
        return True

    def attempt_room(self):
        y0, x0, direction = self.get_wall_coord()
        height = randrange(5, 11)
        width = randrange(7, 14)
        ypos = randrange(height - 2)
        xpos = randrange(width - 2)

        if direction == WEST:
            y = y0 - 1 - ypos
            x = x0 - width + 1
        elif direction == EAST:
            y = y0 - 1 - ypos
            x = x0
        elif direction == NORTH:
            y = y0 - height + 1
            x = x0 - 1 - xpos
        elif direction == SOUTH:
            y = y0
            x = x0 - 1 - xpos
        else:
            assert False

        if self.rect_diggable(y, x, height, width):
            self.make_room(y, x, height, width)
            self.level_template.set_tile_handle(y0, x0, F)

    def make_room(self, y0, x0, height, width):
        for y in range(y0, y0 + height):
            for x in range(x0, x0 + width):
                if y in (y0, y0 + height - 1) or x in (x0, x0 + width - 1):
                    self.level_template.set_tile_handle(y, x, W)
                else:
                    self.level_template.set_tile_handle(y, x, F)

    def dig_rect(self, y0, x0, tile, height=1, width=1):
        for y in range(y0, y0 + height):
            for x in range(x0, x0 + width):
                self.level_template.set_tile_handle(y, x, tile)

    def turn_rock_to_wall(self):
        self.level_template.tilemap_template = [W if x == R else x for
                                                x in self.level_template.tilemap_template]

    def attempt_corridor(self):
        y, x, direction = self.get_wall_coord()
        length = randrange(7, 20)
        if (direction == NORTH and self.rect_diggable(y - length, x - 1, length, 3) or
                direction == SOUTH and self.rect_diggable(y + 1, x - 1, length, 3) or
                direction == WEST and self.rect_diggable(y - 1, x - length, 3, length) or
                direction == EAST and self.rect_diggable(y - 1, x + 1, 3, length)):

            self.make_corridor(y, x, direction, length)
            return True

    def make_corridor(self, y0, x0, direction, length):
        if direction in (NORTH, SOUTH):
            fhei = whei = length
            fwid = 1
            wwid = 3
            fx = x0
            wx = x0 - 1
            if direction == NORTH:
                fy = y0 - length + 1
                wy = fy - 1
            else:
                fy = y0
                wy = fy + 1

        elif direction in (WEST, EAST):
            fwid = wwid = length
            fhei = 1
            whei = 3
            fy = y0
            wy = y0 - 1
            if direction == WEST:
                fx = x0 - length + 1
                wx = fx - 1
            else:
                fx = x0
                wx = fx + 1

        self.dig_rect(wy, wx, W, whei, wwid)
        self.dig_rect(fy, fx, F, fhei, fwid)
