import cProfile
import sys
from pstats import Stats

from pyrl.config.config import Config

def write_results_log(profiler: cProfile.Profile, filename: str) -> None:

    with open(Config.save_folder / filename, "w") as f:
        stats = Stats(profiler, stream=f)
        print_results(stats)

def print_results(stats: Stats) -> None:
    stats.strip_dirs()
    stats.sort_stats('calls').print_stats(10)
    stats.sort_stats('time').print_stats(15)
    stats.sort_stats('cumulative').print_stats(15)
    stats.sort_stats('module', 'nfl').print_stats()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        profile_data_file = sys.argv[1]
        print_results(Stats(profile_data_file))
    else:
        print("Profile data path required.")
