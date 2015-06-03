from __future__ import absolute_import, division, print_function, unicode_literals

from rdg import generate_tiles_to, LevelGen
from config.game import GameConf
from game_data.creatures import creature_templates
from generic_structures import Array2D
from level import LevelLocation


class LevelTemplate(object):

    def __init__(self, danger_level=0, generation_type=LevelGen.Dungeon, tiles=None,
                 location_coords=None, custom_creatures=(), creature_spawning=True):
        self.danger_level = danger_level
        if tiles is None:
            self.tiles = Array2D(GameConf.LEVEL_DIMENSIONS)
        else:
            self.tiles = tiles
        self.location_coords = {}
        self.exit_infos = {}
        self.custom_creatures = list(custom_creatures)
        self.creature_spawning = creature_spawning
        self.creature_spawn_count = 99

        self.exit_point_info = []

        self.generation_type = generation_type
        if self.generation_type.value > LevelGen.ExtendExisting.value:
            self.rows, self.cols = self.tiles.dimensions
        else:
            self.rows, self.cols = GameConf.LEVEL_DIMENSIONS

        if location_coords is not None:
            self.location_coords.update(location_coords)

    def get_creature_spawn_list(self):
        creature_list = []
        for creature in creature_templates:
            start = creature.speciation_lvl
            if start <= self.danger_level:
                weight_coeff = self.danger_level - creature.speciation_lvl
                creature_list.extend((creature, ) * weight_coeff)
        return creature_list

    def will_have_location(self, location):
        if location == LevelLocation.Random_Location:
            return True

        if location in self.location_coords:
            return True

        if self.generation_type != LevelGen.NoGeneration:
            return location in LevelLocation

        return False

    def add_exit_info(self, source_location, target_info):
        self.exit_point_info.append((source_location, target_info))

    def finalize(self):
        if self.generation_type.is_used():
            generate_tiles_to(self)

        self._finalize_exit_infos()

        return self

    def _finalize_exit_infos(self):
        """
        Set exit point data based on previously given exit point info.

        This delayed definition is required because non-custom levels are generated on the
        fly and coord info for the level location_coords doesn't exist yet at the time of
        defining the connections between levels.
        """
        for source_location, target_info in self.exit_point_info:
            source_coord = self.location_coords[source_location]
            self.exit_infos[source_coord] = target_info
