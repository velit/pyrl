from __future__ import annotations

from cProfile import Profile

from pyrl.game_data.levels.shared_assets import default_dims
from pyrl.world.world_types import LevelGen, LevelKey
from pyrl.world.level_gen_params import LevelGenParams
from tools import profile_util

def test_profile_rdg_generation() -> None:
    profiler = Profile()
    profiler.enable()

    for i in range(5):
        LevelGenParams(dimensions=default_dims, generation_type=LevelGen.Dungeon) \
            .create_level(LevelKey("test", i))

    profiler.disable()
    profile_util.write_results_log(profiler)
