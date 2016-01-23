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
    If you wish to unbind a key, use the Key.NONE special key.

    Special key names:

    Key.LEFT, Key.RIGHT, Key.UP, Key.DOWN, Key.ESC, Key.TAB, Key.SHIFT_TAB, Key.BACKSPACE,
    Key.SPACE, Key.ENTER, Key.INSERT, Key.DELETE, Key.HOME, Key.END, Key.PAGE_UP, Key.PAGE_DOWN
    Key.F1 - Key.F12
    Key.NUMPAD_0 - Key.NUMPAD_9 #  mostly for sdl version of the game
    Key.NONE #  use this to unbind a key

    For other keys use a string representing that character. To use shift just write the
    character that comes out of the shift combination directly (eg. Q or #). For alt/meta
    prepend a ! character and for ctrl prepend a ^ character. Some rules:
        -If you use ^ use lower case letters for it to work (eg. ^D or ^N).
        -If you use both ! and ^ in the same bind put ! before ^ for it to work.
        -Modifiers do not work with special keys.
    """

    # General
    Cancel = 'z', Key.SPACE, Key.ESC

    # Full message bar
    Last_Message = Key.ENTER

    # Scrollable views
    Next_Line     = '+', '^n'
    Previous_Line = '-', '^p'
    Next_Page     = Key.PAGE_DOWN, '^d'
    Previous_Page = Key.PAGE_UP, '^u'

    # This is the same as doing Item_Select_Keys = 'a', 'b', 'c' ...
    # But it wont work if you want modifiers like ^ or !.
    # You have to write the whole thing out then.
    Item_Select_Keys = tuple('abcdefghijklmnopqrstuvwxy')

    # Directions used in moving/attacking/targetting
    SouthWest = '1', 'm', Key.NUMPAD_1, Key.END
    South     = '2', ',', Key.NUMPAD_2, Key.DOWN
    SouthEast = '3', '.', Key.NUMPAD_3, Key.PAGE_DOWN
    West      = '4', 'j', Key.NUMPAD_4, Key.LEFT
    Stay      = '5', 'k', Key.NUMPAD_5, Key.NONE
    East      = '6', 'l', Key.NUMPAD_6, Key.RIGHT
    NorthWest = '7', 'u', Key.NUMPAD_7, Key.HOME
    North     = '8', 'i', Key.NUMPAD_8, Key.UP
    NorthEast = '9', 'o', Key.NUMPAD_9, Key.PAGE_UP

    # Initiates walk mode into direction
    Instant_SouthWest = Key.NONE  # Key.END
    Instant_South     = Key.NONE  # Key.DOWN
    Instant_SouthEast = Key.NONE  # Key.PAGE_DOWN
    Instant_West      = Key.NONE  # Key.LEFT
    Instant_Stay      = Key.NONE  # Key.NONE
    Instant_East      = Key.NONE  # Key.RIGHT
    Instant_NorthWest = Key.NONE  # Key.HOME
    Instant_North     = Key.NONE  # Key.UP
    Instant_NorthEast = Key.NONE  # Key.PAGE_UP

    # Main view
    Help        = Key.F1, Key.F2
    Look_Mode   = 'q'
    Equipment   = 'e'
    Backpack    = 'b'
    Descend     = 'X'
    Ascend      = 'x'
    Quit        = 'Q'
    Save        = 'S'
    Attack      = 'a'
    Redraw      = '^r'
    History     = 'p'
    Walk_Mode   = 'w'
    Show_Vision = 'H'

    # Inventory
    View_Inventory            = '^b'
    View_Equipment            = '^e'
    Equipment_Slot_Head       = 'h'
    Equipment_Slot_Body       = 'b'
    Equipment_Slot_Right_Hand = 'r'
    Equipment_Slot_Left_Hand  = 'l'
    Equipment_Slot_Feet       = 'f'

    # Queries
    Yes = 'y'
    No = 'n'
    Default_Yes = 'Y'
    Default_No = 'N'
    Default_Query = Key.ENTER
