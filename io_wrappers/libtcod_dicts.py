from __future__ import absolute_import, division, print_function, unicode_literals

import const.keys as KEY
import const.colors as COLOR


try:
    import libtcod.libtcodpy as libtcod
except Exception as e:
    import sys
    print("Couldn't load libtcod. Tried both 64-bit and 32-bit libs.", file=sys.stderr)
    print("It's possible this happens because libsdl isn't installed.", file=sys.stderr)
    sys.exit(1)


libtcod_color_map = {

    COLOR.BASE_RED:           libtcod.Color(175, 0, 0),
    COLOR.BASE_GREEN:         libtcod.Color(0, 175, 0),
    COLOR.BASE_BLUE:          libtcod.Color(0, 0, 175),
    COLOR.BASE_PURPLE:        libtcod.Color(175, 0, 175),
    COLOR.BASE_CYAN:          libtcod.Color(0, 175, 175),
    COLOR.BASE_YELLOW:        libtcod.Color(255, 255, 95),
    COLOR.BASE_BROWN:         libtcod.Color(150, 75, 0),
    COLOR.BASE_DARK_BLUE:     libtcod.Color(0, 0, 175),
    COLOR.BASE_DARK_BROWN:    libtcod.Color(135, 95, 0),
    COLOR.BASE_LIGHT_RED:     libtcod.Color(255, 95, 95),
    COLOR.BASE_LIGHT_GREEN:   libtcod.Color(95, 255, 95),
    COLOR.BASE_LIGHT_BLUE:    libtcod.Color(95, 95, 255),
    COLOR.BASE_LIGHT_PURPLE:  libtcod.Color(255, 95, 255),
    COLOR.BASE_LIGHT_CYAN:    libtcod.Color(95, 255, 255),
    COLOR.BASE_WHITE:         libtcod.Color(255, 255, 255),
    COLOR.BASE_LIGHT:         libtcod.Color(218, 218, 218),
    COLOR.BASE_NORMAL:        libtcod.Color(187, 187, 187),
    COLOR.BASE_LIGHT_GRAY:    libtcod.Color(168, 168, 168),
    COLOR.BASE_GRAY:          libtcod.Color(138, 138, 138),
    COLOR.BASE_DARK_GRAY:     libtcod.Color(108, 108, 108),
    COLOR.BASE_DARK:          libtcod.Color(78, 78, 78),
    COLOR.BASE_DARKER:        libtcod.Color(48, 48, 48),
    COLOR.BASE_DARKEST:       libtcod.Color(20, 20, 20),
    COLOR.BASE_BLACK:         libtcod.Color(0, 0, 0),
}

libtcod_key_map = {
    libtcod.KEY_BACKSPACE:  KEY.BACKSPACE,
    libtcod.KEY_DELETE:     KEY.DELETE,
    libtcod.KEY_DOWN:       KEY.DOWN,
    libtcod.KEY_END:        KEY.END,
    libtcod.KEY_ENTER:      KEY.ENTER,
    libtcod.KEY_ESCAPE:     KEY.ESC,
    libtcod.KEY_F1:         KEY.F1,
    libtcod.KEY_F2:         KEY.F2,
    libtcod.KEY_F3:         KEY.F3,
    libtcod.KEY_F4:         KEY.F4,
    libtcod.KEY_F5:         KEY.F5,
    libtcod.KEY_F6:         KEY.F6,
    libtcod.KEY_F7:         KEY.F7,
    libtcod.KEY_F8:         KEY.F8,
    libtcod.KEY_F9:         KEY.F9,
    libtcod.KEY_F10:        KEY.F10,
    libtcod.KEY_F11:        KEY.F11,
    libtcod.KEY_F12:        KEY.F12,
    libtcod.KEY_HOME:       KEY.HOME,
    libtcod.KEY_INSERT:     KEY.INSERT,
    libtcod.KEY_KP0:        KEY.NUMPAD_0,
    libtcod.KEY_KP1:        KEY.NUMPAD_1,
    libtcod.KEY_KP2:        KEY.NUMPAD_2,
    libtcod.KEY_KP3:        KEY.NUMPAD_3,
    libtcod.KEY_KP4:        KEY.NUMPAD_4,
    libtcod.KEY_KP5:        KEY.NUMPAD_5,
    libtcod.KEY_KP6:        KEY.NUMPAD_6,
    libtcod.KEY_KP7:        KEY.NUMPAD_7,
    libtcod.KEY_KP8:        KEY.NUMPAD_8,
    libtcod.KEY_KP9:        KEY.NUMPAD_9,
    libtcod.KEY_LEFT:       KEY.LEFT,
    libtcod.KEY_NONE:       KEY.NO_INPUT,
    libtcod.KEY_PAGEDOWN:   KEY.PAGE_DOWN,
    libtcod.KEY_PAGEUP:     KEY.PAGE_UP,
    libtcod.KEY_RIGHT:      KEY.RIGHT,
    libtcod.KEY_SPACE:      KEY.SPACE,
    libtcod.KEY_TAB:        KEY.TAB,
    libtcod.KEY_UP:         KEY.UP,
}
