from __future__ import absolute_import, division, print_function, unicode_literals

from game_data.tiles import TileImpl
from config.game import GameConf
from enums.directions import Dir
from enums.level_locations import LevelLocation
from generic_algorithms import add_vector
from rdg import GenLevelType, generate_tilemap
from game_data.monsters import monster_templates


class LevelTemplate(object):

    default_level_type = GenLevelType.Dungeon

    def __init__(self, danger_level=0, use_dynamic_monsters=True, tilemap=None,
                 static_monster_seq=(), dimensions=GameConf.LEVEL_DIMENSIONS):
        self.danger_level = danger_level
        self.tilemap = tilemap
        self.use_dynamic_monsters = use_dynamic_monsters
        self.rows, self.cols = dimensions
        self.passage_locations = {}
        self.passage_destination_infos = {}
        self.static_monster_templates = list(static_monster_seq)
        self.dynamic_monster_amount = 99

    def finalize(self):
        if self.tilemap is None:
            generate_tilemap(self, self.default_level_type)
        else:
            self._finalize_manual_tilemap()

    def is_legal(self, coord):
        y, x = coord
        return (0 <= y < self.rows) and (0 <= x < self.cols)

    def get_tile(self, coord):
        y, x = coord
        return self.tilemap[y * self.cols + x]

    def set_tile(self, coord, tile):
        y, x = coord
        self.tilemap[y * self.cols + x] = tile

    def add_monster_template(self, monster):
        self.static_monster_templates.append(monster)

    def get_dynamic_monster_spawn_list(self):
        monster_list = []
        for monster in monster_templates:
            start = monster.speciation_lvl
            if start <= self.danger_level:
                weight_coeff = self.danger_level - monster.speciation_lvl
                monster_list.extend((monster, ) * weight_coeff)
        return monster_list

    def _finalize_manual_tilemap(self):
        for index, tile in enumerate(self.tilemap):
            coord = index // self.cols, index % self.cols
            if tile == TileImpl.Stairs_Up.value:
                self.passage_locations[LevelLocation.Passage_Up] = coord
            elif tile == TileImpl.Stairs_Down.value:
                self.passage_locations[LevelLocation.Passage_Down] = coord

        self._transform_dynamic_walls()
        self._fill_rock()

    def _transform_dynamic_walls(self):
        self.tilemap = [TileImpl.Wall.value if self._dynamic_wall_qualifies_as_wall(tile, index)
                                    else tile for index, tile in enumerate(self.tilemap)]

    def _dynamic_wall_qualifies_as_wall(self, tile, index):
        if tile != TileImpl.Dynamic_Wall.value:
            return False
        coord = index // self.cols, index % self.cols
        neighbor_coords = (add_vector(coord, direction) for direction in Dir.All)
        valid_tiles = (self.get_tile(coord) for coord in neighbor_coords if self.is_legal(coord))
        return any(handle not in (TileImpl.Dynamic_Wall.value,
                                  TileImpl.Wall.value,
                                  TileImpl.Rock.value) for handle in valid_tiles)

    def _fill_rock(self):
        self.tilemap = [TileImpl.Rock.value if tile == TileImpl.Dynamic_Wall.value else tile for tile in self.tilemap]
