from __future__ import annotations

from collections.abc import Iterable
from dataclasses import astuple
from typing import Any

import pytest

from pyrl.algorithms.dungeon_generator import DungeonGenerator
from pyrl.game_data.levels.shared_assets import construct_data, DefaultLocation
from pyrl.game_data.pyrl_tiles import PyrlTiles
from pyrl.structures.dimensions import Dimensions
from pyrl.structures.rectangle import Rectangle
from pyrl.structures.table import Table
from pyrl.types.level_gen import LevelGen
from pyrl.types.level_key import LevelKey
from pyrl.world.level_gen_params import LevelGenParams

def pp_tm(tile_matrix: Iterable[Any], cols: int) -> None:
    """Pretty print tiles."""
    for i, char in enumerate(tile_matrix):
        print(char, end=('' if i % cols != cols - 1 else '\n'))

@pytest.mark.slow
def test_many_rdg_generation() -> None:
    for idx in range(100):
        level = LevelGenParams(generation_type=LevelGen.Dungeon).create_level(LevelKey("test", idx))
        assert level.tiles[level.locations.getkey(DefaultLocation.Passage_Down)] == PyrlTiles.Stairs_Down
        assert level.tiles[level.locations.getkey(DefaultLocation.Passage_Up)] == PyrlTiles.Stairs_Up

def test_rdg_generation() -> None:
    level = LevelGenParams(generation_type=LevelGen.Dungeon).create_level(LevelKey("test", 0))
    assert level.tiles[level.locations.getkey(DefaultLocation.Passage_Down)] == PyrlTiles.Stairs_Down
    assert level.tiles[level.locations.getkey(DefaultLocation.Passage_Up)] == PyrlTiles.Stairs_Up


Rectangles = tuple[Rectangle, Rectangle, Rectangle, Rectangle]
@pytest.fixture
def rectangles() -> Rectangles:
    return (
        Rectangle((0,  0),  Dimensions(10,  5)),
        Rectangle((0,  0),  Dimensions(10,  10)),
        Rectangle((10, 10), Dimensions(-10, -10)),
        Rectangle((20, 20), Dimensions(-10, 10)),
    )

def test_rectangle(rectangles: Rectangles) -> None:
    r1, r2, r3, r4 = rectangles
    assert astuple(r1) == (range(0, 10),  range(0, 5),   (10, 5))
    assert astuple(r2) == (range(0, 10),  range(0, 10),  (10, 10))
    assert astuple(r3) == (range(1, 11),  range(1, 11),  (10, 10))
    assert astuple(r4) == (range(11, 21), range(20, 30), (10, 10))

TEST_DIMENSIONS = Dimensions(10, 10)

@pytest.fixture
def generator() -> DungeonGenerator:
    level_params = LevelGenParams(tiles=Table(TEST_DIMENSIONS))
    generator = DungeonGenerator(level_params)
    generator.init_tiles()
    return generator

def test_dungeon_generation(rectangles: Rectangles, generator: DungeonGenerator) -> None:
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
    assert generator.level_params.tiles == room

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
    assert generator.level_params.tiles == room
