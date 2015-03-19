from __future__ import absolute_import, division, print_function, unicode_literals

import const.colors as COLOR
import const.game as GAME
import const.keys as KEY
from const.game import LIBTCOD


try:
    import libtcod.libtcodpy as libtcod
except Exception as e:
    import sys
    print("Couldn't load libtcod. Tried both 64-bit and 32-bit libs.", file=sys.stderr)
    print("It's possible this happens because libsdl isn't installed.", file=sys.stderr)
    sys.exit(1)


TCOD_COLOR = {
    COLOR.BASE_BLACK: libtcod.Color(0, 0, 0),
    COLOR.BASE_RED: libtcod.Color(175, 0, 0),
    COLOR.BASE_GREEN: libtcod.Color(0, 175, 0),
    COLOR.BASE_BLUE: libtcod.Color(0, 0, 175),
    COLOR.BASE_PURPLE: libtcod.Color(175, 0, 175),
    COLOR.BASE_CYAN: libtcod.Color(0, 175, 175),
    COLOR.BASE_YELLOW: libtcod.Color(255, 255, 95),
    COLOR.BASE_BROWN: libtcod.Color(150, 75, 0),

    COLOR.BASE_LIGHT_RED: libtcod.Color(255, 95, 95),
    COLOR.BASE_LIGHT_GREEN: libtcod.Color(95, 255, 95),
    COLOR.BASE_LIGHT_BLUE: libtcod.Color(95, 95, 255),
    COLOR.BASE_LIGHT_PURPLE: libtcod.Color(255, 95, 255),
    COLOR.BASE_LIGHT_CYAN: libtcod.Color(95, 255, 255),

    COLOR.BASE_WHITE: libtcod.Color(255, 255, 255),
    COLOR.BASE_LIGHT: libtcod.Color(218, 218, 218),
    COLOR.BASE_NORMAL: libtcod.Color(187, 187, 187),
    COLOR.BASE_LIGHT_GRAY: libtcod.Color(168, 168, 168),
    COLOR.BASE_GRAY: libtcod.Color(138, 138, 138),
    COLOR.BASE_DARK_GRAY: libtcod.Color(108, 108, 108),
    COLOR.BASE_DARK: libtcod.Color(78, 78, 78),
    COLOR.BASE_DARKER: libtcod.Color(48, 48, 48),
    COLOR.BASE_DARKEST: libtcod.Color(20, 20, 20),
    COLOR.BASE_BLACK: libtcod.Color(0, 0, 0),
}

TCOD_KEYS = {
    libtcod.KEY_ENTER: KEY.ENTER,
    libtcod.KEY_TAB: KEY.TAB,
    libtcod.KEY_ESCAPE: KEY.ESC,
    libtcod.KEY_SPACE: KEY.SPACE,
    libtcod.KEY_LEFT: KEY.LEFT,
    libtcod.KEY_RIGHT: KEY.RIGHT,
    libtcod.KEY_UP: KEY.UP,
    libtcod.KEY_DOWN: KEY.DOWN,
    libtcod.KEY_HOME: KEY.HOME,
    libtcod.KEY_END: KEY.END,
    libtcod.KEY_PAGEDOWN: KEY.PAGE_DOWN,
    libtcod.KEY_PAGEUP: KEY.PAGE_UP,
    libtcod.KEY_INSERT: KEY.INSERT,
    libtcod.KEY_DELETE: KEY.DELETE,
    libtcod.KEY_BACKSPACE: KEY.BACKSPACE,
    libtcod.KEY_F1: KEY.F1,
    libtcod.KEY_F2: KEY.F2,
    libtcod.KEY_F3: KEY.F3,
    libtcod.KEY_F4: KEY.F4,
    libtcod.KEY_F5: KEY.F5,
    libtcod.KEY_F6: KEY.F6,
    libtcod.KEY_F7: KEY.F7,
    libtcod.KEY_F8: KEY.F8,
    libtcod.KEY_F9: KEY.F9,
    libtcod.KEY_F10: KEY.F10,
    libtcod.KEY_F11: KEY.F11,
    libtcod.KEY_F12: KEY.F12,
    libtcod.KEY_KP0: KEY.NUMPAD_0,
    libtcod.KEY_KP1: KEY.NUMPAD_1,
    libtcod.KEY_KP2: KEY.NUMPAD_2,
    libtcod.KEY_KP3: KEY.NUMPAD_3,
    libtcod.KEY_KP4: KEY.NUMPAD_4,
    libtcod.KEY_KP5: KEY.NUMPAD_5,
    libtcod.KEY_KP6: KEY.NUMPAD_6,
    libtcod.KEY_KP7: KEY.NUMPAD_7,
    libtcod.KEY_KP8: KEY.NUMPAD_8,
    libtcod.KEY_KP9: KEY.NUMPAD_9,
    libtcod.KEY_NONE: KEY.NO_INPUT,
}
ROOT_WIN = None

DEFAULT_FG = libtcod.white
DEFAULT_BG = libtcod.black


def init(root_window):
    global ROOT_WIN
    libtcod.console_set_custom_font("data/terminal10x18_gs_ro.png",
                                    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(GAME.SCREEN_COLS, GAME.SCREEN_ROWS,
                              GAME.GAME_NAME, False, libtcod.RENDERER_SDL)


def _init_handle(handle):
    libtcod.console_set_default_foreground(handle, DEFAULT_FG)
    libtcod.console_set_default_background(handle, DEFAULT_BG)


def new_window(size):
    rows, columns = size
    handle = libtcod.console_new(columns, rows)
    _init_handle(handle)
    return handle


def flush():
    libtcod.console_flush()


def get_root_window():
    return ROOT_WIN


def suspend():
    pass


def resume():
    pass


def toggle_fullscreen():
    if libtcod.console_is_fullscreen():
        libtcod.console_set_fullscreen(False)
    else:
        libtcod.console_set_fullscreen(True)


def addch(handle, y, x, char):
    symbol, (fg, bg) = char
    libtcod.console_put_char_ex(handle, x, y, symbol.encode(GAME.ENCODING), TCOD_COLOR[fg], TCOD_COLOR[bg])


def addstr(handle, y, x, string, color=None):
    if color is None:
        libtcod.console_print(handle, x, y, string.encode(GAME.ENCODING))
    else:
        fg, bg = color
        libtcod.console_set_default_foreground(handle, TCOD_COLOR[fg])
        libtcod.console_set_default_background(handle, TCOD_COLOR[bg])
        libtcod.console_print(handle, x, y, string.encode(GAME.ENCODING))
        libtcod.console_set_default_foreground(handle, DEFAULT_FG)
        libtcod.console_set_default_background(handle, DEFAULT_BG)


def draw(handle, char_payload_sequence):
    f = libtcod.console_put_char_ex
    COLOR_LOOKUP = TCOD_COLOR
    for y, x, (symbol, (fg, bg)) in char_payload_sequence:
        f(handle, x, y, symbol.encode(GAME.ENCODING), COLOR_LOOKUP[fg], COLOR_LOOKUP[bg])


def draw_reverse(handle, char_payload_sequence):
    f = libtcod.console_put_char_ex
    COLOR_LOOKUP = TCOD_COLOR
    for y, x, (symbol, (fg, bg)) in char_payload_sequence:
        f(handle, x, y, symbol.encode(GAME.ENCODING), COLOR_LOOKUP[bg], COLOR_LOOKUP[fg])


def get_key(handle_not_used):
    while True:
        key_event = libtcod.Key()
        mouse_event = libtcod.Mouse()
        libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS, key_event, mouse_event, False)
        key = interpret_event(key_event)
        if key != KEY.NO_INPUT:
            return key


def check_key(handle_not_used):
    event = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)
    return interpret_event(event)


def interpret_event(event):
    if libtcod.console_is_window_closed():
        return KEY.CLOSE_WINDOW
    elif event.vk in TCOD_KEYS:
        return TCOD_KEYS[event.vk]
    elif event.vk == libtcod.KEY_CHAR:
        if event.c == ord('c') and event.lctrl or event.rctrl:
            raise KeyboardInterrupt
        ch = chr(event.c)
        if event.lctrl or event.rctrl:
            ch = "^" + ch
        if event.lalt or event.ralt:
            ch = "!" + ch
        return ch
    else:
        return KEY.NO_INPUT


def clear(handle):
    libtcod.console_clear(handle)


def blit(handle, size, screen_position):
    rows, cols = size
    y, x = screen_position
    libtcod.console_blit(handle, 0, 0, cols, rows, ROOT_WIN, x, y, 1.0, 1.0)


def get_dimensions(handle):
    return libtcod.console_get_height(handle), libtcod.console_get_width(handle)


def get_implementation():
    return LIBTCOD
