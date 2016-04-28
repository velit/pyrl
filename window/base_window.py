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

    def draw_char(self, char, coord):
        self.cursor_win.draw_char(char, coord)

    def draw_str(self, string, coord, color=None):
        self.cursor_win.draw_str(string, coord, color)

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

    # Half-blocking
    def get_key_until_timestamp(self, timestamp, refresh=False):
        if refresh:
            self.refresh()

        key = self.check_key()
        while key == Key.NO_INPUT and time.monotonic() < timestamp:
            time.sleep(GameConf.ANIMATION_INPUT_PERIOD)
            key = self.check_key()
        return key

    # Blocking
    def selective_get_key(self, key_seq, refresh=False):
        if refresh:
            self.refresh()

        key = self.get_key()
        while key not in key_seq:
            key = self.get_key()
        return key

    # Half-blocking
    def selective_get_key_until_timestamp(self, timestamp, key_seq, refresh=False):
        if refresh:
            self.refresh()

        key = self.check_key()
        while key not in key_seq:
            if timestamp < time.monotonic():
                return Key.NO_INPUT
            time.sleep(GameConf.ANIMATION_INPUT_PERIOD)
            key = self.check_key()
        return key

    def blit(self):
        self.cursor_win.blit((self.rows, self.cols), self.screen_position)

    def refresh(self):
        self.blit()
        self.cursor_lib.flush()

    def menu(self, header, lines, footer, key_set):
        self.clear()
        self.draw_banner(header)
        self.draw_lines(lines, y_offset=2)
        self.draw_banner(footer, y_offset=-1)
        return self.selective_get_key(key_set, refresh=True)

    def draw_lines(self, lines, y_offset=0, x_offset=0):
        for i, line in enumerate(lines):
            self.draw_str(line, (i + y_offset, x_offset))

    def draw_banner(self, banner_text, y_offset=0, color=Pair.Brown):
        format_str = "{0:+^" + str(self.cols) + "}"
        banner_text = format_str.format("  " + banner_text + "  ")
        if y_offset < 0:
            self.draw_str(banner_text, (self.rows + y_offset, 0), color)
        else:
            self.draw_str(banner_text, (y_offset, 0), color)

    def get_str(self, ask_line="", coord=(0, 0)):
        self.draw_str(ask_line, coord)
        y, x = coord[0], coord[1] + len(ask_line)
        cursor_pos = 0
        user_input = ""
        max_size = self.cols - x - 1
        while True:
            user_input = user_input[:max_size]
            cursor_pos = min(max(cursor_pos, -len(user_input)), 0)
            positive_pos = len(user_input) + cursor_pos
            self.draw_str(user_input, (y, x))
            cursor_char = (" " + user_input)[cursor_pos]
            self.draw_char((cursor_char, Pair.Cursor), (y, x + len(user_input) + cursor_pos))
            key = self.get_key(refresh=True)
            self.draw_str(" " * (len(user_input) + 1), (y, x))

            if key == Key.SPACE:
                key = " "

            if key in (Key.ENTER, "^m", "^j", "^d"):
                return user_input
            elif key in ("^w", "^u"):
                user_input = user_input[positive_pos:]
            elif key in (Key.END, "^e"):
                cursor_pos = 0
            elif key in (Key.HOME, "^a"):
                cursor_pos = -len(user_input)
            elif key in (Key.BACKSPACE, "^h"):
                user_input = user_input[:positive_pos - 1] + user_input[positive_pos:]
            elif key == Key.DELETE:
                user_input = user_input[:positive_pos] + user_input[positive_pos + 1:]
                cursor_pos += 1
            elif key == Key.LEFT:
                cursor_pos = max(cursor_pos - 1, -len(user_input))
            elif key == Key.RIGHT:
                cursor_pos = min(cursor_pos + 1, 0)
            else:
                user_input = user_input[:positive_pos] + key + user_input[positive_pos:]
