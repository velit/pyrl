from const.generated_level_types import DUNGEON as LEVEL_TYPE_DUNGEON, ARENA as LEVEL_TYPE_ARENA

OPTIMIZATION = True

MSG_BAR_SIZE = 2
STATUS_BAR_SIZE = 2

_n = 6

MIN_SCREEN_ROWS = 5 * _n
MIN_SCREEN_COLS = 16 * _n

LEVEL_ROWS = MIN_SCREEN_ROWS - MSG_BAR_SIZE - STATUS_BAR_SIZE
LEVEL_COLS = MIN_SCREEN_COLS

MOVEMENT_COST = 1000

LEVEL_TYPE = "dungeon"

MONSTERS_PER_LEVEL = 100
LEVELS_PER_DUNGEON = 100

MORE_STR = " (more)"
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

YES = set(map(ord, "yY"))
NO = set(map(ord, "nN"))
DEFAULT = set(map(ord, " zZ\n"))
YES_D = YES | DEFAULT
NO_D = NO | DEFAULT
ALL = YES | NO | DEFAULT
MOVES = set(map(ord, "123456790."))

class PyrlException(Exception): pass
