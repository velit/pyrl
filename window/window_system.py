from __future__ import division
import time
import const.game as GAME
import const.debug as DEBUG
import const.keys as KEY
import const.colors as COLOR
from const.game import MSG_BAR_HEIGHT, STATUS_BAR_HEIGHT, LEVEL_HEIGHT, LEVEL_WIDTH

from window.base_window import BaseWindow
from window.message import MessageBar
from window.status import StatusBar
from window.level import LevelWindow


class WindowSystem(object):

	def __init__(self, root_window):
		self.a = BaseWindow(root_window)

		m_handle, m_blit_args = self.a.subwindow(MSG_BAR_HEIGHT, LEVEL_WIDTH, 0, 0)
		l_handle, l_blit_args = self.a.subwindow(LEVEL_HEIGHT, LEVEL_WIDTH, MSG_BAR_HEIGHT, 0)
		s_handle, s_blit_args = self.a.subwindow(STATUS_BAR_HEIGHT, LEVEL_WIDTH, MSG_BAR_HEIGHT + LEVEL_HEIGHT, 0)

		self.m = MessageBar(m_handle, m_blit_args)
		self.l = LevelWindow(l_handle, l_blit_args)
		self.s = StatusBar(s_handle, s_blit_args)

		self.rows, self.cols = self.a.get_dimensions()

	def get_key(self, message=None, refresh=True):
		if message is not None:
			self.msg(message)
		if refresh:
			self.refresh()
		return self.a.get_key()

	def msg(self, *a):
		self.m.queue_msg(*a)

	def ask(self, message, keys=KEY.GROUP_ALL):
		self.msg(message)
		self.refresh()
		return self.a.selective_get_key(keys)

	def notify(self, print_str):
		return self.ask(print_str, KEY.GROUP_MORE)

	def refresh(self):
		self.m.update(); self.l.update(); self.s.update(); self.a.flush();

	def erase(self):
		self.a.erase(); self.m.erase(); self.l.erase(); self.s.erase();

	# clear is stronger than erase, on ncurses it causes a full refresh
	def clear(self):
		self.a.clear(); self.m.clear(); self.l.clear(); self.s.clear();

	def draw(self, character_data_sequence, reverse=False):
		if not reverse:
			self.l.draw(character_data_sequence)
		else:
			self.l.draw_reverse(character_data_sequence)

	def menu(self, lines):
		self.a.add_lines(lines)
		return self.a.get_key(refresh=True)

	def draw_char(self, coord, char, reverse=False):
		self.l.draw_char(coord, char, reverse)

	def drawline(self, *a, **k):
		self.l.draw_line(*a, **k)

	def draw_path(self, path):
		for x in path:
			self.draw_char(x, (" ", COLOR.GREEN), reverse=True)
			if DEBUG.PATH_STEP: self.get_key()
		if not DEBUG.PATH_STEP: self.get_key()

	def suspend(self):
		self.a.suspend()

	def ask_until_timestamp(self, message, timestamp, key_set):
		self.msg(message)
		self.refresh()
		return self.a.selective_get_key_until_timestamp(timestamp, key_set)

	def get_future_time(self, delay=GAME.ANIMATION_DELAY):
		return time.time() + delay
