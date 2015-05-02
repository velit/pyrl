from __future__ import absolute_import, division, print_function, unicode_literals

import time

from enums.colors import Pair
from config.mappings import Mapping
from config.game import GameConf
from config.debug import Debug
from window.base_window import BaseWindow
from window.level import LevelWindow
from window.message import MessageBar
from window.status import StatusBar


class WindowSystem(object):

    def __init__(self, cursor_lib):
        self.cursor_lib = cursor_lib

        msg_rows = GameConf.message_bar_height
        lvl_rows, lvl_cols = GameConf.LEVEL_DIMENSIONS
        sts_rows = GameConf.status_bar_height

        msg_bar_dims = (msg_rows, lvl_cols)
        lvl_bar_dims = (lvl_rows, lvl_cols)
        sts_bar_dims = (sts_rows, lvl_cols)

        self.whole_window = BaseWindow(cursor_lib, GameConf.game_dimensions, (0, 0))

        self.message_bar  = MessageBar(cursor_lib, msg_bar_dims, (0, 0))
        level_position    = (self.message_bar.screen_position[0] + self.message_bar.rows, 0)
        self.level_window = LevelWindow(cursor_lib, lvl_bar_dims, level_position)
        status_position   = (self.level_window.screen_position[0] + self.level_window.rows, 0)
        self.status_bar   = StatusBar(cursor_lib, sts_bar_dims, status_position)

    def get_key(self, message=None, refresh=True):
        if message is not None:
            self.msg(message)
        if refresh:
            self.refresh()
        return self.level_window.get_key()

    def msg(self, *a):
        self.message_bar.queue_msg(*a)

    def ask(self, message, keys=Mapping.Group_All):
        self.msg(message)
        self.refresh()
        return self.level_window.selective_get_key(keys)

    def notify(self, print_str):
        return self.ask(print_str, Mapping.Group_More)

    def refresh(self):
        self.message_bar.update()
        self.level_window.update()
        self.status_bar.update()
        self.cursor_lib.flush()

    def draw(self, character_data_sequence, reverse=False):
        if not reverse:
            self.level_window.draw(character_data_sequence)
        else:
            self.level_window.draw_reverse(character_data_sequence)

    def menu(self, header, lines, footer, key_set, target_window=None):
        if target_window is None:
            target_window = self.whole_window
        target_window.clear()
        target_window.draw_banner(header)
        target_window.draw_lines(lines, y_offset=2)
        target_window.draw_banner(footer, y_offset=-1)
        return target_window.selective_get_key(key_set, refresh=True)

    def draw_char(self, coord, char, reverse=False):
        self.level_window.draw_char(coord, char, reverse)

    def draw_line(self, *a, **k):
        self.level_window.draw_line(*a, **k)

    def draw_path(self, path):
        for coord in path:
            self.draw_char(coord, (" ", Pair.Green), reverse=True)
            if Debug.path_step:
                self.level_window.get_key(refresh=True)
        if not Debug.path_step:
            self.level_window.get_key(refresh=True)

    def suspend(self):
        self.cursor_lib.suspend()

    def resume(self):
        self.cursor_lib.resume()

    def ask_until_timestamp(self, message, timestamp, key_set):
        self.msg(message)
        self.refresh()
        return self.level_window.selective_get_key_until_timestamp(timestamp, key_set)

    def get_future_time(self, delay):
        return time.time() + delay

    def get_current_time(self):
        return time.time()
