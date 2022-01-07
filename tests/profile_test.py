from __future__ import annotations

from cProfile import Profile

from pyrl.types.level_gen import LevelGen
from pyrl.types.level_key import LevelKey
from pyrl.world.level_gen_params import LevelGenParams
from tools import profile_util

def test_profile_rdg_generation() -> None:
    profiler = Profile()
    profiler.enable()

    for i in range(5):
        LevelGenParams(generation_type=LevelGen.Dungeon)\
            .create_level(LevelKey("test", i))

    profiler.disable()
    profile_util.write_results_log(profiler)
