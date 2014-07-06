from __future__ import absolute_import, division, print_function, unicode_literals

from cProfile import Profile

import profile_util
from tests import profiler_test


if __name__ == "__main__":

    profiler = Profile()
    profiler.enable()

    profiler_test.run_all()

    profiler.disable()
    profile_util.write_profiler_results(profiler)
