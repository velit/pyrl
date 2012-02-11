import curses

import const.game as GAME

from window.pyrl_window import PyrlWindow
from window.curses_window import CursesWindow, init_colors
from window.message import MessageBar
from window.status import StatusBar
from window.level import LevelWindow


def init_io_module(*a, **k):
	init_colors()
	global io
	io = IO(*a, **k)
	curses.curs_set(0)

class IO(object):

	def __init__(self, curs_window, msg_bar_size=GAME.MSG_BAR_SIZE, status_bar_size=GAME.STATUS_BAR_SIZE):
		self.w = curs_window
		self.rows, self.cols = self.w.getmaxyx()

		self.level_rows = self.rows - msg_bar_size - status_bar_size
		self.level_cols = self.cols

		self.m = MessageBar(CursesWindow(self.w.derwin(msg_bar_size, 0, 0, 0)))
		self.s = StatusBar(CursesWindow(self.w.derwin(status_bar_size, 0, self.rows - status_bar_size, 0)))
		self.l = LevelWindow(CursesWindow(self.w.derwin(self.level_rows, 0, msg_bar_size, 0)))
		self.a = PyrlWindow(CursesWindow(self.w))

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
			self.draw_block(x, u"green")
		self.getch()
