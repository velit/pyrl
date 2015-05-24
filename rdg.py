from __future__ import absolute_import, division, print_function, unicode_literals

from functools import partial
from random import randrange, random, choice
from enum import Enum

from enums.level_locations import LevelLocation
from enums.directions import Dir
from generic_algorithms import add_vector
from game_data.tiles import PyrlTile
from generic_structures import List2D


class GenLevelType(Enum):
    Dungeon = "Dungeon"
    Arena = "Arena"

_room_y_range = (5, 11)
_room_x_range = (7, 14)
_corridor_y_range = (5, 14)
_corridor_x_range = (7, 20)
_rdg_level_passes = 300
_corridor_chance_range = (0, 0.3)
_room_chance_range = (0.3, 1)
F = PyrlTile.Floor
W = PyrlTile.Wall
R = PyrlTile.Rock


def generate_tiles(level_template, level_type):
    RDG(level_template, level_type).generate_tiles()


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

    def __init__(self, level_template, level_type=GenLevelType.Arena):
        self.level_template = level_template
        self.rows = level_template.rows
        self.cols = level_template.cols
        self.level_type = level_type

        self.wall_coords = set()
        self.wall_coords_cache = tuple()
        self.is_wall_coords_dirty = True

    def generate_tiles(self):
        if self.level_type == GenLevelType.Dungeon:
            if self.level_template.tiles is None:
                self.init_tiles()
                self.make_initial_room()

            self.generator_loop()

        elif self.level_type == GenLevelType.Arena:
            self.init_tiles()
            self.make_room(Rectangle(0, 0, self.rows, self.cols))

        if LevelLocation.Passage_Up not in self.level_template.passage_locations:
            self.add_passageway(LevelLocation.Passage_Up, PyrlTile.Stairs_Up)
        if LevelLocation.Passage_Down not in self.level_template.passage_locations:
            self.add_passageway(LevelLocation.Passage_Down, PyrlTile.Stairs_Down)

    def generator_loop(self):
        rand_room_height = partial(randrange, *_room_y_range)
        rand_room_width = partial(randrange, *_room_x_range)
        rand_corridor_height = partial(randrange, *_corridor_y_range)
        rand_corridor_width = partial(randrange, *_corridor_x_range)
        room_start, room_limit = _room_chance_range
        corridor_start, corridor_limit = _corridor_chance_range

        for _ in range(_rdg_level_passes):

            (door_y, door_x), (y_dir, x_dir) = self.get_wall_coord_and_dir()
            artifact_roll = random()

            if corridor_start <= artifact_roll < corridor_limit:

                if y_dir:
                    corridor_length = rand_corridor_height()
                elif x_dir:
                    corridor_length = rand_corridor_width()
                self.attempt_corridor((door_y, door_x), (y_dir, x_dir), corridor_length)

            elif room_start <= artifact_roll < room_limit:

                height, width = rand_room_height(), rand_room_width()
                if y_dir:
                    room_y = door_y
                    room_x = door_x - 1 - randrange(width - 2)
                    height *= y_dir
                elif x_dir:
                    room_y = door_y - 1 - randrange(height - 2)
                    room_x = door_x
                    width *= x_dir
                else:
                    assert False

                room = Rectangle(room_y, room_x, height, width)
                self.attempt_room(room, (door_y, door_x))

            else:
                assert False

    def init_tiles(self):
        self.level_template.tiles = List2D((R for _ in range(self.rows * self.cols)), self.cols)

    def add_passageway(self, passage, passage_tile_id):
        while True:
            coord = self.get_free_coord()
            neighbors = self.get_up_down_left_right_neighbors(coord)
            tile = self.level_template.tiles[coord]

            if neighbors == (F, F, F, F) and tile == F:
                break

        self.level_template.tiles[coord] = passage_tile_id
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
        self.level_template.tiles[y + 2, x + 2] = PyrlTile.Black_Floor

    def attempt_corridor(self, door_coord, direction, length):
        y, x = door_coord
        y_dir, x_dir = direction

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

    def attempt_room(self, rectangle, door_coord):
        if self.rectangle_consists_of_tiles(rectangle, (W, R)):
            self.make_room(rectangle)
            self.level_template.tiles[door_coord] = F
            return True
        else:
            return False

    def get_free_coord(self):
        while True:
            coord = self.get_random_coord()
            if self.level_template.tiles[coord].is_passable:
                return coord

    def get_random_coord(self):
        return randrange(self.rows), randrange(self.cols)

    def get_random_wall_coord(self):
        if self.is_wall_coords_dirty:
            self.wall_coords_cache = tuple(self.wall_coords)
            self.is_wall_coords_dirty = False

        return choice(self.wall_coords_cache)

    def mark_wall(self, coord):
        if coord in self.wall_coords:
            self.wall_coords.remove(coord)
        else:
            self.wall_coords.add(coord)
        self.is_wall_coords_dirty = True

    def get_wall_coord_and_dir(self):
        """Return a random wall coordinate and build direction."""
        while True:
            coord = self.get_random_wall_coord()
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
        dir_map = {(R, F, W, W): Dir.North,
                   (F, R, W, W): Dir.South,
                   (W, W, R, F): Dir.West,
                   (W, W, F, R): Dir.East}
        try:
            return dir_map[neighbors]
        except KeyError:
            return False

    def get_up_down_left_right_neighbors(self, coord):
        tiles = self.level_template.tiles
        neighbors = (
            tiles[add_vector(coord, Dir.North)],
            tiles[add_vector(coord, Dir.South)],
            tiles[add_vector(coord, Dir.West)],
            tiles[add_vector(coord, Dir.East)],
        )
        return neighbors

    def make_room(self, rectangle):
        y_start, x_start, y_limit, x_limit = rectangle

        for y in range(y_start, y_limit):
            for x in range(x_start, x_limit):
                if y in (y_start, y_limit - 1) or x in (x_start, x_limit - 1):
                    self.level_template.tiles[y, x] = W
                    self.mark_wall((y, x))
                else:
                    self.level_template.tiles[y, x] = F

    def rectangle_consists_of_tiles(self, rectangle, tile_seq):
        template = self.level_template
        for coord in rectangle.iterate():
            if not template.tiles.is_legal(coord) or template.tiles[coord] not in tile_seq:
                return False
        return True

    def set_rectangle(self, rectangle, tile):
        """Set all the tiles in rectangle to given tile."""
        if tile == W:
            for coord in rectangle.iterate():
                self.level_template.tiles[coord] = tile
                self.mark_wall(coord)
        else:
            for coord in rectangle.iterate():
                self.level_template.tiles[coord] = tile

    def turn_rock_to_wall(self):
        new_tiles = (t if t != R else W for t in self.level_template.tiles)
        self.level_template.tiles = List2D(new_tiles, self.cols)
