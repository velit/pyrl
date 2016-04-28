import pytest

import rdg
from game_data.levels.shared_assets import construct_data
from game_data.tiles import PyrlTile
from generic_structures import Array2D
from world.level import LevelLocation
from world.level_template import LevelTemplate


def pp_tm(tm, cols):
    """Pretty print tiles."""
    for i, c in enumerate(tm):
        print(c, end=('' if i % cols != cols - 1 else '\n'))


@pytest.mark.slow
def test_many_rdg_generation():
    for _ in range(100):
        lt = LevelTemplate(generation_type=rdg.LevelGen.Dungeon)
        rdg.generate_tiles_to(lt)
        lt.tiles[lt.locations.getkey(LevelLocation.Passage_Down)] == PyrlTile.Stairs_Down
        lt.tiles[lt.locations.getkey(LevelLocation.Passage_Down)] == PyrlTile.Stairs_Up


def test_rdg_generation():
    lt = LevelTemplate(generation_type=rdg.LevelGen.Dungeon)
    rdg.generate_tiles_to(lt)
    lt.tiles[lt.locations.getkey(LevelLocation.Passage_Down)] == PyrlTile.Stairs_Down
    lt.tiles[lt.locations.getkey(LevelLocation.Passage_Down)] == PyrlTile.Stairs_Up


@pytest.fixture
def rectangles():
    return (
        rdg.Rectangle(0, 0, 10, 5),
        rdg.Rectangle(0, 0, 10, 10),
        rdg.Rectangle(10, 10, -10, -10),
        rdg.Rectangle(20, 20, -10, 10),
    )


def test_Rectangle(rectangles):
    r1, r2, r3, r4 = rectangles
    assert r1 == (0, 0, 10, 5)
    assert r2 == (0, 0, 10, 10)
    assert r3 == (1, 1, 11, 11)
    assert r4 == (11, 20, 21, 30)


TEST_DIMENSIONS = (10, 10)


@pytest.fixture
def generator():

    level_template = LevelTemplate(tiles=Array2D(TEST_DIMENSIONS))
    generator = rdg.RDG(level_template)
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
    assert generator.level_template.tiles == room

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
    assert generator.level_template.tiles == room
