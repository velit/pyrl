from __future__ import annotations

from typing import NamedTuple

class LevelKey(NamedTuple):
    """Uniquely identifies a Level.
    Levels are found in dungeons and the idx identifies which level in that dungeon."""
    dungeon: str
    idx: int
