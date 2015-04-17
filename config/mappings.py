from __future__ import absolute_import, division, print_function, unicode_literals

import string

from enums.directions import Dir
from enums.keys import Key


class Mapping(object):

    """
    Modify this class to define the mappings you want.

    Check enums/keys.py to see the names of special keys. For other keys use a string
    representing that character. Character keys can also have a modifier before the
    character. ^ means ctrl and ! means alt. Shift is achieved just by uppercasing the
    letter.
    """

    # general
    Cancel = 'z'

    Group_Yes = {'y', 'Y'}
    Group_No = {'n', 'N'}
    Group_Cancel = {Cancel, Key.ESC}
    Group_More = {Key.ENTER, Key.SPACE}
    Group_Default = Group_Cancel | Group_More
    Group_All = Group_Yes | Group_No | Group_Default

    Directions = {
        '1': Dir.SouthWest,
        '2': Dir.South,
        '3': Dir.SouthEast,
        '4': Dir.West,
        '5': Dir.Stay,
        '6': Dir.East,
        '7': Dir.NorthWest,
        '8': Dir.North,
        '9': Dir.NorthEast,
        'h': Dir.West,
        'j': Dir.South,
        'k': Dir.North,
        'l': Dir.East,
        '.': Dir.Stay,
        'u': Dir.NorthWest,
        'o': Dir.NorthEast,
        'n': Dir.SouthWest,
        'm': Dir.SouthEast,
        Key.NUMPAD_1: Dir.SouthWest,
        Key.NUMPAD_2: Dir.South,
        Key.NUMPAD_3: Dir.SouthEast,
        Key.NUMPAD_4: Dir.West,
        Key.NUMPAD_5: Dir.Stay,
        Key.NUMPAD_6: Dir.East,
        Key.NUMPAD_7: Dir.NorthWest,
        Key.NUMPAD_8: Dir.North,
        Key.NUMPAD_9: Dir.NorthEast,
    }

    Instant_Walk_Mode = {
        Key.UP: Dir.North,
        Key.DOWN: Dir.South,
        Key.LEFT: Dir.West,
        Key.RIGHT: Dir.East,
        Key.END: Dir.SouthWest,
        Key.HOME: Dir.NorthWest,
        Key.PAGE_UP: Dir.NorthEast,
        Key.PAGE_DOWN: Dir.SouthEast,
    }

    # main view
    Help = Key.F1
    Look_Mode = 'q'
    Inventory = 'i'
    Descend = 'X'
    Ascend = 'x'
    Quit = 'Q'
    Save = 'S'
    Attack = 'a'
    Redraw = '^r'
    History = 'p'
    Walk_Mode = 'w'

    # inventory
    View_Inventory = 'v'
    Equipment_Slot_Head = 'h'
    Equipment_Slot_Body = 'b'
    Equipment_Slot_Right_Hand = 'r'
    Equipment_Slot_Left_Hand = 'l'
    Equipment_Slot_Feet = 'f'

    Inventory_Keys = tuple(string.ascii_lowercase.replace(Cancel, ''))
