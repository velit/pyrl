import logging
from os.path import join

from pyrl.config.game import GameConf


class Debug(object):

    log_level = logging.DEBUG
    log_file = join(GameConf.save_folder, "pyrl.log")
    profiling_output_file = join(GameConf.save_folder, "profiling_results")
    path = True
    path_step = False
    cross = True
    cross_mod = 100
    show_map = False
    show_keycodes = False
    max_loop_cycles = 1000000
    debug_string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam varius massa enim, id fermentum erat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. In et enim ut nibh rutrum suscipit. Aenean a lacus eget justo dignissim tempus. Nunc venenatis congue erat vel adipiscing. Nam nulla felis, accumsan eu sagittis aliquet, fermentum at tortor. Suspendisse tortor risus, dapibus quis porta vel, mattis sit amet libero. Morbi vel metus eget metus ultricies ultrices placerat ac sapien. Lorem ipsum dolor sit amet, consectetur adipiscing elit.  Nulla urna erat, lacinia vitae pellentesque et, accumsan eget ante. Sed commodo molestie ipsum, a mattis sapien malesuada at. Integer et lorem magna. Sed nec erat orci. Donec id elementum elit. In hac habitasse platea dictumst. Duis id nisi ut felis convallis blandit id sit amet magna. Nam feugiat erat eget velit ullamcorper varius. Nunc tellus massa, fermentum eu aliquet non, fermentum a quam.  Pellentesque turpis erat, aliquam at feugiat in, congue nec urna. Nulla ut turpis dapibus metus blandit faucibus.  Suspendisse potenti. Proin facilisis massa vitae purus dignissim quis dapibus eros gravida. Vivamus ac sapien ante, ut euismod nunc. Pellentesque faucibus neque at tortor malesuada eu commodo nisl vehicula. Vivamus eu odio ut est egestas luctus. Duis orci magna, tincidunt id suscipit id, consectetur sodales nisl. Etiam justo lorem, molestie sit amet rutrum eget, consequat mattis magna.  Fusce eros est, tincidunt id consequat id, scelerisque ac sapien.  Donec lacus leo, adipiscing et vulputate in, pulvinar vitae sem. Suspendisse sem augue, adipiscing vitae tempor sit amet, egestas a neque. Donec nibh mauris, rutrum vitae dictum in, adipiscing in magna. Duis fringilla sem vel nisl tempus dignissim. Fusce vel felis ipsum. Sed risus ipsum, iaculis a mollis vel, viverra in nisi. Suspendisse est tellus, aliquet et vulputate vel, iaculis egestas nulla.  Praesent sed tortor sed neque varius consequat. Quisque interdum facilisis convallis. Aliquam eu nisi arcu. Proin convallis sagittis nisi id molestie. Aenean rutrum elementum mauris, vitae venenatis tellus semper et. Proin eu nisl ligula. Maecenas dui mi, varius eget adipiscing quis, commodo et libero."


def breakpoint():
    import curses
    curses.endwin()
    import pdb
    pdb.set_trace()
