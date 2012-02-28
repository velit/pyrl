import const.debug as DEBUG
import const.keys as KEY
import const.colors as COLOR

from window.pyrl_window import PyrlWindow
from window.message import MessageBar
from window.status import StatusBar
from window.level import LevelWindow
from const.game import MSG_BAR_HEIGHT, STATUS_BAR_HEIGHT, LEVEL_HEIGHT, LEVEL_WIDTH


class Front(object):

	def __init__(self, cursor_lib, root_window):
		self.a = PyrlWindow(cursor_lib, root_window)

		mh, mb = self.a.sub_handle(MSG_BAR_HEIGHT, LEVEL_WIDTH, 0, 0)
		lh, lb = self.a.sub_handle(LEVEL_HEIGHT, LEVEL_WIDTH, MSG_BAR_HEIGHT, 0)
		sh, sb = self.a.sub_handle(STATUS_BAR_HEIGHT, LEVEL_WIDTH, MSG_BAR_HEIGHT + LEVEL_HEIGHT, 0)

		self.m = MessageBar(cursor_lib, mh, mb)
		self.l = LevelWindow(cursor_lib, lh, lb)
		self.s = StatusBar(cursor_lib, sh, sb)

		self.rows, self.cols = self.a.get_dimensions()

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
		self.m.update()
		self.l.update()
		self.s.update()
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
			self.draw_block(x, COLOR.BASE_GREEN)
			if DEBUG.PATH_STEP: self.getch()
		if not DEBUG.PATH_STEP: self.getch()
