from collections import deque
from functools import wraps

from config.debug import Debug
from config.game import GameConf
from enums.colors import Pair
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

        self.prepared_input = deque()

    def get_key(self, message=None, keys=None):
        if message:
            self.msg(message)

        self.refresh()

        if self.prepared_input:
            return self.prepared_input.popleft()

        return self.whole_window.get_key(keys=keys)

    def check_key(self, message=None, keys=None, until=None):
        if message:
            self.msg(message)

        self.refresh()

        return self.whole_window.check_key(keys=keys, until=until)

    def msg(self, *messages):
        self.message_bar.queue_msg(*messages)

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

    @wraps(BaseWindow.menu, assigned=())
    def menu(self, *args, **kwargs):
        return self.whole_window.menu(*args, **kwargs)

    @wraps(LevelWindow.draw_char, assigned=())
    def draw_char(self, *args, **kwargs):
        self.level_window.draw_char(*args, **kwargs)

    @wraps(LevelWindow.draw_line, assigned=())
    def draw_line(self, *args, **kwargs):
        self.level_window.draw_line(*args, **kwargs)

    def draw_path(self, path):
        for coord in path:
            self.draw_char((" ", Pair.Green), coord, reverse=True)
            if Debug.path_step:
                self.level_window.get_key(refresh=True)
        if not Debug.path_step:
            self.level_window.get_key(refresh=True)

    def suspend(self):
        self.cursor_lib.suspend()

    def resume(self):
        self.cursor_lib.resume()

    def get_str(self, ask_line="", coord=(0, 0)):
        self.message_bar.clear()
        return self.message_bar.get_str(ask_line=ask_line, coord=coord)

    def get_future_time(self, delay):
        return BaseWindow.get_time() + delay

    def get_time(self):
        return BaseWindow.get_time()
