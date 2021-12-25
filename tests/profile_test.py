from __future__ import annotations

from cProfile import Profile

from pyrl.types.level_gen import LevelGen
from pyrl.dungeon_generation.rdg import generate_tiles_to
from tools import profile_util
from pyrl.world.level import Level

def test_profile_rdg_generation() -> None:
    profiler = Profile()
    profiler.enable()

    for _ in range(5):
        level = Level(generation_type=LevelGen.Dungeon)
        generate_tiles_to(level)

    profiler.disable()
    profile_util.write_results_log(profiler)
