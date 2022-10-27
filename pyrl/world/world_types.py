from __future__ import annotations

from enum import Enum
from typing import NamedTuple

class LevelLocation(Enum):
    """Key for various interesting locations inside Levels. This is the supertype."""
    pass

class LevelGen(Enum):
    """
    Dictates what sort of level generation is applied when generating level tiles.

    NoGeneration: Use given tiles as is.
    ExtendExisting: Extend the given tiles using standard dungeon generation.
    Dungeon: Generate a standard dungeon overwriting any existing tiles.
    Arena: Generate an empty arena spanning the whole level overwriting any existing tiles.
    """
    NoGeneration   = 1
    ExtendExisting = 2  # TODO: Not implemented
    Dungeon        = 3
    Arena          = 4

    def is_used(self) -> bool:
        return self != LevelGen.NoGeneration

class WorldPoint(NamedTuple):
    """Describes a specific level and location. Used for marking passage connections."""
    level_key: LevelKey
    level_location: LevelLocation

class LevelKey(NamedTuple):
    """Uniquely identifies a Level.
    Levels are found in dungeons and the idx identifies which level in that dungeon."""
    dungeon: str
    idx: int
