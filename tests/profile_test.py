from cProfile import Profile

from pyrl.enums.level_gen import LevelGen
from pyrl.rdg import generate_tiles_to
from tools import profile_util
from pyrl.world.level import Level


def test_profile_rdg_generation():
    profiler = Profile()
    profiler.enable()

    for _ in range(5):
        level = Level(generation_type=LevelGen.Dungeon)
        generate_tiles_to(level)

    profiler.disable()
    profile_util.write_results_log(profiler)
