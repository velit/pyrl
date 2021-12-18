from pyrl.creature.creature import Creature
from pyrl.enums.directions import Dir
from pyrl.game_data.tiles import PyrlTile
from pyrl.generic_algorithms import add_vector
from pyrl.generic_structures import Array2D, TableDims
from pyrl.enums.level_location import LevelLocation

default_level_dimensions = TableDims(26, 96)

base_tiles = {
    '.': PyrlTile.Floor,
    'w': PyrlTile.Wall,
    '#': PyrlTile.Dynamic_Wall,
    'r': PyrlTile.Rock,
    '/': PyrlTile.Open_Door,
    '+': PyrlTile.Closed_Door,
    '>': PyrlTile.Stairs_Down,
    '<': PyrlTile.Stairs_Up,
}

base_creatures: dict[str, Creature] = {
}

base_locations = {
    '<': LevelLocation.Passage_Up,
    '>': LevelLocation.Passage_Down,
}

def construct_data(dimensions, charstr, custom_tiles, custom_locations, custom_creatures):
    _assert_size(charstr, dimensions)
    unfinalized_tiles = Array2D(dimensions, charstr)

    tiles_lookup = base_tiles.copy()
    tiles_lookup.update(custom_tiles)

    locations = base_locations.copy()
    locations.update(custom_locations)

    creatures_lookup = base_creatures.copy()
    creatures_lookup.update(custom_creatures)

    return _construct_data(unfinalized_tiles, tiles_lookup, locations, creatures_lookup)

def _assert_size(charstr, dimensions):
    assert len(charstr) == dimensions[0] * dimensions[1], \
        "Wrong dimensions for custom level definition."

def _construct_data(unfinalized_tiles, tiles_lookup, locations_lookup, creatures_lookup):
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

def _finalize_tiles(tiles):
    for coord, tile in tiles.enumerate():
        tiles[coord] = _finalize_tile(coord, tile, tiles)

def _finalize_tile(coord, tile, tiles):
    if tile != PyrlTile.Dynamic_Wall:
        return tile

    neighbor_coords = (add_vector(coord, direction) for direction in Dir.All)
    neighbor_tiles = (tiles[coord] for coord in neighbor_coords if tiles.is_legal(coord))
    rocks = (PyrlTile.Dynamic_Wall, PyrlTile.Wall, PyrlTile.Rock)
    if any(handle not in rocks for handle in neighbor_tiles):
        return PyrlTile.Wall
    else:
        return PyrlTile.Rock
