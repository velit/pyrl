from __future__ import absolute_import, division, print_function, unicode_literals

from config.finalize import finalize_bindings
from enums.keys import Key


@finalize_bindings
class Bind(object):

    """
    Modify this class to define the mappings you want.

    For multiple bindings for the same action, write a comma separated list:
        Cancel = 'z', Key.ESC
    The first binding in a list is used for printing the key in menus.
    If you wish to unbind a key, insert () instead of a key string.

    Special key names:

    Key.LEFT, Key.RIGHT, Key.UP, Key.DOWN, Key.ESC, Key.TAB, Key.SHIFT_TAB, Key.BACKSPACE,
    Key.SPACE, Key.ENTER, Key.INSERT, Key.DELETE, Key.HOME, Key.END, Key.PAGE_UP, Key.PAGE_DOWN
    Key.F1 - Key.F12
    Key.NUMPAD_0 - Key.NUMPAD_9 #  mostly for sdl version of the game

    For other keys use a string representing that character. To use shift just write the
    character that comes out of the shift combination directly (eg. Q or #). For alt/meta
    prepend a ! character and for ctrl prepend a ^ character. Some rules:
        -If you use ^ use lower case letters for it to work (eg. ^D or ^N).
        -If you use both ! and ^ in the same bind put ! before ^ for it to work.
        -Modifiers do not work with special keys.
    """

    # General
    Cancel = 'z', Key.SPACE, Key.ESC

    # Debug
    Debug_Commands = 'd'

    # Full message bar
    Last_Message = Key.ENTER

    # Scrollable views
    Next_Line     = '+', '^n'
    Previous_Line = '-', '^p'
    Next_Page     = Key.PAGE_DOWN, '^d'
    Previous_Page = Key.PAGE_UP, '^u'

    # Multi-select views
    Select_All   = '^a'
    Deselect_All = '^e'

    # Directions used in moving/attacking/targetting
    SouthWest = '1', 'm', Key.NUMPAD_1, Key.END
    South     = '2', ',', Key.NUMPAD_2, Key.DOWN
    SouthEast = '3', '.', Key.NUMPAD_3, Key.PAGE_DOWN
    West      = '4', 'j', Key.NUMPAD_4, Key.LEFT
    Stay      = '5', 'k', Key.NUMPAD_5
    East      = '6', 'l', Key.NUMPAD_6, Key.RIGHT
    NorthWest = '7', 'u', Key.NUMPAD_7, Key.HOME
    North     = '8', 'i', Key.NUMPAD_8, Key.UP
    NorthEast = '9', 'o', Key.NUMPAD_9, Key.PAGE_UP

    # Initiates walk mode into direction
    Instant_SouthWest = ()  # Key.END
    Instant_South     = ()  # Key.DOWN
    Instant_SouthEast = ()  # Key.PAGE_DOWN
    Instant_West      = ()  # Key.LEFT
    Instant_Stay      = ()
    Instant_East      = ()  # Key.RIGHT
    Instant_NorthWest = ()  # Key.HOME
    Instant_North     = ()  # Key.UP
    Instant_NorthEast = ()  # Key.PAGE_UP

    # Main view
    Help          = Key.F1, Key.F2
    Look_Mode     = 'q'
    Equipment     = 'e'
    Backpack      = 'b'
    Drop_Items    = '^d'
    Pick_Up_Items = 'p'
    Descend       = 'X'
    Ascend        = 'x'
    Quit          = 'Q'
    Save          = 'S'
    Attack        = 'a'
    Redraw        = '^r'
    History       = 'p'
    Walk_Mode     = 'w'
    Show_Vision   = 'H'

    # Equipment View           Head  Body  RightHand  LeftHand  Feet
    Equipment_Select_Keys   = 'h',  'b',  'r',       'l',      'f'
    Equipment_View_Backpack = 'v'

    # Backpack View

    # This is the same as doing Item_Select_Keys = 'a', 'b', 'c' ...
    # But it wont work if you want modifiers like ^ or !.
    # You have to write the whole thing out then.
    Backpack_Select_Keys = tuple('abcdefghijklmnopqrstuvwxy')
    Backpack_Drop_Items = '^d'

    # Queries
    Yes = 'y'
    No = 'n'
    Default_Yes = 'Y'
    Default_No = 'N'
    Default_Query = Key.ENTER
