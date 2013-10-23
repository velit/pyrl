from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time
import const.keys as KEY
import const.game as GAME
import const.colors as COLOR


class BaseWindow(object):

    def __init__(self, cursor_lib, size, screen_position):
        self.cursor_lib = cursor_lib
        self.h = self.cursor_lib.new_window(size)
        self.rows, self.cols = size
        self.screen_position = screen_position

    def addch(self, y, x, char):
        self.cursor_lib.addch(self.h, y, x, char)

    def addstr(self, y, x, string, color=None):
        self.cursor_lib.addstr(self.h, y, x, string, color)

    def draw(self, char_payload_sequence):
        self.cursor_lib.draw(self.h, char_payload_sequence)

    def draw_reverse(self, char_payload_sequence):
        self.cursor_lib.draw_reverse(self.h, char_payload_sequence)

    def clear(self):
        self.cursor_lib.clear(self.h)

    # Blocking
    def get_key(self, refresh=False):
        if refresh:
            self.refresh()
        return self.cursor_lib.get_key(self.h)

    # Non-blocking
    def check_key(self, refresh=False):
        if refresh:
            self.refresh()
        return self.cursor_lib.check_key(self.h)

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
        self.cursor_lib.blit(self.h, size, self.screen_position)

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
