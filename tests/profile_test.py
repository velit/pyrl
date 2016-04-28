from cProfile import Profile

from rdg import generate_tiles_to, LevelGen
from tools import profile_util
from world.level_template import LevelTemplate


def test_profile_rdg_generation():
    profiler = Profile()
    profiler.enable()

    for _ in range(5):
        lt = LevelTemplate(generation_type=LevelGen.Dungeon)
        generate_tiles_to(lt)

    profiler.disable()
    profile_util.write_results_log(profiler)
