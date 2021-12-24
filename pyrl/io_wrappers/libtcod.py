from __future__ import annotations

import tcod

from pyrl.config.config import Config
from pyrl.constants.colors import ColorPair, Color
from pyrl.constants.keys import Key
from pyrl.io_wrappers.libtcod_dicts import libtcod_color_map, libtcod_key_map
from pyrl.window.window_system import WindowSystem

IMPLEMENTATION = "tcod"

class TCODWrapper:

    """Wrapper for the chronicles of doryen roguelike library (SDL)."""

    implementation = IMPLEMENTATION

    def __init__(self, root_window=None):
        """Init the SDL surface and prepare for draw calls."""
        flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INROW
        tcod.console_set_custom_font(b"resources/terminal10x18_gs_ro.png", flags)
        rows, cols = WindowSystem.game_dimensions
        tcod.console_init_root(cols, rows, Config.default_game_name.encode(), False,
                               tcod.RENDERER_SDL)

    def new_window(self, dimensions):
        rows, columns = dimensions
        window = tcod.console_new(columns, rows)
        return TCODWindow(window)

    def flush(self):
        tcod.console_flush()

    def suspend(self):
        """SDL version doesn't require suspend."""
        pass

    def resume(self):
        """SDL version doesn't require resume."""
        pass

    def _toggle_fullscreen(self):
        if tcod.console_is_fullscreen():
            tcod.console_set_fullscreen(False)
        else:
            tcod.console_set_fullscreen(True)

class TCODWindow:

    implementation = IMPLEMENTATION
    key_map = libtcod_key_map
    color_map = libtcod_color_map

    def __init__(self, libtcod_window):
        self.default_fg = self.color_map[Color.Normal]
        self.default_bg = self.color_map[Color.Black]
        self.win = libtcod_window
        tcod.console_set_default_foreground(self.win, self.default_fg)
        tcod.console_set_default_background(self.win, self.default_bg)

    def get_key(self):
        while True:
            key_event = tcod.Key()
            mouse_event = tcod.Mouse()
            tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key_event, mouse_event, False)
            key = self._interpret_event(key_event)
            if key != Key.NO_INPUT:
                return key

    def check_key(self):
        event = tcod.console_check_for_keypress(tcod.KEY_PRESSED)
        return self._interpret_event(event)

    def _interpret_event(self, event):
        if tcod.console_is_window_closed():
            return Key.CLOSE_WINDOW
        elif event.vk in self.key_map:
            return self.key_map[event.vk]
        elif event.vk == tcod.KEY_CHAR:
            if event.c == ord('c') and event.lctrl or event.rctrl:
                raise KeyboardInterrupt
            ch = chr(event.c)
            if event.shift:
                ch = ch.upper()
            if event.lctrl or event.rctrl:
                ch = "^" + ch
            if event.lalt or event.ralt:
                ch = "!" + ch
            return ch
        else:
            return Key.NO_INPUT

    def clear(self):
        tcod.console_clear(self.win)

    def blit(self, size, screen_position):
        rows, cols = size
        y, x = screen_position
        tcod.console_blit(self.win, 0, 0, cols, rows, 0, x, y, 1.0, 1.0)

    def get_dimensions(self):
        return tcod.console_get_height(self.win), tcod.console_get_width(self.win)

    def draw_char(self, char, coord=(0, 0)):
        y, x = coord
        symbol, (fg, bg) = char
        tcod.console_put_char_ex(self.win, x, y, symbol, self.color_map[fg], self.color_map[bg])

    def draw_str(self, string, coord=(0, 0), color=None):
        y, x = coord
        if color is None:
            fg, bg = ColorPair.Normal
        else:
            fg, bg = color
        tcod.console_set_color_control(tcod.COLCTRL_1, self.color_map[fg], self.color_map[bg])
        string = chr(tcod.COLCTRL_1) + string + chr(tcod.COLCTRL_STOP)
        tcod.console_print(self.win, x, y, string)

    def draw(self, char_payload_sequence):
        d = tcod.console_put_char_ex
        local_color = self.color_map
        for (y, x), (symbol, (fg, bg)) in char_payload_sequence:
            d(self.win, x, y, symbol, local_color[fg], local_color[bg])

    def draw_reverse(self, char_payload_sequence):
        d = tcod.console_put_char_ex
        local_color = self.color_map
        for (y, x), (symbol, (fg, bg)) in char_payload_sequence:
            d(self.win, x, y, symbol, local_color[bg], local_color[fg])
