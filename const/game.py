import const.generated_level_types as GENERATED_LEVEL_TYPE
from itertools import imap

OPTIMIZATION = True

MSG_BAR_SIZE = 2
STATUS_BAR_SIZE = 2

_n = 6

MIN_SCREEN_ROWS = 5 * _n
MIN_SCREEN_COLS = 16 * _n

LEVEL_ROWS = MIN_SCREEN_ROWS - MSG_BAR_SIZE - STATUS_BAR_SIZE
LEVEL_COLS = MIN_SCREEN_COLS

MOVEMENT_COST = 1000
ATTACK_COST = 1000
DIAGONAL_MODIFIER = 2 ** 0.5

LEVEL_TYPE = GENERATED_LEVEL_TYPE.DUNGEON

MONSTERS_PER_LEVEL = 100
LEVELS_PER_DUNGEON = 100

GAME_NAME = "pyrl"

ENCODING = "utf-8"

SET_LEVEL = "set-level"
NEXT_LEVEL = "next-level"
PREVIOUS_LEVEL = "previous-level"
UP = (PREVIOUS_LEVEL, None, None)
DOWN = (NEXT_LEVEL, None, None)

DUNGEON = "dungeon"
FIRST_LEVEL = (DUNGEON, 0)

PASSAGE_UP = "an exit going up"
PASSAGE_DOWN = "an exit going down"
PASSAGE_RANDOM = "random entry point"

YES = set(imap(ord, "yY"))
NO = set(imap(ord, "nN"))
DEFAULT = set(imap(ord, " zZ\n"))
YES_D = YES | DEFAULT
NO_D = NO | DEFAULT
ALL = YES | NO | DEFAULT
MOVES = set(imap(ord, "123456790."))

class PyrlException(Exception): pass
