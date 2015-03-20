from __future__ import absolute_import, division, print_function, unicode_literals

import locale
import const.game as GAME
import const.keys as KEY
from io_wrappers.libtcod_dicts import libtcod_color_map
from io_wrappers.libtcod_dicts import libtcod_key_map


try:
    import libtcod.libtcodpy as libtcod
except Exception as e:
    import sys
    print("Couldn't load libtcod. Tried both 64-bit and 32-bit libs.", file=sys.stderr)
    print("It's possible this happens because libsdl isn't installed.", file=sys.stderr)
    sys.exit(1)


def LibTCODWrapper():
    libtcod.console_set_custom_font("data/terminal10x18_gs_ro.png",
            libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(GAME.SCREEN_COLS, GAME.SCREEN_ROWS,
            GAME.GAME_NAME, False, libtcod.RENDERER_SDL)
    return _LibTCODWrapper


class _LibTCODWrapper(object):

    _root_win = 0
    _default_fg = libtcod.white
    _default_bg = libtcod.black

    IMPLEMENTATION = GAME.LIBTCOD

    key_map = libtcod_key_map
    color_map = libtcod_color_map

    locale.setlocale(locale.LC_ALL, "")
    encoding = locale.getpreferredencoding()

    @staticmethod
    def flush():
        libtcod.console_flush()

    @staticmethod
    def suspend():
        """SDL version doesn't require suspend."""
        pass

    @staticmethod
    def resume():
        """SDL version doesn't require resume."""
        pass

    @classmethod
    def get_key(cls):
        while True:
            key_event = libtcod.Key()
            mouse_event = libtcod.Mouse()
            libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS, key_event, mouse_event, False)
            key = cls._interpret_event(key_event)
            if key != KEY.NO_INPUT:
                return key

    @classmethod
    def check_key(cls):
        event = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)
        return cls._interpret_event(event)

    @classmethod
    def _interpret_event(cls, event):
        if libtcod.console_is_window_closed():
            return KEY.CLOSE_WINDOW
        elif event.vk in cls.key_map:
            return cls.key_map[event.vk]
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

    @staticmethod
    def _toggle_fullscreen():
        if libtcod.console_is_fullscreen():
            libtcod.console_set_fullscreen(False)
        else:
            libtcod.console_set_fullscreen(True)

    @classmethod
    def new_window(cls, size):
        rows, columns = size
        window = libtcod.console_new(columns, rows)
        return cls(window)

    def __init__(self, libtcod_window):
        self.window = libtcod_window
        libtcod.console_set_default_foreground(self.window, self._default_fg)
        libtcod.console_set_default_background(self.window, self._default_bg)

    def clear(self):
        libtcod.console_clear(self.window)

    def blit(self, size, screen_position):
        rows, cols = size
        y, x = screen_position
        libtcod.console_blit(self.window, 0, 0, cols, rows, self._root_win, x, y, 1.0, 1.0)

    def get_dimensions(self):
        return libtcod.console_get_height(self.window), libtcod.console_get_width(self.window)

    def addch(self, y, x, char):
        symbol, (fg, bg) = char
        libtcod.console_put_char_ex(self.window, x, y,
                                    symbol.encode(self.encoding),
                                    self.color_map[fg], self.color_map[bg])

    def addstr(self, y, x, string, color=None):
        if color is None:
            libtcod.console_print(self.window, x, y, string.encode(self.encoding))
        else:
            fg, bg = color
            libtcod.console_set_default_foreground(self.window, self.color_map[fg])
            libtcod.console_set_default_background(self.window, self.color_map[bg])
            libtcod.console_print(self.window, x, y, string.encode(self.encoding))
            libtcod.console_set_default_foreground(self.window, self._default_fg)
            libtcod.console_set_default_background(self.window, self._default_bg)

    def draw(self, char_payload_sequence):
        f = libtcod.console_put_char_ex
        local_color = self.color_map
        for y, x, (symbol, (fg, bg)) in char_payload_sequence:
            f(self.window, x, y, symbol.encode(self.encoding), local_color[fg],
              local_color[bg])

    def draw_reverse(self, char_payload_sequence):
        f = libtcod.console_put_char_ex
        local_color = self.color_map
        for y, x, (symbol, (fg, bg)) in char_payload_sequence:
            f(self.window, x, y, symbol.encode(self.encoding), local_color[bg],
              local_color[fg])
