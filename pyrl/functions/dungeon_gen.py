from __future__ import annotations

from collections.abc import Sequence
from functools import partial
from random import randrange, random, choice
from typing import TYPE_CHECKING

from pyrl.functions.coord_algorithms import add_vector
from pyrl.config.debug import Debug
from pyrl.structures.dimensions import Dimensions
from pyrl.structures.helper_mixins import DimensionsMixin
from pyrl.structures.rectangle import Rectangle
from pyrl.game_data.levels.shared_assets import DefaultLocation
from pyrl.game_data.pyrl_tiles import PyrlTiles
from pyrl.structures.table import Table
from pyrl.types.directions import Dir, Direction, Coord
from pyrl.world.world_types import LevelLocation, LevelGen
from pyrl.world.tile import Tile

if TYPE_CHECKING:
    from pyrl.world.level_gen_params import LevelGenParams

Floor = PyrlTiles.Floor
Wall = PyrlTiles.Wall
Rock = PyrlTiles.Rock

class DungeonGen(DimensionsMixin):

    def __init__(self, level_params: LevelGenParams) -> None:
        if level_params.tiles is not None:
            self.tiles = level_params.tiles
            self.dimensions = self.tiles.dimensions
        elif level_params.dimensions is not None:
            self.dimensions = level_params.dimensions
            self.tiles = Table(self.dimensions, fillvalue=Rock)
        else:
            raise ValueError(f"Can't generate tiles to {level_params=} which has neither dimensions nor tiles set")

        self.generation_type = level_params.generation_type
        self.locations = level_params.locations

        self.level_cycles          = 300
        self.room_y_range          = 5, 11
        self.room_x_range          = 7, 14
        self.corridor_y_range      = 5, 14
        self.corridor_x_range      = 7, 20
        self.corridor_chance_range = 0, 0.3
        self.room_chance_range     = 0.3, 1

        self.wall_coords: set[Coord] = set()
        self.wall_coords_cache: tuple[Coord, ...] = tuple()
        self.is_wall_coords_dirty = True

    def generate_tiles(self) -> Table[Tile]:
        if self.generation_type == LevelGen.Dungeon:
            self.make_initial_room()
            self.generator_loop()

        elif self.generation_type == LevelGen.Arena:
            self.make_room(Rectangle((0, 0), self.dimensions))

        if self.generation_type.value >= LevelGen.Dungeon.value:
            if DefaultLocation.Passage_Up not in self.locations.values():
                self.add_location(PyrlTiles.Stairs_Up, DefaultLocation.Passage_Up)
            if DefaultLocation.Passage_Down not in self.locations.values():
                self.add_location(PyrlTiles.Stairs_Down, DefaultLocation.Passage_Down)

        return self.tiles

    def generator_loop(self) -> None:
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

                room = Rectangle((room_y, room_x), Dimensions(height, width))
                self.attempt_room(room, (door_y, door_x))

            else:
                assert False

    def add_location(self, tile: Tile, location: LevelLocation) -> None:
        for _ in range(Debug.max_loop_cycles):
            coord = self.free_coord()
            neighbors = self.get_up_down_left_right_neighbors(coord)
            old_tile = self.tiles[coord]

            if neighbors == (Floor, Floor, Floor, Floor) and old_tile == Floor:
                break
        else:
            assert False, "Location add failed due to free coord get failed."

        self.tiles[coord] = tile
        self.locations[coord] = location

    def make_initial_room(self) -> None:
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
            if self.rectangle_consists_of_tiles(Rectangle((y, x), Dimensions(height, width)), (Wall, Rock)):
                break

        self.make_room(Rectangle((y, x), Dimensions(height, width)))
        self.tiles[y + 2, x + 2] = PyrlTiles.Black_Floor

    def attempt_corridor(self, door_coord: Coord, direction: Direction, length: int) -> bool:
        y, x = door_coord
        y_dir, x_dir = direction

        # Corridors are three tiles wide, thus times three
        corridor_rectangle = Rectangle((y - x_dir, x - y_dir),
                                       Dimensions(y_dir * length + x_dir * 3, x_dir * length + y_dir * 3))

        # Floor part of corridor. length - 1 because floor part ends before corridor end wall
        floor_rectangle = Rectangle((y, x), Dimensions(y_dir * (length - 1) + x_dir, x_dir * (length - 1) + y_dir))

        if self.rectangle_consists_of_tiles(corridor_rectangle, (Wall, Rock)):
            self.set_rectangle(corridor_rectangle, Wall)
            self.set_rectangle(floor_rectangle, Floor)
            return True
        else:
            return False

    def attempt_room(self, rectangle: Rectangle, door_coord: Coord) -> bool:
        if self.rectangle_consists_of_tiles(rectangle, (Wall, Rock)):
            self.make_room(rectangle)
            self.tiles[door_coord] = Floor
            return True
        else:
            return False

    def free_coord(self) -> Coord:
        while True:
            coord = self.tiles.random_coord()
            if self.tiles[coord] == Floor:
                return coord

    def get_random_wall_coord(self) -> Coord:
        if self.is_wall_coords_dirty:
            self.wall_coords_cache = tuple(self.wall_coords)
            self.is_wall_coords_dirty = False

        return choice(self.wall_coords_cache)

    def mark_wall(self, coord: Coord) -> None:
        if coord in self.wall_coords:
            self.wall_coords.remove(coord)
        else:
            self.wall_coords.add(coord)
        self.is_wall_coords_dirty = True

    def get_wall_coord_and_dir(self) -> tuple[Coord, Direction]:
        """Return a random wall coordinate and build direction."""
        while True:
            coord = self.get_random_wall_coord()
            direction = self.get_edge_direction(coord)
            if direction:
                return coord, direction

    def get_edge_direction(self, coord: Coord) -> Direction | None:
        """Return a valid direction if the coordinate is an edge with a buildable direction."""
        y, x = coord

        # Exclude map border squares
        if y in (0, self.rows - 1) or x in (0, self.cols - 1):
            return None

        neighbors = self.get_up_down_left_right_neighbors(coord)
        dir_map = {(Rock, Floor, Wall, Wall): Dir.North,
                   (Floor, Rock, Wall, Wall): Dir.South,
                   (Wall, Wall, Rock, Floor): Dir.West,
                   (Wall, Wall, Floor, Rock): Dir.East}
        try:
            return dir_map[neighbors]
        except KeyError:
            return None

    def get_up_down_left_right_neighbors(self, coord: Coord) -> tuple[Tile, Tile, Tile, Tile]:
        tiles = self.tiles
        neighbors = (
            tiles[add_vector(coord, Dir.North)],
            tiles[add_vector(coord, Dir.South)],
            tiles[add_vector(coord, Dir.West)],
            tiles[add_vector(coord, Dir.East)],
        )
        return neighbors

    def make_room(self, rectangle: Rectangle) -> None:
        for (is_edge, coord) in rectangle.enumerate_with_edge():
            if is_edge:
                self.tiles[coord] = Wall
                self.mark_wall(coord)
            else:
                self.tiles[coord] = Floor

    def rectangle_consists_of_tiles(self, rectangle: Rectangle, given_tiles: Sequence[Tile]) -> bool:
        tiles = self.tiles
        return all(tiles.is_legal(coord) and tiles[coord] in given_tiles for coord in rectangle.iterate())

    def set_rectangle(self, rectangle: Rectangle, tile: Tile) -> None:
        """Set all the tiles in rectangle to given tile."""
        if tile == Wall:
            for coord in rectangle.iterate():
                self.tiles[coord] = tile
                self.mark_wall(coord)
        else:
            for coord in rectangle.iterate():
                self.tiles[coord] = tile

    def turn_rock_to_wall(self) -> None:
        for coord, tile in self.tiles.enumerate():
            if tile == Rock:
                self.tiles[coord] = Wall
