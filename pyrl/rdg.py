from __future__ import annotations

from functools import partial
from random import randrange, random, choice

from pyrl.config.debug import Debug
from pyrl.constants.direction import Dir
from pyrl.constants.level_gen import LevelGen
from pyrl.game_data.levels.shared_assets import DefaultLocation
from pyrl.game_data.tiles import PyrlTile
from pyrl.generic_algorithms import add_vector

def generate_tiles_to(level):
    RDG(level).generate_tiles()

class Rectangle(tuple):
    """
    A Rectangle consists of start coords and limit coords.
    """

    def __new__(cls, y, x, height, width):
        """
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

        return super().__new__(cls, (y_start, x_start, y_limit, x_limit))

    def iterate(self):

        y_start, x_start, y_limit, x_limit = self

        for y in range(y_start, y_limit):
            for x in range(x_start, x_limit):
                yield y, x

class RDG:

    F = PyrlTile.Floor
    W = PyrlTile.Wall
    R = PyrlTile.Rock

    def __init__(self, level):
        self.level = level
        self.rows, self.cols = level.tiles.dimensions.params
        self.generation_type = level.generation_type

        self.level_cycles          = 300
        self.room_y_range          = 5, 11
        self.room_x_range          = 7, 14
        self.corridor_y_range      = 5, 14
        self.corridor_x_range      = 7, 20
        self.corridor_chance_range = 0, 0.3
        self.room_chance_range     = 0.3, 1

        self.wall_coords = set()
        self.wall_coords_cache = tuple()
        self.is_wall_coords_dirty = True

    def generate_tiles(self):
        if self.generation_type == LevelGen.Dungeon:
            self.init_tiles()
            self.make_initial_room()
            self.generator_loop()

        elif self.generation_type == LevelGen.Arena:
            self.init_tiles()
            self.make_room(Rectangle(0, 0, self.rows, self.cols))

        if self.generation_type.value >= LevelGen.Dungeon.value:
            if DefaultLocation.Passage_Up not in self.level.locations.values():
                self.add_location(PyrlTile.Stairs_Up, DefaultLocation.Passage_Up)
            if DefaultLocation.Passage_Down not in self.level.locations.values():
                self.add_location(PyrlTile.Stairs_Down, DefaultLocation.Passage_Down)

    def init_tiles(self):
        for coord, item in self.level.tiles.enumerate():
            self.level.tiles[coord] = self.R

    def generator_loop(self):
        rand_room_height = partial(randrange, *self.room_y_range)
        rand_room_width = partial(randrange, *self.room_x_range)
        rand_corridor_height = partial(randrange, *self.corridor_y_range)
        rand_corridor_width = partial(randrange, *self.corridor_x_range)
        room_start, room_limit = self.room_chance_range
        corridor_start, corridor_limit = self.corridor_chance_range

        for _ in range(self.level_cycles):

            (door_y, door_x), (y_dir, x_dir) = self.get_wall_coord_and_dir()
            artifact_roll = random()

            if corridor_start <= artifact_roll < corridor_limit:

                if y_dir:
                    corridor_length = rand_corridor_height()
                else:
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

    def add_location(self, tile, location):
        for _ in range(Debug.max_loop_cycles):
            coord = self.free_coord()
            neighbors = self.get_up_down_left_right_neighbors(coord)
            old_tile = self.level.tiles[coord]

            if neighbors == (self.F, self.F, self.F, self.F) and old_tile == self.F:
                break
        else:
            assert False, "Location add failed due to free coord get failed."

        self.level.tiles[coord] = tile
        self.level.locations[coord] = location

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
            if self.rectangle_consists_of_tiles(Rectangle(y, x, height, width), (self.W, self.R)):
                break

        self.make_room(Rectangle(y, x, height, width))
        self.level.tiles[y + 2, x + 2] = PyrlTile.Black_Floor

    def attempt_corridor(self, door_coord, direction, length):
        y, x = door_coord
        y_dir, x_dir = direction

        # Corridors are three tiles wide, thus times three
        corridor_rectangle = Rectangle(y - x_dir, x - y_dir, y_dir * length +
                                       x_dir * 3, x_dir * length + y_dir * 3)

        # Floor part of corridor. length - 1 because floor part ends before corridor end wall
        floor_rectangle = Rectangle(y, x, y_dir * (length - 1) + x_dir, x_dir * (length - 1) + y_dir)

        if self.rectangle_consists_of_tiles(corridor_rectangle, (self.W, self.R)):
            self.set_rectangle(corridor_rectangle, self.W)
            self.set_rectangle(floor_rectangle, self.F)
            return True
        else:
            return False

    def attempt_room(self, rectangle, door_coord):
        if self.rectangle_consists_of_tiles(rectangle, (self.W, self.R)):
            self.make_room(rectangle)
            self.level.tiles[door_coord] = self.F
            return True
        else:
            return False

    def free_coord(self):
        while True:
            coord = self.level.tiles.random_coord()
            if self.level.tiles[coord] == self.F:
                return coord

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
        dir_map = {(self.R, self.F, self.W, self.W): Dir.North,
                   (self.F, self.R, self.W, self.W): Dir.South,
                   (self.W, self.W, self.R, self.F): Dir.West,
                   (self.W, self.W, self.F, self.R): Dir.East}
        try:
            return dir_map[neighbors]
        except KeyError:
            return False

    def get_up_down_left_right_neighbors(self, coord):
        tiles = self.level.tiles
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
                    self.level.tiles[y, x] = self.W
                    self.mark_wall((y, x))
                else:
                    self.level.tiles[y, x] = self.F

    def rectangle_consists_of_tiles(self, rectangle, tile_seq):
        tiles = self.level.tiles
        return all(tiles.is_legal(coord) and tiles[coord] in tile_seq for coord in rectangle.iterate())

    def set_rectangle(self, rectangle, tile):
        """Set all the tiles in rectangle to given tile."""
        if tile == self.W:
            for coord in rectangle.iterate():
                self.level.tiles[coord] = tile
                self.mark_wall(coord)
        else:
            for coord in rectangle.iterate():
                self.level.tiles[coord] = tile

    def turn_rock_to_wall(self):
        for coord, tile in self.level.tiles.enumerate():
            if tile == self.R:
                self.level.tiles[coord] = self.W
