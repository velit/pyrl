from __future__ import annotations

from typing import NamedTuple

from pyrl.engine.world.enums.level_location import LevelLocation
from pyrl.engine.world.enums.level_key import LevelKey

class WorldPoint(NamedTuple):
    """Describes a specific level and location. Used for marking passage connections."""
    level_key: LevelKey
    level_location: LevelLocation
