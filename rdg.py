from __future__ import absolute_import, division, print_function, unicode_literals

from random import randrange, random

import const.game as GAME
import templates.tiles as TILE
from generic_algorithms import add_vector
from templates.tiles import WALL as W, ROCK as R, FLOOR as F
from const.directions import NORTH, SOUTH, WEST, EAST


DUNGEON = "GENERATED_LEVEL_TYPE_DUNGEON"
ARENA = "GENERATED_LEVEL_TYPE_ARENA"

RDG_LEVEL_PASSES = 300
CORRIDOR_CHANCE = 0.3


def generate_tilemap_template(level_template, level_type=ARENA):
    return RDG().generate_tilemap_template(level_template, level_type)


def Rectangle(y, x, height, width):
    """
    Return a rectangle which consists of start coords and limit coords.

    Accepts negative height and width: think of them as a vector which in
    combination with y, x define the rectangle.

    y_start and x_start are always calculated to be top left and y_limit and
    x_limit are calculated to be positive.
    """

    if height < 0:
        y_start = y + height + 1
        y_limit = y + 1
    else:
        y_start = y
        y_limit = y + height

    if width < 0:
        x_start = x + width + 1
        x_limit = x + 1
    else:
        x_start = x
        x_limit = x + width

    return _Rectangle((y_start, x_start, y_limit, x_limit))


class _Rectangle(tuple):

    def iterate(self):
        y_start, x_start, y_limit, x_limit = self

        for y in range(y_start, y_limit):
            for x in range(x_start, x_limit):
                yield y, x


class RDG(object):

    def generate_tilemap_template(self, level_template, level_type=ARENA):
        self.level_template = level_template
        self.rows = level_template.rows
        self.cols = level_template.cols

        if level_type == DUNGEON:
            if self.level_template.tilemap_template is None:
                self.init_tilemap_template()
                self.make_initial_room()

            for x in range(RDG_LEVEL_PASSES):
                if random() < CORRIDOR_CHANCE:
                    self.attempt_corridor()
                else:
                    self.attempt_room()

        elif level_type == ARENA:
            self.init_tilemap_template()
            self.make_room(Rectangle(0, 0, self.rows, self.cols))

        if GAME.PASSAGE_UP not in self.level_template.passage_locations:
            self.add_passageway(GAME.PASSAGE_UP, TILE.STAIRS_UP)
        if GAME.PASSAGE_DOWN not in self.level_template.passage_locations:
            self.add_passageway(GAME.PASSAGE_DOWN, TILE.STAIRS_DOWN)

    def init_tilemap_template(self):
        self.level_template.tilemap_template = [R for x in range(self.rows * self.cols)]

    def add_passageway(self, passage, passage_tile_id):
        while True:
            coord = self.get_free_coord()
            neighbors = self.get_up_down_left_right_neighbors(coord)
            tile = self.level_template.get_tile_handle(coord)

            if neighbors == (F, F, F, F) and tile == F:
                break

        self.level_template.set_tile_handle(coord, passage_tile_id)
        self.level_template.passage_locations[passage] = coord

    def make_initial_room(self):
        while True:
            height, width = randrange(5, 11), randrange(7, 14)
            if height * width <= 8 * 8:
                break

        while True:
            # y_scale is the degree of freedom the initial room can spawn in the
            # level. Same thing with x_scale
            y_scale = self.rows - height
            y = randrange((y_scale // 8) * 3, (y_scale // 8) * 5)

            x_scale = self.cols - width
            x = randrange((x_scale // 8) * 3, (x_scale // 8) * 5)
            if self.rectangle_consists_of_tiles(Rectangle(y, x, height, width), (W, R)):
                break

        self.make_room(Rectangle(y, x, height, width))
        self.level_template.set_tile_handle((y + 2, x + 2), TILE.BLACK_FLOOR)

    def attempt_corridor(self):
        (y, x), (y_dir, x_dir) = self.get_wall_coord_and_dir()

        if y_dir:
            length = randrange(5, 14)
        elif x_dir:
            length = randrange(7, 20)
        else:
            assert False

        # Corridors are three tiles wide, thus times three
        corridor_rectangle = Rectangle(y - x_dir, x - y_dir, y_dir * length +
                                       x_dir * 3, x_dir * length + y_dir * 3)

        # Floor part of corridor. length - 1 because floor part ends before corridor end wall
        floor_rectangle = Rectangle(y, x, y_dir * (length - 1) + x_dir, x_dir * (length - 1) + y_dir)

        if self.rectangle_consists_of_tiles(corridor_rectangle, (W, R)):
            self.set_rectangle(corridor_rectangle, W)
            self.set_rectangle(floor_rectangle, F)
            return True
        else:
            return False

    def attempt_room(self):
        (door_y, door_x), (y_dir, x_dir) = self.get_wall_coord_and_dir()
        height = randrange(5, 11)
        width = randrange(7, 14)
        y_mod = randrange(height - 2)
        x_mod = randrange(width - 2)

        if y_dir:
            y = door_y
            x = door_x - 1 - x_mod
            height *= y_dir
        elif x_dir:
            y = door_x - 1 - y_mod
            x = door_x
            width *= x_dir
        else:
            assert False

        rectangle = Rectangle(y, x, height, width)
        if self.rectangle_consists_of_tiles(rectangle, (W, R)):
            self.make_room(rectangle)
            self.level_template.set_tile_handle((door_y, door_x), F)

    def get_free_coord(self):
        while True:
            coord = self.get_random_coord()
            if self.level_template.get_tile_from_coord(coord).is_passable:
                return coord

    def get_random_coord(self):
        return randrange(self.rows), randrange(self.cols)

    def get_wall_coord_and_dir(self):
        """Return a random wall coordinate and build direction."""
        while True:
            coord = self.get_random_coord()
            direction = self.is_edge(coord)
            if direction:
                return coord, direction

    def is_edge(self, coord):
        """Return a valid direction if the coordinate is an edge with a buildable direction."""

        y, x = coord

        # Exclude map border squares
        if y in (0, self.rows - 1) or x in (0, self.cols - 1):
            return False

        neighbors = self.get_up_down_left_right_neighbors(coord)
        dir_map = {(R, F, W, W): NORTH,
                   (F, R, W, W): SOUTH,
                   (W, W, R, F): WEST,
                   (W, W, F, R): EAST}
        try:
            return dir_map[neighbors]
        except KeyError:
            return False

    def get_up_down_left_right_neighbors(self, coord):
        get = self.level_template.get_tile_handle
        neighbors = (get(add_vector(coord, NORTH)),
                     get(add_vector(coord, SOUTH)),
                     get(add_vector(coord, WEST)),
                     get(add_vector(coord, EAST)),)
        return neighbors

    def is_legal(self, coord):
        y, x = coord
        return 0 < y < self.rows and 0 < x < self.cols

    def make_room(self, rectangle):
        y_start, x_start, y_limit, x_limit = rectangle

        for y in range(y_start, y_limit):
            for x in range(x_start, x_limit):
                if y in (y_start, y_limit - 1) or x in (x_start, x_limit - 1):
                    self.level_template.set_tile_handle((y, x), W)
                else:
                    self.level_template.set_tile_handle((y, x), F)

    def rectangle_consists_of_tiles(self, rectangle, tile_seq):

        coords = rectangle.iterate()
        get_tile = self.level_template.get_tile_handle

        return all(self.is_legal(coord) and (get_tile(coord) in tile_seq) for coord in coords)

    def set_rectangle(self, rectangle, tile):
        """Set all the tiles in rectangle to given tile."""

        for coord in rectangle.iterate():
            self.level_template.set_tile_handle(coord, tile)

    def turn_rock_to_wall(self):
        self.level_template.tilemap_template = [W if x == R else x for
                                                x in self.level_template.tilemap_template]
