from __future__ import absolute_import, division, print_function, unicode_literals

import rdg
import const.game as GAME
import templates.tiles as TILE
import const.directions as DIR

from generic_algorithms import add_vector
from templates.monsters import monster_templates


def gettile(handle, tile_dict=None):
    if tile_dict is not None and handle in tile_dict:
        return tile_dict[handle]
    elif handle in TILE.tiles:
        return TILE.tiles[handle]
    else:
        raise KeyError("Handle '{}' not in global tiles nor in '{}'".format(handle, tile_dict))


class LevelTemplate(object):

    def __init__(self, danger_level=0, tilemap_template=None,
                 static_level=False, use_dynamic_monsters=True,
                 rows=GAME.LEVEL_HEIGHT, cols=GAME.LEVEL_WIDTH):
        self.danger_level = danger_level
        self.tilemap_template = tilemap_template
        self.static_level = static_level
        self.use_dynamic_monsters = use_dynamic_monsters
        self.rows = rows
        self.cols = cols
        self.passage_locations = {}
        self.static_monster_templates = []
        self.tile_dict = {}

    def finalize(self):
        if not self.static_level:
            rdg.generate_tilemap_template(self, GAME.LEVEL_TYPE)

    def get_tile_handle(self, y, x):
        return self.tilemap_template[y * self.cols + x]

    def set_tile_handle(self, y, x, tile_id):
        self.tilemap_template[y * self.cols + x] = tile_id

    def get_tile_from_coord(self, y, x):
        return gettile(self.get_tile_handle(y, x), self.tile_dict)

    def tilemap(self):
        for key in self.tilemap_template:
            yield gettile(key, self.tile_dict)

    def add_monster_file(self, monster):
        self.static_monster_templates.append(monster)

    def legal_coord(self, coord):
        return (0 <= coord[0] < self.rows) and (0 <= coord[1] < self.cols)

    def get_dynamic_monster_spawn_list(self):
        monster_list = []
        for monster in monster_templates:
            start = monster.speciation_lvl
            if start <= self.danger_level:
                weight_coeff = self.danger_level - monster.speciation_lvl
                monster_list.extend((monster, ) * weight_coeff)
        return monster_list

    def _add_walls(self):
        self.tilemap_template = [TILE.WALL if self._tile_qualifies_as_wall(loc, tile)
                                 else tile for loc, tile in enumerate(self.tilemap_template)]

    def _tile_qualifies_as_wall(self, loc, tile_handle):
        if tile_handle != TILE.ROCK:
            return False
        coord = loc // self.cols, loc % self.cols
        neighbor_coords = (add_vector(coord, direction) for direction in DIR.ALL_MINUS_STOP)
        valid_handles = (self.get_tile_handle(*coord) for coord in neighbor_coords if self.legal_coord(coord))
        return any(handle not in (TILE.WALL, TILE.ROCK) for handle in valid_handles)
