import curses

from message_window import MessageBar
from status_window import StatusBar
from level_window import LevelWindow
from window import Window
from colors import init_colors
from const.game import STATUS_BAR_SIZE, MSG_BAR_SIZE


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

	def __init__(self, curs_window, msg_bar_size=MSG_BAR_SIZE,
				status_bar_size=STATUS_BAR_SIZE):
		self.w = curs_window
		self.w.keypad(1)
		self.rows, self.cols = self.w.getmaxyx()

		self.level_rows = self.rows - msg_bar_size - status_bar_size
		self.level_cols = self.cols

		self.m = MessageBar(self.w.derwin(msg_bar_size, 0, 0, 0))
		self.s = StatusBar(
			self.w.derwin(status_bar_size, 0, self.rows - status_bar_size, 0))
		self.l = LevelWindow(
			self.w.derwin(self.level_rows, 0, msg_bar_size, 0))
		self.a = Window(self.w)

	def clear_level(self, *a, **k):
		self.l.clear(*a, **k)

	def clearlos(self, *a, **k):
		self.l.clearlos(*a, **k)

	def drawlevel(self, *a, **k):
		self.l.drawlevel(*a, **k)

	def drawmemory(self, *a, **k):
		self.l.drawmemory(*a, **k)

	def drawtilemap(self, *a, **k):
		self.l.drawtilemap(*a, **k)

	def draw_menu(self, *a, **k):
		return self.l.draw_menu(*a, **k)

	def draw_h_menu(self, *a, **k):
		return self.m.draw_h_menu(*a, **k)

	def drawlos(self, *a, **k):
		self.l.drawlos(*a, **k)

	def drawline(self, *a, **k):
		self.l.drawline(*a, **k)

	def getbool(self, *a, **k):
		return_ =  self.m.getbool(*a, **k)
		self.refresh()
		return return_

	def getchar(self, *a, **k):
		return_ =  self.m.getchar(*a, **k)
		self.refresh()
		return return_

	def getcolor(self, *a, **k):
		return_ =  self.m.getcolor(*a, **k)
		self.refresh()
		return return_

	def getint(self, *a, **k):
		return_ =  self.m.getint(*a, **k)
		self.refresh()
		return return_

	def getstr(self, *a, **k):
		return_ =  self.m.getstr(*a, **k)
		self.refresh()
		return return_

	def getch(self, *a, **k):
		self.refresh()
		return self.l.getch(*a, **k)

	def sel_getch(self, print_str=None, *a, **k):
		if print_str is not None:
			curses.curs_set(0)
			self.msg(print_str)
			self.refresh()
		return_ = self.l.sel_getch(None, *a, **k)
		if print_str is not None:
			curses.curs_set(1)
			self.refresh()
		return return_

	def msg(self, *a, **k):
		self.m.queue_msg(*a, **k)

	def refresh(self):
		self.m.update()
		self.s.update()
		self.l.update()
		curses.doupdate()

	def drawstar(self, *a, **k):
		self.l.drawstar(*a, **k)

	def drawblock(self, *a, **k):
		self.l.drawblock(*a, **k)

	def drawpath(self, iterator):
		curses.curs_set(0)
		for x in iterator:
			self.drawstar(x)
		self.getch()
		curses.curs_set(1)
