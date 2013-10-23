from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import const.game as GAME
import const.tiles as TILE
import const.directions as DIR
import const.monsters as MONSTER

from generic_algorithms import add_vector


def gettile(handle, tile_dict=None):
    if tile_dict is not None and handle in tile_dict:
        return tile_dict[handle]
    elif handle in TILE.tiles:
        return TILE.tiles[handle]
    else:
        raise KeyError("Handle '{}' not in global tiles nor in '{}'".format(handle, tile_dict))


class LevelFile(object):

    def __init__(self, danger_level=0, tilefile=None, static_level=False,
                 use_dynamic_monsters=True, rows=GAME.LEVEL_HEIGHT, cols=GAME.LEVEL_WIDTH):
        self.danger_level = danger_level
        self.tilefile = tilefile
        self.static_level = static_level
        self.use_dynamic_monsters = use_dynamic_monsters
        self.rows = rows
        self.cols = cols
        self.passage_locations = {}
        self.static_monster_files = []
        self.tile_dict = {}

    def get_tile_id(self, y, x):
        return self.tilefile[y * self.cols + x]

    def set_tile_id(self, y, x, tile_id):
        self.tilefile[y * self.cols + x] = tile_id

    def get_tile_from_coord(self, y, x):
        return gettile(self.get_tile_id(y, x), self.tile_dict)

    def get_tile_from_loc(self, loc):
        return gettile(self.tilefile[loc], self.tile_dict)

    def tilemap(self):
        for key in self.tilefile:
            yield gettile(key, self.tile_dict)

    def add_monster_file(self, monster):
        self.static_monster_files.append(monster)

    def legal_coord(self, coord):
        return (0 <= coord[0] < self.rows) and (0 <= coord[1] < self.cols)

    def neighbors(self, y, x):
        for direction in DIR.ALL_MINUS_STOP:
            c = add_vector((y, x), direction)
            if self.legal_coord(c):
                yield self.get_tile_id(*c)

    def add_walls(self):
        for y, x in ((y, x) for y in range(self.rows) for x in range(self.cols)):
            if self.get_tile_id(y, x) == TILE.ROCK and any(
                    tile_id not in (TILE.WALL, TILE.ROCK) for tile_id in self.neighbors(y, x)):
                self.set_tile_id(y, x, TILE.WALL)

    def get_dynamic_monster_spawn_list(self):
        monster_list = []
        for monster in MONSTER.monster_files:
            start = monster.speciation_lvl
            if start <= self.danger_level:
                weight_coeff = self.danger_level - monster.speciation_lvl
                monster_list.extend((monster, ) * weight_coeff)
        return monster_list
