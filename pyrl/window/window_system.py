from collections import deque
from functools import wraps

from pyrl.config.debug import Debug
from pyrl.config.config import Config
from pyrl.enums.colors import Pair
from pyrl.game_data.levels.shared_assets import default_level_dimensions
from pyrl.generic_structures import TableDims, Coord
from pyrl.window.base_window import BaseWindow
from pyrl.window.level_window import LevelWindow
from pyrl.window.message_bar import MessageBar
from pyrl.window.status_bar import StatusBar

class WindowSystem:

    message_dimensions = TableDims(Config.message_bar_height, default_level_dimensions.cols)
    status_dimensions = TableDims(Config.status_bar_height, default_level_dimensions.cols)
    game_dimensions = TableDims(message_dimensions.rows + status_dimensions.rows +
                                default_level_dimensions.rows, default_level_dimensions.cols)

    def __init__(self, cursor_lib):
        self.cursor_lib = cursor_lib

        self.whole_window = BaseWindow(cursor_lib, self.game_dimensions, Coord(0, 0))
        self.message_bar  = MessageBar(cursor_lib, self.message_dimensions, Coord(0, 0))
        level_position    = Coord(self.message_bar.screen_position.y + self.message_bar.rows, 0)
        self.level_window = LevelWindow(cursor_lib, default_level_dimensions, level_position)
        status_position   = Coord(self.level_window.screen_position.y + self.level_window.rows, 0)
        self.status_bar   = StatusBar(cursor_lib, self.status_dimensions, status_position)

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
