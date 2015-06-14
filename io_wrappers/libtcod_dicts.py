from __future__ import absolute_import, division, print_function, unicode_literals

from const.colors import Color
from const.keys import Key


try:
    import libtcod.libtcodpy as libtcod
except Exception as e:
    import sys
    print("Couldn't load libtcod. Tried both 64-bit and 32-bit libs.", file=sys.stderr)
    print("It's possible this happens because libsdl isn't installed.", file=sys.stderr)
    sys.exit(1)


libtcod_color_map = {
    Color.Red:           libtcod.Color(175, 0, 0),
    Color.Green:         libtcod.Color(0, 175, 0),
    Color.Blue:          libtcod.Color(0, 0, 175),
    Color.Purple:        libtcod.Color(175, 0, 175),
    Color.Cyan:          libtcod.Color(0, 175, 175),
    Color.Yellow:        libtcod.Color(255, 255, 95),
    Color.Brown:         libtcod.Color(150, 75, 0),
    Color.Dark_Blue:     libtcod.Color(0, 0, 175),
    Color.Dark_Brown:    libtcod.Color(135, 95, 0),
    Color.Light_Red:     libtcod.Color(255, 95, 95),
    Color.Light_Green:   libtcod.Color(95, 255, 95),
    Color.Light_Blue:    libtcod.Color(95, 95, 255),
    Color.Light_Purple:  libtcod.Color(255, 95, 255),
    Color.Light_Cyan:    libtcod.Color(95, 255, 255),
    Color.White:         libtcod.Color(255, 255, 255),
    Color.Light:         libtcod.Color(218, 218, 218),
    Color.Normal:        libtcod.Color(187, 187, 187),
    Color.Light_Gray:    libtcod.Color(168, 168, 168),
    Color.Gray:          libtcod.Color(138, 138, 138),
    Color.Dark_Gray:     libtcod.Color(108, 108, 108),
    Color.Dark:          libtcod.Color(78, 78, 78),
    Color.Darker:        libtcod.Color(48, 48, 48),
    Color.Darkest:       libtcod.Color(20, 20, 20),
    Color.Black:         libtcod.Color(0, 0, 0),
}

libtcod_key_map = {
    libtcod.KEY_BACKSPACE:  Key.BACKSPACE,
    libtcod.KEY_DELETE:     Key.DELETE,
    libtcod.KEY_DOWN:       Key.DOWN,
    libtcod.KEY_END:        Key.END,
    libtcod.KEY_ENTER:      Key.ENTER,
    libtcod.KEY_ESCAPE:     Key.ESC,
    libtcod.KEY_F1:         Key.F1,
    libtcod.KEY_F2:         Key.F2,
    libtcod.KEY_F3:         Key.F3,
    libtcod.KEY_F4:         Key.F4,
    libtcod.KEY_F5:         Key.F5,
    libtcod.KEY_F6:         Key.F6,
    libtcod.KEY_F7:         Key.F7,
    libtcod.KEY_F8:         Key.F8,
    libtcod.KEY_F9:         Key.F9,
    libtcod.KEY_F10:        Key.F10,
    libtcod.KEY_F11:        Key.F11,
    libtcod.KEY_F12:        Key.F12,
    libtcod.KEY_HOME:       Key.HOME,
    libtcod.KEY_INSERT:     Key.INSERT,
    libtcod.KEY_KP0:        Key.NUMPAD_0,
    libtcod.KEY_KP1:        Key.NUMPAD_1,
    libtcod.KEY_KP2:        Key.NUMPAD_2,
    libtcod.KEY_KP3:        Key.NUMPAD_3,
    libtcod.KEY_KP4:        Key.NUMPAD_4,
    libtcod.KEY_KP5:        Key.NUMPAD_5,
    libtcod.KEY_KP6:        Key.NUMPAD_6,
    libtcod.KEY_KP7:        Key.NUMPAD_7,
    libtcod.KEY_KP8:        Key.NUMPAD_8,
    libtcod.KEY_KP9:        Key.NUMPAD_9,
    libtcod.KEY_LEFT:       Key.LEFT,
    libtcod.KEY_NONE:       Key.NO_INPUT,
    libtcod.KEY_PAGEDOWN:   Key.PAGE_DOWN,
    libtcod.KEY_PAGEUP:     Key.PAGE_UP,
    libtcod.KEY_RIGHT:      Key.RIGHT,
    libtcod.KEY_SPACE:      Key.SPACE,
    libtcod.KEY_TAB:        Key.TAB,
    libtcod.KEY_UP:         Key.UP,
}
