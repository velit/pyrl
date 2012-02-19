import const.debug as DEBUG
import const.game as GAME
import const.keys as KEY
import const.colors as COLOR

from window.pyrl_window import PyrlWindow
from window.message import MessageBar
from window.status import StatusBar
from window.level import LevelWindow


class Front(object):

	def __init__(self, cursor_lib, root_window, msg_bar_size=GAME.MSG_BAR_SIZE, status_bar_size=GAME.STATUS_BAR_SIZE):
		self.a = PyrlWindow(cursor_lib, root_window)
		self.rows, self.cols = self.a.get_dimensions()

		self.level_rows = self.rows - msg_bar_size - status_bar_size
		self.level_cols = self.cols

		self.m = self.a.SubWindow(MessageBar, msg_bar_size, self.cols, 0, 0)
		self.l = self.a.SubWindow(LevelWindow, self.level_rows, self.cols, msg_bar_size, 0)
		self.s = self.a.SubWindow(StatusBar, status_bar_size, self.cols, status_bar_size + self.level_rows, 0)

	def getch(self):
		self.refresh()
		return self.a.getch()

	def getch_print(self, print_str):
		self.msg(print_str)
		return self.getch()

	def selective_getch(self, char_seq):
		while True:
			c = self.getch()
			if c in char_seq:
				return c

	def ask(self, string, char_seq=KEY.GROUP_ALL):
		self.msg(string)
		return self.selective_getch(char_seq)

	def notify(self, *a):
		self.msg(*a)
		return self.selective_getch(KEY.GROUP_ALL)

	def msg(self, *a):
		self.m.queue_msg(*a)

	def refresh(self):
		self.m.prepare_flush()
		self.l.prepare_flush()
		self.s.prepare_flush()
		self.a.flush()

	def clear_level_buffer(self, *a, **k):
		self.l.clear(*a, **k)

	def draw(self, character_data_sequence, reverse=False):
		if not reverse:
			self.l.draw(character_data_sequence)
		else:
			self.l.draw_reverse(character_data_sequence)

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
			self.draw_block(x, COLOR.GREEN)
			if DEBUG.PATH_STEP: self.getch()
		if not DEBUG.PATH_STEP: self.getch()
