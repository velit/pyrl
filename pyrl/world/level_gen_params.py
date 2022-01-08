from __future__ import annotations

from dataclasses import dataclass, field

from pyrl.functions.dungeon_generator import generate_tiles_to
from pyrl.creature.creature import Creature
from pyrl.game_data.levels.shared_assets import default_dims, DefaultLocation
from pyrl.structures.uniq_dict import UniqDict
from pyrl.structures.table import Table
from pyrl.types.coord import Coord
from pyrl.types.level_gen import LevelGen
from pyrl.types.level_key import LevelKey
from pyrl.types.level_location import LevelLocation
from pyrl.world.level import Level
from pyrl.world.tile import Tile

@dataclass
class LevelGenParams:
    area_level: int                         = 0
    tiles: Table[Tile]                        = field(default_factory=lambda: Table(default_dims))
    locations: UniqDict[Coord, LevelLocation] = field(default_factory=UniqDict)
    custom_creatures: list[Creature]          = field(default_factory=list)
    initial_creature_spawns: bool             = True
    ongoing_creature_spawns: bool             = True
    generation_type: LevelGen                 = LevelGen.Dungeon

    def will_have_location(self, location: LevelLocation) -> bool:
        if location == DefaultLocation.Random_Location:
            return True

        if location in self.locations.values():
            return True

        if self.generation_type != LevelGen.NoGeneration:
            return location in DefaultLocation

        return False

    def create_level(self, level_key: LevelKey) -> Level:
        if self.generation_type.is_used():
            generate_tiles_to(self)
        return Level(
            level_key,
            area_level=self.area_level,
            tiles=self.tiles,
            locations=self.locations,
            custom_creatures=self.custom_creatures,
            initial_creature_spawns=self.initial_creature_spawns,
            ongoing_creature_spawns=self.ongoing_creature_spawns,
        )
