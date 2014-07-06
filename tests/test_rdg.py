from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

import rdg
from level_template import LevelTemplate


def pp_tm(tm, cols):
    """Pretty print tilemap."""
    for i, c in enumerate(tm):
        print(c, end=('' if i % cols != cols - 1 else '\n'))


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


@pytest.fixture
def generator():

    level_template = LevelTemplate(rows=10, cols=10)
    generator = rdg.RDG(level_template)
    generator.init_tilemap_template()
    return generator


def test_dungeon_generation(rectangles, generator):
    rect = rectangles[0]

    generator.attempt_room(rect, (0, 1))
    room = list(
        "w.wwwrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "wwwwwrrrrr"
    )
    assert generator.level_template.tilemap_template == room

    generator.attempt_corridor((4, 4), (0, 1), 6)
    room = list(
        "w.wwwrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wwwwww"
        "w........w"
        "w...wwwwww"
        "w...wrrrrr"
        "w...wrrrrr"
        "w...wrrrrr"
        "wwwwwrrrrr"
    )
    assert generator.level_template.tilemap_template == room
