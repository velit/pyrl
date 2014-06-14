from __future__ import absolute_import, division, print_function, unicode_literals

import string
import const.keys as KEY
import const.directions as DIR

# general
CANCEL = 'z'

GROUP_YES = {'y', 'Y'}
GROUP_NO = {'n', 'N'}
GROUP_CANCEL = {CANCEL, KEY.ESC}
GROUP_MORE = {KEY.ENTER, KEY.SPACE}
GROUP_DEFAULT = GROUP_CANCEL | GROUP_MORE
GROUP_ALL = GROUP_YES | GROUP_NO | GROUP_DEFAULT

DIRECTIONS = {
    '1': DIR.SW,
    '2': DIR.SO,
    '3': DIR.SE,
    '4': DIR.WE,
    '5': DIR.STOP,
    '6': DIR.EA,
    '7': DIR.NW,
    '8': DIR.NO,
    '9': DIR.NE,
    'h': DIR.WE,
    'j': DIR.SO,
    'k': DIR.NO,
    'l': DIR.EA,
    '.': DIR.STOP,
    'y': DIR.NW,
    'u': DIR.NE,
    'b': DIR.SW,
    'n': DIR.SE,
    KEY.NUMPAD_1: DIR.SW,
    KEY.NUMPAD_2: DIR.SO,
    KEY.NUMPAD_3: DIR.SE,
    KEY.NUMPAD_4: DIR.WE,
    KEY.NUMPAD_5: DIR.STOP,
    KEY.NUMPAD_6: DIR.EA,
    KEY.NUMPAD_7: DIR.NW,
    KEY.NUMPAD_8: DIR.NO,
    KEY.NUMPAD_9: DIR.NE,
}

INSTANT_WALK_MODE = {
    KEY.UP: DIR.NO,
    KEY.DOWN: DIR.SO,
    KEY.LEFT: DIR.WE,
    KEY.RIGHT: DIR.EA,
    KEY.END: DIR.SW,
    KEY.HOME: DIR.NW,
    KEY.PAGE_UP: DIR.NE,
    KEY.PAGE_DOWN: DIR.SE,
}

# main view
HELP = KEY.F1
LOOK_MODE = 'q'
INVENTORY = 'i'
DESCEND = 'X'
ASCEND = 'x'
QUIT = 'Q'
SAVE = 'S'
ATTACK = 'a'
REDRAW = '^r'
HISTORY = 'p'
WALK_MODE = 'w'

# inventory
VIEW_INVENTORY = 'v'

EQUIPMENT_SLOT_HEAD = 'h'
EQUIPMENT_SLOT_BODY = 'b'
EQUIPMENT_SLOT_RIGHT_HAND = 'r'
EQUIPMENT_SLOT_FEET = 'f'

INVENTORY_KEYS = tuple(letter for letter in string.ascii_lowercase if letter != CANCEL)
