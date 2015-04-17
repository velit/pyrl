from __future__ import absolute_import, division, print_function, unicode_literals

import time

from config.game import GameConf
from enums.colors import Pair
from enums.keys import Key


class BaseWindow(object):

    def __init__(self, cursor_lib, dimensions, screen_position):
        self.cursor_lib = cursor_lib
        self.rows, self.cols = dimensions
        self.screen_position = screen_position
        self.cursor_win = cursor_lib.new_window(dimensions)

    def addch(self, y, x, char):
        self.cursor_win.addch(y, x, char)

    def addstr(self, y, x, string, color=None):
        self.cursor_win.addstr(y, x, string, color)

    def draw(self, char_payload_sequence):
        self.cursor_win.draw(char_payload_sequence)

    def draw_reverse(self, char_payload_sequence):
        self.cursor_win.draw_reverse(char_payload_sequence)

    def clear(self):
        self.cursor_win.clear()

    # Blocking
    def get_key(self, refresh=False):
        if refresh:
            self.refresh()
        return self.cursor_win.get_key()

    # Non-blocking
    def check_key(self):
        return self.cursor_win.check_key()

    # Blocking
    def selective_get_key(self, key_set, refresh=False):
        if refresh:
            self.refresh()
        while True:
            key = self.get_key()
            if key in key_set:
                return key

    # Half-blocking
    def selective_get_key_until_timestamp(self, timestamp, key_set, refresh=False):
        if refresh:
            self.refresh()

        key = self.check_key()
        while key not in key_set:
            if time.time() >= timestamp:
                return Key.NO_INPUT
            time.sleep(GameConf.ANIMATION_INPUT_PERIOD)
            key = self.check_key()
        return key

    def blit(self):
        self.cursor_win.blit((self.rows, self.cols), self.screen_position)

    def refresh(self):
        self.blit()
        self.cursor_lib.flush()

    def draw_header(self, header, color=Pair.Brown, y=0):
        format_str = "{0:+^" + str(self.cols) + "}"
        header = format_str.format("  " + header + "  ")
        self.addstr(y, 0, header, color)

    def draw_lines(self, lines, y_offset=2, x_offset=0):
        for i, line in enumerate(lines):
            self.addstr(y_offset + i, x_offset, line)

    def draw_footer(self, footer, color=Pair.Brown, y=0):
        format_str = "{0:+^" + str(self.cols) + "}"
        footer = format_str.format("  " + footer + "  ")
        self.addstr((self.rows - 1) - y, 0, footer, color)
