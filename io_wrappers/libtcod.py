from __future__ import absolute_import, division, print_function, unicode_literals

import locale
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


C, lC = COLOR, libtcod.Color
color_map = {

    C.BASE_RED: lC(175, 0, 0),              C.BASE_GREEN: lC(0, 175, 0),
    C.BASE_BLUE: lC(0, 0, 175),

    C.BASE_PURPLE: lC(175, 0, 175),         C.BASE_CYAN: lC(0, 175, 175),
    C.BASE_YELLOW: lC(255, 255, 95),        C.BASE_BROWN: lC(150, 75, 0),

    C.BASE_DARK_BLUE: lC(0, 0, 175),        C.BASE_DARK_BROWN: lC(135, 95, 0),

    C.BASE_LIGHT_RED: lC(255, 95, 95),      C.BASE_LIGHT_GREEN: lC(95, 255, 95),
    C.BASE_LIGHT_BLUE: lC(95, 95, 255),

    C.BASE_LIGHT_PURPLE: lC(255, 95, 255),  C.BASE_LIGHT_CYAN: lC(95, 255, 255),

    C.BASE_WHITE: lC(255, 255, 255),        C.BASE_LIGHT: lC(218, 218, 218),
    C.BASE_NORMAL: lC(187, 187, 187),       C.BASE_LIGHT_GRAY: lC(168, 168, 168),
    C.BASE_GRAY: lC(138, 138, 138),         C.BASE_DARK_GRAY: lC(108, 108, 108),
    C.BASE_DARK: lC(78, 78, 78),            C.BASE_DARKER: lC(48, 48, 48),
    C.BASE_DARKEST: lC(20, 20, 20),         C.BASE_BLACK: lC(0, 0, 0),
}
del C, lC

key_map = {
    libtcod.KEY_ENTER: KEY.ENTER,          libtcod.KEY_TAB: KEY.TAB,
    libtcod.KEY_ESCAPE: KEY.ESC,           libtcod.KEY_SPACE: KEY.SPACE,
    libtcod.KEY_LEFT: KEY.LEFT,            libtcod.KEY_RIGHT: KEY.RIGHT,
    libtcod.KEY_UP: KEY.UP,                libtcod.KEY_DOWN: KEY.DOWN,
    libtcod.KEY_HOME: KEY.HOME,            libtcod.KEY_END: KEY.END,
    libtcod.KEY_PAGEDOWN: KEY.PAGE_DOWN,   libtcod.KEY_PAGEUP: KEY.PAGE_UP,
    libtcod.KEY_INSERT: KEY.INSERT,        libtcod.KEY_DELETE: KEY.DELETE,
    libtcod.KEY_BACKSPACE: KEY.BACKSPACE,  libtcod.KEY_F1: KEY.F1,
    libtcod.KEY_F2: KEY.F2,                libtcod.KEY_F3: KEY.F3,
    libtcod.KEY_F4: KEY.F4,                libtcod.KEY_F5: KEY.F5,
    libtcod.KEY_F6: KEY.F6,                libtcod.KEY_F7: KEY.F7,
    libtcod.KEY_F8: KEY.F8,                libtcod.KEY_F9: KEY.F9,
    libtcod.KEY_F10: KEY.F10,              libtcod.KEY_F11: KEY.F11,
    libtcod.KEY_F12: KEY.F12,              libtcod.KEY_KP0: KEY.NUMPAD_0,
    libtcod.KEY_KP1: KEY.NUMPAD_1,         libtcod.KEY_KP2: KEY.NUMPAD_2,
    libtcod.KEY_KP3: KEY.NUMPAD_3,         libtcod.KEY_KP4: KEY.NUMPAD_4,
    libtcod.KEY_KP5: KEY.NUMPAD_5,         libtcod.KEY_KP6: KEY.NUMPAD_6,
    libtcod.KEY_KP7: KEY.NUMPAD_7,         libtcod.KEY_KP8: KEY.NUMPAD_8,
    libtcod.KEY_KP9: KEY.NUMPAD_9,         libtcod.KEY_NONE: KEY.NO_INPUT,
}


class LibTCODWrapper(object):

    def __init__(self):
        self.root_window = 0

        libtcod.console_set_custom_font("data/terminal10x18_gs_ro.png",
                                        libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
        libtcod.console_init_root(GAME.SCREEN_COLS, GAME.SCREEN_ROWS,
                                  GAME.GAME_NAME, False, libtcod.RENDERER_SDL)

    def new_window(self, size):
        return _LibTCODWindow(size, self)

    def flush(self):
        libtcod.console_flush()

    def suspend(self):
        """SDL version doesn't require suspend."""
        pass

    def resume(self):
        """SDL version doesn't require resume."""
        pass

    def toggle_fullscreen(self):
        if libtcod.console_is_fullscreen():
            libtcod.console_set_fullscreen(False)
        else:
            libtcod.console_set_fullscreen(True)

    def _get_key(self, window_not_used=None):
        while True:
            key_event = libtcod.Key()
            mouse_event = libtcod.Mouse()
            libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS, key_event, mouse_event, False)
            key = self._interpret_event(key_event)
            if key != KEY.NO_INPUT:
                return key

    def _check_key(self, window_not_used=None):
        event = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)
        return self._interpret_event(event)

    def _interpret_event(self, event):
        if libtcod.console_is_window_closed():
            return KEY.CLOSE_WINDOW
        elif event.vk in key_map:
            return key_map[event.vk]
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

    def get_implementation(self):
        return LIBTCOD

    def get_root_window_dimensions(self):
        return libtcod.console_get_height(self.root_window), libtcod.console_get_width(self.root_window)


class _LibTCODWindow(object):

    def __init__(self, size, cursor_lib):
        self.cursor_lib = cursor_lib
        self.default_fg = libtcod.white
        self.default_bg = libtcod.black

        locale.setlocale(locale.LC_ALL, "")
        self.encoding = locale.getpreferredencoding()

        rows, columns = size
        self.window = libtcod.console_new(columns, rows)
        libtcod.console_set_default_foreground(self.window, self.default_fg)
        libtcod.console_set_default_background(self.window, self.default_bg)

    def clear(self):
        libtcod.console_clear(self.window)

    def blit(self, size, screen_position):
        rows, cols = size
        y, x = screen_position
        libtcod.console_blit(self.window, 0, 0, cols, rows,
                             self.cursor_lib.root_window, x, y, 1.0, 1.0)

    def get_dimensions(self):
        return libtcod.console_get_height(self.window), libtcod.console_get_width(self.window)

    def get_key(self):
        return self.cursor_lib._get_key()

    def check_key(self):
        return self.cursor_lib._check_key()

    def addch(self, y, x, char):
        symbol, (fg, bg) = char
        libtcod.console_put_char_ex(self.window, x, y, symbol.encode(self.encoding), color_map[fg], color_map[bg])

    def addstr(self, y, x, string, color=None):
        if color is None:
            libtcod.console_print(self.window, x, y, string.encode(self.encoding))
        else:
            fg, bg = color
            libtcod.console_set_default_foreground(self.window, color_map[fg])
            libtcod.console_set_default_background(self.window, color_map[bg])
            libtcod.console_print(self.window, x, y, string.encode(self.encoding))
            libtcod.console_set_default_foreground(self.window, self.default_fg)
            libtcod.console_set_default_background(self.window, self.default_bg)

    def draw(self, char_payload_sequence):
        f = libtcod.console_put_char_ex
        local_color = color_map
        for y, x, (symbol, (fg, bg)) in char_payload_sequence:
            f(self.window, x, y, symbol.encode(self.encoding), local_color[fg],
              local_color[bg])

    def draw_reverse(self, char_payload_sequence):
        f = libtcod.console_put_char_ex
        local_color = color_map
        for y, x, (symbol, (fg, bg)) in char_payload_sequence:
            f(self.window, x, y, symbol.encode(self.encoding), local_color[bg],
              local_color[fg])
