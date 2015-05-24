from __future__ import absolute_import, division, print_function, unicode_literals
from generic_structures import List2D
from game_data.tiles import PyrlTile


base_tiles = {
    '.': PyrlTile.Floor,
    'w': PyrlTile.Wall,
    '#': PyrlTile.Dynamic_Wall,
    'r': PyrlTile.Rock,
    '/': PyrlTile.Open_Door,
    '+': PyrlTile.Closed_Door,
    '"': PyrlTile.Grass,
    '>': PyrlTile.Stairs_Down,
    '<': PyrlTile.Stairs_Up,
    'P': PyrlTile.Stairs_Up,
    '@': PyrlTile.Floor,
}


def finalize_tiles(chars):
    return List2D((base_tiles[char] for char in chars), chars._bound)


def finalize_creatures(creature_dict, chars):
    for index, char in enumerate(chars):
        if char in creature_dict:
            creature = creature_dict[char]
            creature.coord = chars.get_coord(index)

    return tuple(creature_dict.values())
