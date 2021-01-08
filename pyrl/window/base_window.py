import time

from pyrl.enums.colors import Pair
from pyrl.enums.keys import Key
from pyrl.generic_structures import TableDims, Coord

class BaseWindow:

    # Seconds to sleep until next user input check in half-block functions
    half_block_input_responsiveness = 0.001

    def __init__(self, cursor_lib, dimensions, screen_position):
        self.cursor_lib = cursor_lib
        self.rows, self.cols = TableDims(*dimensions)
        self.screen_position = Coord(*screen_position)
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

    @classmethod
    def get_time(cls):
        """Get a time in fractional seconds that is compatible with self.check_key(until=timestamp)."""
        return time.perf_counter()

    def get_key(self, keys=None, refresh=False):
        """
        Return key from user.

        If keys is given only those keys are considered valid return values. Continues blocking
        until a valid key is returned by user in this case.
        """
        if refresh:
            self.refresh()

        while True:
            key = self.cursor_win.get_key()
            if not keys or key in keys:
                return key

    def check_key(self, keys=None, until=None, refresh=False):
        """
        Return key if user has given one, otherwise return Key.NO_INPUT.

        If keys is given only considers those keys valid return values returning Key.NO_INPUT
        otherwise.
        If until is given doesn't immediately return on no input. Instead waits for user input until
        given time and returns Key.NO_INPUT in case no input is given in this time period.
        """
        if refresh:
            self.refresh()

        while True:
            key = self.cursor_win.check_key()
            if until is None or self.get_time() >= until:
                break
            if key in keys:
                break
            time.sleep(self.half_block_input_responsiveness)

        if not keys or key in keys:
            return key
        else:
            return Key.NO_INPUT

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
        return self.get_key(keys=key_set, refresh=True)

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
        input_y = coord[0]
        input_x = coord[1] + len(ask_line)
        input_coord = input_y, input_x
        user_input = ""
        cursor_index = len(user_input)
        max_input_size = self.cols - input_x - 1
        while True:
            # Normalize input
            user_input = user_input[:max_input_size]
            cursor_index = max(min(cursor_index, len(user_input)), 0)

            # Update vars
            cursor_coord = input_y, input_x + cursor_index
            cursor_char = ((user_input + " ")[cursor_index], Pair.Cursor)

            # Print
            self.draw_str(user_input, input_coord)
            self.draw_char(cursor_char, cursor_coord)
            key = self.get_key(refresh=True)
            self.draw_str(" " * (len(user_input)), input_coord)
            self.draw_char((" ", Pair.Normal), cursor_coord)

            if key == Key.SPACE:
                key = " "

            if key in (Key.ENTER, "^m", "^j", "^d"):
                return user_input
            elif key == "^w":
                state_whitespace = True
                del_amount = 0
                for char in reversed(user_input[:cursor_index]):
                    if state_whitespace and not char.isspace():
                        state_whitespace = False
                    elif not state_whitespace and char.isspace():
                        break
                    del_amount += 1
                user_input = user_input[:cursor_index - del_amount] + user_input[cursor_index:]
                cursor_index -= del_amount
            elif key == "^u":
                user_input = user_input[cursor_index:]
                cursor_index = 0
            elif key in (Key.END, "^e"):
                cursor_index = len(user_input)
            elif key in (Key.HOME, "^a"):
                cursor_index = 0
            elif key in (Key.BACKSPACE, "^h"):
                user_input = user_input[:max(cursor_index - 1, 0)] + user_input[cursor_index:]
                cursor_index -= 1
            elif key == Key.DELETE:
                user_input = user_input[:cursor_index] + user_input[cursor_index + 1:]
            elif key == Key.LEFT:
                cursor_index -= 1
            elif key == Key.RIGHT:
                cursor_index += 1
            else:
                user_input = user_input[:cursor_index] + key + user_input[cursor_index:]
                cursor_index += len(key)
