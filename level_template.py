from __future__ import absolute_import, division, print_function, unicode_literals

from enums.directions import Dir
from enums.level_locations import LevelLocation
from game_data.creatures import creature_templates
from game_data.tiles import PyrlTile
from generic_algorithms import add_vector
from rdg import GenLevelType, generate_tiles
from generic_structures import List2D
from config.game import GameConf


class LevelTemplate(object):

    default_level_type = GenLevelType.Dungeon

    def __init__(self, danger_level=0, dimensions=GameConf.LEVEL_DIMENSIONS, tiles=None,
                 static_creatures=(), creature_spawning=True):
        self.danger_level = danger_level
        self.tiles = tiles
        self.rows, self.cols = dimensions
        self.passage_locations = {}
        self.passage_destination_infos = {}
        self.static_creatures = list(static_creatures)
        self.creature_spawning = creature_spawning
        self.creature_spawn_count = 99

    def finalize(self):
        if self.tiles is None:
            generate_tiles(self, self.default_level_type)
        else:
            self._finalize_manual_tiles()

    def get_creature_spawn_list(self):
        creature_list = []
        for creature in creature_templates:
            start = creature.speciation_lvl
            if start <= self.danger_level:
                weight_coeff = self.danger_level - creature.speciation_lvl
                creature_list.extend((creature, ) * weight_coeff)
        return creature_list

    def _finalize_manual_tiles(self):
        self.tiles = List2D((self._finalize_tile(tile, self.tiles, index) for
                             index, tile in enumerate(self.tiles)), self.tiles._bound)

    def _finalize_tile(self, tile, tiles, index):
        coord = self.tiles.get_coord(index)
        if tile.exit_point is not None:
            self.passage_locations[tile.exit_point] = coord

        if tile != PyrlTile.Dynamic_Wall:
            return tile

        neighbor_coords = (add_vector(coord, direction) for direction in Dir.All)
        neighbor_tiles = (tiles[coord] for coord in neighbor_coords if tiles.is_legal(coord))
        rocks = (PyrlTile.Dynamic_Wall, PyrlTile.Wall, PyrlTile.Rock)
        if any(handle not in rocks for handle in neighbor_tiles):
            return PyrlTile.Wall
        else:
            return PyrlTile.Rock
