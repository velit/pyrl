from __future__ import absolute_import, division, print_function, unicode_literals

from .finalize import finalize_bindings
from enums.keys import Key


@finalize_bindings
class Bind(object):

    """
    Modify this class to define the mappings you want.

    For multiple bindings for the same action, write a comma separated list:
        Cancel = 'z', Key.ESC
    The first binding in a list is used for printing the key in menus.

    Special key names:

    Key.LEFT, Key.RIGHT, Key.UP, Key.DOWN, Key.ESC, Key.TAB, Key.BACKSPACE, Key.SPACE,
    Key.ENTER, Key.INSERT, Key.DELETE, Key.HOME, Key.END, Key.PAGE_UP, Key.PAGE_DOWN
    Key.F1 - Key.F12
    Key.NUMPAD_0 - Key.NUMPAD_9

    For other keys use a string representing that character. To use shift just write the
    character that comes out of the shift combination directly (eg. Q or #). For alt/meta
    prepend a ! character and for ctrl prepend a ^ character. Some rules:
        -If you use ^ use lower case letters for it to work (eg. ^d or ^n).
        -If you use both ! and ^ in the same bind put ! before ^ for it to work.
        -Modifiers do not work with special keys.
    """

    # general
    Cancel = 'z', Key.SPACE, Key.ESC

    # full message bar
    Last_Message = Key.ENTER

    # scrollable views
    Next_Line     = '^n'
    Previous_Line = '^p'
    Next_Page     = '^d'
    Previous_Page = '^u'

    # Directions used in moving/attacking/targetting
    SouthWest = '1', 'n'
    South     = '2', 'j'
    SouthEast = '3', 'm'
    West      = '4', 'h'
    Stay      = '5', '.'
    East      = '6', 'l'
    NorthWest = '7', 'u'
    North     = '8', 'k'
    NorthEast = '9', 'o'

    # Initiates walk mode into direction
    Instant_SouthWest = Key.END
    Instant_South     = Key.DOWN
    Instant_SouthEast = Key.PAGE_DOWN
    Instant_West      = Key.LEFT
    Instant_Stay      = Key.NUMPAD_5
    Instant_East      = Key.RIGHT
    Instant_NorthWest = Key.HOME
    Instant_North     = Key.UP
    Instant_NorthEast = Key.PAGE_UP

    # queries
    Yes = 'y'
    No = 'n'
    Default_Yes = 'Y'
    Default_No = 'N'
    Default_Query = Key.ENTER
    # The way these work is for example:
    #   "Quit the game? [Yes/Default_No]
    #       or
    #   "Save the game? [Default_Yes/No]
    # Default_Query executes the default action.
    # Pressing Yes/Default_Yes will execute yes and vice versa with No/Default_No

    # main view
    Help      = Key.F1, Key.F2
    Look_Mode = 'q'
    Inventory = 'i'
    Descend   = 'X'
    Ascend    = 'x'
    Quit      = 'Q'
    Save      = 'S'
    Attack    = 'a'
    Redraw    = '^r'
    History   = 'p'
    Walk_Mode = 'w'

    # inventory
    View_Inventory            = 'v'
    Equipment_Slot_Head       = 'h'
    Equipment_Slot_Body       = 'b'
    Equipment_Slot_Right_Hand = 'r'
    Equipment_Slot_Left_Hand  = 'l'
    Equipment_Slot_Feet       = 'f'
