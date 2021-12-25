from __future__ import annotations

from typing import NamedTuple

from pyrl.types.level_key import LevelKey
from pyrl.types.level_location import LevelLocation

class WorldPoint(NamedTuple):
    """Describes a specific level and location. Used for marking passage connections."""
    level_key: LevelKey
    level_location: LevelLocation
