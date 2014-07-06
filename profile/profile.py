from __future__ import absolute_import, division, print_function

from cProfile import Profile
from pstats import Stats

from level_template import LevelTemplate
from rdg import generate_tilemap_template


def test_rdg_generation():

    for _ in range(250):
        lt = LevelTemplate()
        generate_tilemap_template(lt)


if __name__ == "__main__":

    pr = Profile()
    pr.enable()

    test_rdg_generation()

    pr.disable()

    with open("profiling_results", "w") as f:
        st = Stats(pr, stream=f)
        st.strip_dirs()

        st.sort_stats('calls').print_stats(10)
        st.sort_stats('time').print_stats(15)
        st.sort_stats('cumulative').print_stats(15)
        st.sort_stats('module', 'nfl').print_stats()
