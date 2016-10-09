from cProfile import Profile

from enums.level_gen import LevelGen
from rdg import generate_tiles_to
from tools import profile_util
from world.level import Level


def test_profile_rdg_generation():
    profiler = Profile()
    profiler.enable()

    for _ in range(5):
        level = Level(generation_type=LevelGen.Dungeon)
        generate_tiles_to(level)

    profiler.disable()
    profile_util.write_results_log(profiler)
