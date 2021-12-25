from __future__ import annotations

import pytest

from pyrl import rdg
from pyrl.game_data.levels.shared_assets import construct_data, DefaultLocation
from pyrl.game_data.tiles import PyrlTile
from pyrl.generic_structures.dimensions import Dimensions
from pyrl.generic_structures.table import Table
from pyrl.world.level import Level

def pp_tm(tm, cols):
    """Pretty print tiles."""
    for i, c in enumerate(tm):
        print(c, end=('' if i % cols != cols - 1 else '\n'))

@pytest.mark.slow
def test_many_rdg_generation():
    for _ in range(100):
        level = Level(generation_type=rdg.LevelGen.Dungeon)
        rdg.generate_tiles_to(level)
        assert level.tiles[level.locations.getkey(DefaultLocation.Passage_Down)] == PyrlTile.Stairs_Down
        assert level.tiles[level.locations.getkey(DefaultLocation.Passage_Up)] == PyrlTile.Stairs_Up

def test_rdg_generation():
    level = Level(generation_type=rdg.LevelGen.Dungeon)
    rdg.generate_tiles_to(level)
    assert level.tiles[level.locations.getkey(DefaultLocation.Passage_Down)] == PyrlTile.Stairs_Down
    assert level.tiles[level.locations.getkey(DefaultLocation.Passage_Up)] == PyrlTile.Stairs_Up

@pytest.fixture
def rectangles():
    return (
        rdg.Rectangle(0, 0, 10, 5),
        rdg.Rectangle(0, 0, 10, 10),
        rdg.Rectangle(10, 10, -10, -10),
        rdg.Rectangle(20, 20, -10, 10),
    )

def test_rectangle(rectangles):
    r1, r2, r3, r4 = rectangles
    assert r1 == (0, 0, 10, 5)
    assert r2 == (0, 0, 10, 10)
    assert r3 == (1, 1, 11, 11)
    assert r4 == (11, 20, 21, 30)

TEST_DIMENSIONS = Dimensions(10, 10)

@pytest.fixture
def generator():
    level = Level(tiles=Table(TEST_DIMENSIONS))
    generator = rdg.RDG(level)
    generator.init_tiles()
    return generator

def test_dungeon_generation(rectangles, generator):
    rect = rectangles[0]

    generator.attempt_room(rect, (0, 1))
    room, _, _ = construct_data(
        TEST_DIMENSIONS,
        "w.wwwrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "wwwwwrrrrr",
        {}, {}, {},
    )
    assert generator.level.tiles == room

    generator.attempt_corridor((4, 4), (0, 1), 6)
    room, _, _ = construct_data(
        TEST_DIMENSIONS,
        "w.wwwrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wwwwww"
        "w........w"
        "w...wwwwww"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "wwwwwrrrrr",
        {}, {}, {},
    )
    assert generator.level.tiles == room
