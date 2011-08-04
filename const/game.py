OPTIMIZATION = True
DEBUG = False


MSG_BAR_SIZE = 2
STATUS_BAR_SIZE = 2

_n = 6

LEVEL_ROWS = 5*_n - MSG_BAR_SIZE - STATUS_BAR_SIZE
LEVEL_COLS = 16*_n

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
DEFAULT = set(map(ord, " \n"))
MOVES = set(map(ord, "123456790."))

class PyrlException(Exception): pass
