from __future__ import annotations

from pyrl.constants.char import Letter
from pyrl.constants.coord import Coord
from pyrl.constants.direction import Dir
from pyrl.constants.level_location import LevelLocation
from pyrl.creature.creature import Creature
from pyrl.game_data.tiles import PyrlTile
from pyrl.generic_algorithms import add_vector
from pyrl.generic_structures.table import Table
from pyrl.generic_structures.dimensions import Dimensions
from pyrl.world.tile import Tile

default_dims = Dimensions(26, 96)

class DefaultLocation(LevelLocation):
    Passage_Up      = 1
    Passage_Down    = 2
    Random_Location = 3

base_tiles: dict[Letter, Tile] = {
    '.': PyrlTile.Floor,
    'w': PyrlTile.Wall,
    '#': PyrlTile.Dynamic_Wall,
    'r': PyrlTile.Rock,
    '/': PyrlTile.Open_Door,
    '+': PyrlTile.Closed_Door,
    '>': PyrlTile.Stairs_Down,
    '<': PyrlTile.Stairs_Up,
}

base_creatures: dict[Letter, Creature] = {
}

base_locations: dict[Letter, LevelLocation] = {
    '<': DefaultLocation.Passage_Up,
    '>': DefaultLocation.Passage_Down,
}

def construct_data(dimensions: Dimensions, table_data: str, custom_tiles: dict[Letter, Tile],
                   custom_locations: dict[Letter, LevelLocation], custom_creatures: dict[Letter, Creature]) \
                   -> tuple[Table[Tile], dict[Coord, LevelLocation], list[Creature]]:

    _assert_dimensions(dimensions, table_data)
    unfinalized_tiles = Table(dimensions, table_data)

    tiles_lookup = base_tiles.copy()
    tiles_lookup.update(custom_tiles)

    locations = base_locations.copy()
    locations.update(custom_locations)

    creatures_lookup = base_creatures.copy()
    creatures_lookup.update(custom_creatures)

    return _construct_data(unfinalized_tiles, tiles_lookup, locations, creatures_lookup)

def _assert_dimensions(dimensions: Dimensions, table_data: str) -> None:
    assert len(table_data) == dimensions.area, "Wrong dimensions for custom level definition."

def _construct_data(unfinalized_tiles: Table, tiles_lookup: dict[Letter, Tile],
                    locations_lookup: dict[Letter, LevelLocation], creatures_lookup: dict[Letter, Creature]) \
                        -> tuple[Table[Tile], dict[Coord, LevelLocation], list[Creature]]:
    tiles = unfinalized_tiles
    locations = {}
    creatures = []
    for coord, char in tiles.enumerate():

        tiles[coord] = tiles_lookup[char]

        if char in locations_lookup:
            locations[coord] = locations_lookup[char]

        if char in creatures_lookup:
            creature = creatures_lookup[char]
            creature.coord = coord
            creatures.append(creature)

    _finalize_tiles(tiles)
    return tiles, locations, creatures

def _finalize_tiles(tiles: Table) -> None:
    for coord, tile in tiles.enumerate():
        tiles[coord] = _finalize_tile(coord, tile, tiles)

def _finalize_tile(coord: Coord, tile: Tile, tiles: Table) -> Tile:
    if tile != PyrlTile.Dynamic_Wall:
        return tile

    neighbor_coords = (add_vector(coord, direction) for direction in Dir.All)
    neighbor_tiles = (tiles[coord] for coord in neighbor_coords if tiles.is_legal(coord))
    rocks = (PyrlTile.Dynamic_Wall, PyrlTile.Wall, PyrlTile.Rock)
    if any(handle not in rocks for handle in neighbor_tiles):
        return PyrlTile.Wall
    else:
        return PyrlTile.Rock
