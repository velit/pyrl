from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import pytest

from pyrl.dungeon_generation import rdg
from pyrl.game_data.levels.shared_assets import construct_data, DefaultLocation
from pyrl.game_data.pyrl_tiles import PyrlTiles
from pyrl.dungeon_generation.rdg import RDG
from pyrl.structures.dimensions import Dimensions
from pyrl.structures.table import Table
from pyrl.types.level_gen import LevelGen
from pyrl.world.level import Level

def pp_tm(tile_matrix: Iterable[Any], cols: int) -> None:
    """Pretty print tiles."""
    for i, char in enumerate(tile_matrix):
        print(char, end=('' if i % cols != cols - 1 else '\n'))

@pytest.mark.slow
def test_many_rdg_generation() -> None:
    for _ in range(100):
        level = Level(generation_type=LevelGen.Dungeon)
        rdg.generate_tiles_to(level)
        assert level.tiles[level.locations.getkey(DefaultLocation.Passage_Down)] == PyrlTiles.Stairs_Down
        assert level.tiles[level.locations.getkey(DefaultLocation.Passage_Up)] == PyrlTiles.Stairs_Up

def test_rdg_generation() -> None:
    level = Level(generation_type=LevelGen.Dungeon)
    rdg.generate_tiles_to(level)
    assert level.tiles[level.locations.getkey(DefaultLocation.Passage_Down)] == PyrlTiles.Stairs_Down
    assert level.tiles[level.locations.getkey(DefaultLocation.Passage_Up)] == PyrlTiles.Stairs_Up


Rectangles = tuple[rdg.Rectangle, rdg.Rectangle, rdg.Rectangle, rdg.Rectangle]
@pytest.fixture
def rectangles() -> Rectangles:
    return (
        rdg.Rectangle(0, 0, 10, 5),
        rdg.Rectangle(0, 0, 10, 10),
        rdg.Rectangle(10, 10, -10, -10),
        rdg.Rectangle(20, 20, -10, 10),
    )

def test_rectangle(rectangles: Rectangles) -> None:
    r1, r2, r3, r4 = rectangles
    assert r1 == (0, 0, 10, 5)
    assert r2 == (0, 0, 10, 10)
    assert r3 == (1, 1, 11, 11)
    assert r4 == (11, 20, 21, 30)

TEST_DIMENSIONS = Dimensions(10, 10)

@pytest.fixture
def generator() -> RDG:
    level = Level(tiles=Table(TEST_DIMENSIONS))
    generator = RDG(level)
    generator.init_tiles()
    return generator

def test_dungeon_generation(rectangles: Rectangles, generator: RDG) -> None:
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
