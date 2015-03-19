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


class LibTCODWrapper(object):

    _ROOT_WIN = 0

    def __init__(self):

        libtcod.console_set_custom_font("data/terminal10x18_gs_ro.png",
                                        libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
        libtcod.console_init_root(GAME.SCREEN_COLS, GAME.SCREEN_ROWS,
                                  GAME.GAME_NAME, False, libtcod.RENDERER_SDL)

        self.default_fg = libtcod.white
        self.default_bg = libtcod.black

        locale.setlocale(locale.LC_ALL, "")
        self.encoding = locale.getpreferredencoding()

        C = COLOR
        lC = libtcod.Color
        self.color_map = {

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

        l = libtcod
        self.key_map = {
            l.KEY_ENTER: KEY.ENTER,          l.KEY_TAB: KEY.TAB,
            l.KEY_ESCAPE: KEY.ESC,           l.KEY_SPACE: KEY.SPACE,
            l.KEY_LEFT: KEY.LEFT,            l.KEY_RIGHT: KEY.RIGHT,
            l.KEY_UP: KEY.UP,                l.KEY_DOWN: KEY.DOWN,
            l.KEY_HOME: KEY.HOME,            l.KEY_END: KEY.END,
            l.KEY_PAGEDOWN: KEY.PAGE_DOWN,   l.KEY_PAGEUP: KEY.PAGE_UP,
            l.KEY_INSERT: KEY.INSERT,        l.KEY_DELETE: KEY.DELETE,
            l.KEY_BACKSPACE: KEY.BACKSPACE,  l.KEY_F1: KEY.F1,
            l.KEY_F2: KEY.F2,                l.KEY_F3: KEY.F3,
            l.KEY_F4: KEY.F4,                l.KEY_F5: KEY.F5,
            l.KEY_F6: KEY.F6,                l.KEY_F7: KEY.F7,
            l.KEY_F8: KEY.F8,                l.KEY_F9: KEY.F9,
            l.KEY_F10: KEY.F10,              l.KEY_F11: KEY.F11,
            l.KEY_F12: KEY.F12,              l.KEY_KP0: KEY.NUMPAD_0,
            l.KEY_KP1: KEY.NUMPAD_1,         l.KEY_KP2: KEY.NUMPAD_2,
            l.KEY_KP3: KEY.NUMPAD_3,         l.KEY_KP4: KEY.NUMPAD_4,
            l.KEY_KP5: KEY.NUMPAD_5,         l.KEY_KP6: KEY.NUMPAD_6,
            l.KEY_KP7: KEY.NUMPAD_7,         l.KEY_KP8: KEY.NUMPAD_8,
            l.KEY_KP9: KEY.NUMPAD_9,         l.KEY_NONE: KEY.NO_INPUT,
        }

    def new_window(self, size):
        rows, columns = size
        window = libtcod.console_new(columns, rows)
        libtcod.console_set_default_foreground(window, self.default_fg)
        libtcod.console_set_default_background(window, self.default_bg)
        return window

    def flush(self):
        libtcod.console_flush()

    def get_root_window(self):
        return self._ROOT_WIN

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

    def addch(self, window, y, x, char):
        symbol, (fg, bg) = char
        libtcod.console_put_char_ex(window, x, y, symbol.encode(self.encoding), self.color_map[fg], self.color_map[bg])

    def addstr(self, window, y, x, string, color=None):
        if color is None:
            libtcod.console_print(window, x, y, string.encode(self.encoding))
        else:
            fg, bg = color
            libtcod.console_set_default_foreground(window, self.color_map[fg])
            libtcod.console_set_default_background(window, self.color_map[bg])
            libtcod.console_print(window, x, y, string.encode(self.encoding))
            libtcod.console_set_default_foreground(window, self.default_fg)
            libtcod.console_set_default_background(window, self.default_bg)

    def draw(self, window, char_payload_sequence):
        f = libtcod.console_put_char_ex
        color = self.color_map
        for y, x, (symbol, (fg, bg)) in char_payload_sequence:
            f(window, x, y, symbol.encode(self.encoding), color[fg], color[bg])

    def draw_reverse(self, window, char_payload_sequence):
        f = libtcod.console_put_char_ex
        color = self.color_map
        for y, x, (symbol, (fg, bg)) in char_payload_sequence:
            f(window, x, y, symbol.encode(self.encoding), color[bg], color[fg])

    def get_key(self, window_not_used):
        while True:
            key_event = libtcod.Key()
            mouse_event = libtcod.Mouse()
            libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS, key_event, mouse_event, False)
            key = self.interpret_event(key_event)
            if key != KEY.NO_INPUT:
                return key

    def check_key(self, handle_not_used):
        event = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)
        return self.interpret_event(event)

    def interpret_event(self, event):
        if libtcod.console_is_window_closed():
            return KEY.CLOSE_WINDOW
        elif event.vk in self.key_map:
            return self.key_map[event.vk]
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

    def clear(self, window):
        libtcod.console_clear(window)

    def blit(self, window, size, screen_position):
        rows, cols = size
        y, x = screen_position
        libtcod.console_blit(window, 0, 0, cols, rows, self._ROOT_WIN, x, y, 1.0, 1.0)

    def get_dimensions(self, window):
        return libtcod.console_get_height(window), libtcod.console_get_width(window)

    def get_implementation(self):
        return LIBTCOD
