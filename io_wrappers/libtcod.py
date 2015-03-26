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


class LibTCODWrapper(object):

    IMPLEMENTATION = GAME.LIBTCOD

    def __init__(self, curses_root_window=None):
        """Init the SDL surface and prepare for draw calls."""
        libtcod.console_set_custom_font("data/terminal10x18_gs_ro.png",
                                        libtcod.FONT_TYPE_GREYSCALE |
                                        libtcod.FONT_LAYOUT_ASCII_INROW)
        libtcod.console_init_root(GAME.SCREEN_COLS, GAME.SCREEN_ROWS,
                                  GAME.GAME_NAME, False, libtcod.RENDERER_SDL)
        LibTCODWindow.init_class_attributes()

    def new_window(self, dimensions):
        rows, columns = dimensions
        window = libtcod.console_new(columns, rows)
        return LibTCODWindow(window)

    def flush(self):
        libtcod.console_flush()

    def suspend(self):
        """SDL version doesn't require suspend."""
        pass

    def resume(self):
        """SDL version doesn't require resume."""
        pass

    def _toggle_fullscreen(self):
        if libtcod.console_is_fullscreen():
            libtcod.console_set_fullscreen(False)
        else:
            libtcod.console_set_fullscreen(True)


class LibTCODWindow(object):

    _root_win = None
    _encoding = None
    _default_fg = libtcod.white
    _default_bg = libtcod.black
    _key_map = libtcod_key_map
    _color_map = libtcod_color_map
    IMPLEMENTATION = GAME.LIBTCOD

    @classmethod
    def init_class_attributes(cls):
        """
        Initialize class attributes.

        This function has to be called separately if this class is used
        directly instead of from LibTCODWrapper().new_window(dimensions)
        """
        cls._root_win = 0
        cls._encoding = locale.getpreferredencoding()

    def __init__(self, libtcod_window):
        self.win = libtcod_window
        libtcod.console_set_default_foreground(self.win, self._default_fg)
        libtcod.console_set_default_background(self.win, self._default_bg)

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
        elif event.vk in cls._key_map:
            return cls._key_map[event.vk]
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

    def clear(self):
        libtcod.console_clear(self.win)

    def blit(self, size, screen_position):
        rows, cols = size
        y, x = screen_position
        libtcod.console_blit(self.win, 0, 0, cols, rows, self._root_win, x, y, 1.0, 1.0)

    def get_dimensions(self):
        return libtcod.console_get_height(self.win), libtcod.console_get_width(self.win)

    def addch(self, y, x, char):
        symbol, (fg, bg) = char
        libtcod.console_put_char_ex(self.win, x, y,
                                    symbol.encode(self._encoding),
                                    self._color_map[fg], self._color_map[bg])

    def addstr(self, y, x, string, color=None):
        if color is None:
            libtcod.console_print(self.win, x, y, string.encode(self._encoding))
        else:
            fg, bg = color
            libtcod.console_set_default_foreground(self.win, self._color_map[fg])
            libtcod.console_set_default_background(self.win, self._color_map[bg])
            libtcod.console_print(self.win, x, y, string.encode(self._encoding))
            libtcod.console_set_default_foreground(self.win, self._default_fg)
            libtcod.console_set_default_background(self.win, self._default_bg)

    def draw(self, char_payload_sequence):
        d = libtcod.console_put_char_ex
        local_color = self._color_map
        for y, x, (symbol, (fg, bg)) in char_payload_sequence:
            d(self.win, x, y, symbol.encode(self._encoding), local_color[fg],
              local_color[bg])

    def draw_reverse(self, char_payload_sequence):
        d = libtcod.console_put_char_ex
        local_color = self._color_map
        for y, x, (symbol, (fg, bg)) in char_payload_sequence:
            d(self.win, x, y, symbol.encode(self._encoding), local_color[bg],
              local_color[fg])
