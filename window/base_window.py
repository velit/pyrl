from __future__ import absolute_import, division, print_function, unicode_literals

import time

import const.colors as COLOR
import const.game as GAME
import const.keys as KEY


class BaseWindow(object):

    def __init__(self, cursor_lib, size, screen_position):
        self.cursor_lib = cursor_lib
        self.cursor_win = cursor_lib.new_window(size)
        self.rows, self.cols = size
        self.screen_position = screen_position

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
                return KEY.NO_INPUT
            time.sleep(GAME.INPUT_INTERVAL)
            key = self.check_key()
        return key

    def blit(self):
        size = self.rows, self.cols
        self.cursor_win.blit(size, self.screen_position)

    def refresh(self):
        self.blit()
        self.cursor_lib.flush()

    def draw_header(self, header, color=COLOR.BROWN, y=0):
        format_str = "{0:+^" + str(self.cols) + "}"
        header = format_str.format("  " + header + "  ")
        self.addstr(y, 0, header, color)

    def draw_lines(self, lines, y_offset=2, x_offset=0):
        for i, line in enumerate(lines):
            self.addstr(y_offset + i, x_offset, line)

    def draw_footer(self, footer, color=COLOR.BROWN, y=0):
        format_str = "{0:+^" + str(self.cols) + "}"
        footer = format_str.format("  " + footer + "  ")
        self.addstr((self.rows - 1) - y, 0, footer, color)
