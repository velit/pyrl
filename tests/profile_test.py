from __future__ import absolute_import, division, print_function, unicode_literals

from cProfile import Profile
import pytest

from level_template import LevelTemplate
from rdg import generate_tilemap, GenLevelType
from tools import profile_util


@pytest.mark.slow
def test_rdg_generation():
    profiler = Profile()
    profiler.enable()

    for _ in range(300):
        lt = LevelTemplate()
        generate_tilemap(lt, GenLevelType.Arena)

    profiler.disable()
    profile_util.write_results_log(profiler)
