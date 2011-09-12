import curses

import const.game as GAME

from window.message import MessageBar
from window.status import StatusBar
from window.level import LevelWindow
from window.window import Window
from colors import init_colors


def init_io_module(*a, **k):
	init_colors()
	Wrapper._inst = _IO(*a, **k)


class Wrapper:
	_inst = None

	def __getattr__(self, name):
		return getattr(self._inst, name)

	def __setattr__(self, name, value):
		return setattr(self._inst, name, value)

	def __delattr__(self, name):
		return delattr(self._inst, name, value)


io = Wrapper()


class _IO:

	def __init__(self, curs_window, msg_bar_size=GAME.MSG_BAR_SIZE,
				status_bar_size=GAME.STATUS_BAR_SIZE):
		self.w = curs_window
		self.w.keypad(1)
		self.rows, self.cols = self.w.getmaxyx()

		self.level_rows = self.rows - msg_bar_size - status_bar_size
		self.level_cols = self.cols

		self.m = MessageBar(self.w.derwin(msg_bar_size, 0, 0, 0))
		self.s = StatusBar(self.w.derwin(status_bar_size, 0, self.rows - status_bar_size, 0))
		self.l = LevelWindow(self.w.derwin(self.level_rows, 0, msg_bar_size, 0))
		self.a = Window(self.w)

	def clear_level_buffer(self, *a, **k):
		self.l.clear(*a, **k)

	def clearlos(self, *a, **k):
		self.l.clearlos(*a, **k)

	def draw(self, *a, **k):
		self.l.draw(*a, **k)

	def draw_menu(self, *a, **k):
		return self.l.draw_menu(*a, **k)

	def draw_h_menu(self, *a, **k):
		return self.m.draw_h_menu(*a, **k)

	def drawlos(self, *a, **k):
		self.l.drawlos(*a, **k)

	def drawline(self, *a, **k):
		self.l.draw_line(*a, **k)

	def getbool(self, *a, **k):
		return_data =  self.m.getbool(*a, **k)
		self.refresh()
		return return_data

	def getchar(self, *a, **k):
		return_data =  self.m.getchar(*a, **k)
		self.refresh()
		return return_data

	def getcolor(self, *a, **k):
		return_data =  self.m.getcolor(*a, **k)
		self.refresh()
		return return_data

	def getint(self, *a, **k):
		return_data =  self.m.getint(*a, **k)
		self.refresh()
		return return_data

	def getstr(self, *a, **k):
		return_data =  self.m.getstr(*a, **k)
		self.refresh()
		return return_data

	def getch(self, *a, **k):
		self.refresh()
		return self.l.getch(*a, **k)

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
		self.m.update()
		self.s.update()
		self.l.update()
		curses.doupdate()

	def draw_star(self, *a, **k):
		self.l.draw_star(*a, **k)

	def draw_block(self, *a, **k):
		self.l.draw_block(*a, **k)

	def draw_char(self, *a, **k):
		self.l.draw_char(*a, **k)

	def draw_path(self, iterator):
		curses.curs_set(0)
		for x in iterator:
			self.draw_block(x, "green")
		self.getch()
		curses.curs_set(1)
