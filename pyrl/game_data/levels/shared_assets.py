from __future__ import annotations

from pyrl.types.char import Letter
from pyrl.types.coord import Coord
from pyrl.types.direction import Dir
from pyrl.types.level_location import LevelLocation
from pyrl.creature.creature import Creature
from pyrl.game_data.pyrl_tiles import PyrlTiles
from pyrl.algorithms.coord_algorithms import add_vector
from pyrl.structures.table import Table
from pyrl.structures.dimensions import Dimensions
from pyrl.world.tile import Tile

default_dims = Dimensions(26, 96)

class DefaultLocation(LevelLocation):
    Passage_Up      = 1
    Passage_Down    = 2
    Random_Location = 3

AssetTileDict = dict[Letter, Tile]
AssetCreatureDict = dict[Letter, Creature]
AssetLocationDict = dict[Letter, LevelLocation]

base_tiles: AssetTileDict = {
    '.': PyrlTiles.Floor,
    'w': PyrlTiles.Wall,
    '#': PyrlTiles.Dynamic_Wall,
    'r': PyrlTiles.Rock,
    '/': PyrlTiles.Open_Door,
    '+': PyrlTiles.Closed_Door,
    '>': PyrlTiles.Stairs_Down,
    '<': PyrlTiles.Stairs_Up,
}

base_creatures: AssetCreatureDict = {
}

base_locations: AssetLocationDict = {
    '<': DefaultLocation.Passage_Up,
    '>': DefaultLocation.Passage_Down,
}

def construct_data(dimensions: Dimensions, table_data: str, custom_tiles: AssetTileDict,
                   custom_locations: AssetLocationDict, custom_creatures: AssetCreatureDict) \
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

def _construct_data(unfinalized_tiles: Table, tiles_lookup: AssetTileDict,
                    locations_lookup: AssetLocationDict, creatures_lookup: AssetCreatureDict) \
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
    if tile != PyrlTiles.Dynamic_Wall:
        return tile

    neighbor_coords = (add_vector(coord, direction) for direction in Dir.All)
    neighbor_tiles = (tiles[coord] for coord in neighbor_coords if tiles.is_legal(coord))
    rocks = (PyrlTiles.Dynamic_Wall, PyrlTiles.Wall, PyrlTiles.Rock)
    if any(handle not in rocks for handle in neighbor_tiles):
        return PyrlTiles.Wall
    else:
        return PyrlTiles.Rock
