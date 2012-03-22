from __future__ import division
import time
import const.game as GAME
import const.debug as DEBUG
import const.keys as KEY
import const.colors as COLOR

from window.base_window import BaseWindow
from window.message import MessageBar
from window.status import StatusBar
from window.level import LevelWindow
from const.game import MSG_BAR_HEIGHT, STATUS_BAR_HEIGHT, LEVEL_HEIGHT, LEVEL_WIDTH


class WindowSystem(object):

	def __init__(self, root_window):
		self.a = BaseWindow(root_window)

		mh, mb = self.a.sub_handle(MSG_BAR_HEIGHT, LEVEL_WIDTH, 0, 0)
		lh, lb = self.a.sub_handle(LEVEL_HEIGHT, LEVEL_WIDTH, MSG_BAR_HEIGHT, 0)
		sh, sb = self.a.sub_handle(STATUS_BAR_HEIGHT, LEVEL_WIDTH, MSG_BAR_HEIGHT + LEVEL_HEIGHT, 0)

		self.m = MessageBar(mh, mb)
		self.l = LevelWindow(lh, lb)
		self.s = StatusBar(sh, sb)

		self.rows, self.cols = self.a.get_dimensions()

	def get_key(self, print_str=None):
		if print_str is not None:
			self.msg(print_str)
		self.refresh()
		return self.a.get_key()

	# returns KEY.NO_INPUT if timestamp is reached without input
	def selective_check_key_until_timestamp(self, key_set, timestamp, stepping=GAME.INPUT_INTERVAL):
		self.refresh()
		t = time.time
		sleep = time.sleep
		key = self.a.check_key()
		while t() < timestamp and key not in key_set:
			key = self.a.check_key()
			sleep(stepping)
		return key

	def ask(self, string, char_seq=KEY.GROUP_ALL):
		self.msg(string)
		return self._selective_getch(char_seq)

	def notify(self, print_str):
		self.msg(print_str)
		return self._selective_getch(KEY.GROUP_MORE)

	def msg(self, *a):
		self.m.queue_msg(*a)

	def refresh(self):
		self.m.update()
		self.l.update()
		self.s.update()
		self.a.flush()

	def erase(self):
		self.m.erase()
		self.l.erase()
		self.s.erase()

	def clear(self):
		self.m.clear()
		self.l.clear()
		self.s.clear()

	def draw(self, character_data_sequence, reverse=False):
		if not reverse:
			self.l.draw(character_data_sequence)
		else:
			self.l.draw_reverse(character_data_sequence)

	def draw_inventory(self, lines):
		self.a.draw_inventory(lines)
		self.a.refresh()
		self.a.get_key()

	def draw_char(self, coord, char):
		self.l.draw_char(coord, char)

	def draw_reverse_char(self, coord, char):
		self.l.draw_reverse_char(coord, char)

	def drawline(self, *a, **k):
		self.l.draw_line(*a, **k)

	def draw_star(self, *a, **k):
		self.l.draw_star(*a, **k)

	def draw_block(self, *a, **k):
		self.l.draw_block(*a, **k)

	def draw_path(self, iterator):
		for x in iterator:
			self.draw_block(x, COLOR.BASE_GREEN)
			if DEBUG.PATH_STEP: self.get_key()
		if not DEBUG.PATH_STEP: self.get_key()

	def suspend(self):
		self.a.suspend()

	def get_future_time(self, delay=GAME.ANIMATION_DELAY):
		return time.time() + delay

	def _selective_getch(self, char_set):
		self.refresh()
		c = None
		while c not in char_set:
			c = self.a.get_key()
		return c
