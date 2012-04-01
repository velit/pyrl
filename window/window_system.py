from __future__ import division
import time
import const.game as GAME
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

		self.a = BaseWindow((GAME.SCREEN_ROWS, GAME.SCREEN_COLS), (0, 0))
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

	def menu(self, header, lines, footer, key_set):
		self.a.clear()
		self.a.draw_header(header)
		self.a.draw_lines(lines)
		self.a.draw_footer(footer)
		return self.a.selective_get_key(key_set, refresh=True)

	def draw_char(self, coord, char, reverse=False):
		self.l.draw_char(coord, char, reverse)

	def drawline(self, *a, **k):
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

	def get_future_time(self, delay=None):
		if delay is not None:
			return time.time() + delay
		else:
			return time.time() + GAME.ANIMATION_DELAY
