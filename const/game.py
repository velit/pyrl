from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from os.path import join


OPTIMIZATION = True

MSG_BAR_HEIGHT = 2
STATUS_BAR_HEIGHT = 2

_N = 6

SCREEN_ROWS = 5 * _N
SCREEN_COLS = 16 * _N

LEVEL_HEIGHT = SCREEN_ROWS - MSG_BAR_HEIGHT - STATUS_BAR_HEIGHT
LEVEL_WIDTH = SCREEN_COLS

MOVEMENT_COST = 1000
ATTACK_COST = 1000
DIAGONAL_MODIFIER = 2 ** 0.5

MONSTERS_PER_LEVEL = 99
LEVELS_PER_DUNGEON = 99

# in seconds
ANIMATION_DELAY = 0.02
INPUT_INTERVAL = min(ANIMATION_DELAY / 10, 0.01)

GAME_NAME = "pyrl"
DATA_FOLDER = "data"
LOG_LEVEL = logging.DEBUG
LOG_FILE = join(DATA_FOLDER, "pyrl.log")
PROFILE_DATA_PATH = join(DATA_FOLDER, "profiling_results")
SAVE_FILE_COMPRESSION_LEVEL = 6  # valid in range(1, 10)

PASSAGE_UP = "up"
PASSAGE_DOWN = "down"
PASSAGE_RANDOM = "random"

NCURSES = "ncurses"
LIBTCOD = "libtcod"
