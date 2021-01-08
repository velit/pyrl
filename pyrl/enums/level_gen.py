from enum import Enum

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

    def is_used(self):
        return self != LevelGen.NoGeneration
