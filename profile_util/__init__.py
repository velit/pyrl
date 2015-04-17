from __future__ import absolute_import, division, print_function, unicode_literals

from pstats import Stats

from config.debug import Debug


def write_profiler_results(profiler):

    with open(Debug.profiling_output_file, "w") as f:
        st = Stats(profiler, stream=f)
        st.strip_dirs()

        st.sort_stats('calls').print_stats(10)
        st.sort_stats('time').print_stats(15)
        st.sort_stats('cumulative').print_stats(15)
        st.sort_stats('module', 'nfl').print_stats()
