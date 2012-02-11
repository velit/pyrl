import const.game as GAME
import const.colors as COLOR

from window.pyrl_window import PyrlWindow
from window.message import MessageBar
from window.status import StatusBar
from window.level import LevelWindow


def init_global_io(*a, **k):
	global io
	io = IO(*a, **k)

class IO(object):

	def __init__(self, WindowImplementation, root_window, msg_bar_size=GAME.MSG_BAR_SIZE, status_bar_size=GAME.STATUS_BAR_SIZE):
		self.a = PyrlWindow(WindowImplementation(root_window))
		self.rows, self.cols = self.a.get_dimensions()

		self.level_rows = self.rows - msg_bar_size - status_bar_size
		self.level_cols = self.cols

		self.m = MessageBar(WindowImplementation(self.a.subwindow(msg_bar_size, self.cols, 0, 0)))
		self.l = LevelWindow(WindowImplementation(self.a.subwindow(self.level_rows, self.cols, msg_bar_size, 0)))
		self.s = StatusBar(WindowImplementation(self.a.subwindow(status_bar_size, self.cols, self.rows - status_bar_size, 0)))

	def clear_level_buffer(self, *a, **k):
		self.l.clear(*a, **k)

	def draw(self, *a, **k):
		self.l.draw(*a, **k)

	def drawline(self, *a, **k):
		self.l.draw_line(*a, **k)

	def getch(self):
		self.refresh()
		return self.l.getch()

	def getch_print(self, print_str):
		self.msg(print_str)
		return self.getch()

	def notify(self, *a):
		if len(a) > 1:
			self.msg(a)
		else:
			self.msg(*a)
		self.refresh()
		return self.l.sel_getch(char_list=GAME.DEFAULT)

	def sel_getch(self, print_str=None, *a, **k):
		if print_str is not None:
			self.msg(print_str)
			self.refresh()
		return self.l.sel_getch(None, *a, **k)

	def msg(self, *a):
		if len(a) > 1:
			self.m.queue_msg(a)
		else:
			self.m.queue_msg(*a)

	def refresh(self):
		self.m.prepare_flush()
		self.s.prepare_flush()
		self.l.prepare_flush()
		self.a.flush()

	def draw_star(self, *a, **k):
		self.l.draw_star(*a, **k)

	def draw_block(self, *a, **k):
		self.l.draw_block(*a, **k)

	def draw_char(self, *a, **k):
		self.l.draw_char(*a, **k)

	def draw_path(self, iterator):
		for x in iterator:
			self.draw_block(x, COLOR.GREEN)
		self.getch()
