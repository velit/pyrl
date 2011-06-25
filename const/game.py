OPTIMIZATION = True
DEBUG = False


MSG_BAR_SIZE = 2
STATUS_BAR_SIZE = 2

_n = 6

MAP_ROWS = 5*_n - MSG_BAR_SIZE - STATUS_BAR_SIZE
MAP_COLS = 16*_n

MORE_STR = " (more)"
ENCODING = "utf-8"

SET_LEVEL = "set-level"
NEXT_LEVEL = "next-level"
PREVIOUS_LEVEL = "previous-level"
UP = (PREVIOUS_LEVEL, )
DOWN = (NEXT_LEVEL, )

DUNGEON = "dungeon"

PASSAGE_UP = "an exit going up"
PASSAGE_DOWN = "an exit going down"
PASSAGE_RANDOM = "random entry point"

YES = set(map(ord, "yY"))
NO = set(map(ord, "nN"))
DEFAULT = set(map(ord, " \n"))
MOVES = set(map(ord, "123456790."))
