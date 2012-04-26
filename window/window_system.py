from __future__ import division
import time
import debug
import mappings as MAPPING
import const.colors as COLOR

from window.base_window import BaseWindow
from window.message import MessageBar
from window.status import StatusBar
from window.level import LevelWindow
from main import cursor_lib


class WindowSystem(object):

    def __init__(self, root_window):
        from const.game import MSG_BAR_HEIGHT, STATUS_BAR_HEIGHT, LEVEL_HEIGHT, LEVEL_WIDTH
        from const.game import SCREEN_ROWS, SCREEN_COLS

        self.a = BaseWindow((SCREEN_ROWS, SCREEN_COLS), (0, 0))
        self.m = MessageBar((MSG_BAR_HEIGHT, LEVEL_WIDTH), (0, 0))
        self.l = LevelWindow((LEVEL_HEIGHT, LEVEL_WIDTH), (MSG_BAR_HEIGHT, 0))
        self.s = StatusBar((STATUS_BAR_HEIGHT, LEVEL_WIDTH), (MSG_BAR_HEIGHT + LEVEL_HEIGHT, 0))

    def get_key(self, message=None, refresh=True):
        if message is not None:
            self.msg(message)
        if refresh:
            self.refresh()
        return self.l.get_key()

    def msg(self, *a):
        self.m.queue_msg(*a)

    def ask(self, message, keys=MAPPING.GROUP_ALL):
        self.msg(message)
        self.refresh()
        return self.l.selective_get_key(keys)

    def notify(self, print_str):
        return self.ask(print_str, MAPPING.GROUP_MORE)

    def refresh(self):
        self.m.update()
        self.l.update()
        self.s.update()
        cursor_lib.flush()

    def draw(self, character_data_sequence, reverse=False):
        if not reverse:
            self.l.draw(character_data_sequence)
        else:
            self.l.draw_reverse(character_data_sequence)

    def menu(self, header, lines, footer, key_set, target_window=None):
        if target_window is None:
            target_window = self.a
        target_window.clear()
        target_window.draw_header(header)
        target_window.draw_lines(lines)
        target_window.draw_footer(footer)
        return target_window.selective_get_key(key_set, refresh=True)

    def draw_char(self, coord, char, reverse=False):
        self.l.draw_char(coord, char, reverse)

    def draw_line(self, *a, **k):
        self.l.draw_line(*a, **k)

    def draw_path(self, path):
        for x in path:
            self.draw_char(x, (" ", COLOR.GREEN), reverse=True)
            if debug.path_step: self.get_key()
        if not debug.path_step: self.get_key()

    def suspend(self):
        cursor_lib.suspend()

    def resume(self):
        cursor_lib.resume()

    def ask_until_timestamp(self, message, timestamp, key_set):
        self.msg(message)
        self.refresh()
        return self.l.selective_get_key_until_timestamp(timestamp, key_set)

    def get_future_time(self, delay):
        return time.time() + delay

    def get_current_time(self):
        return time.time()
