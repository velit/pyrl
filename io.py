import curses
import _curses

from colors import color
from message import MessageBar
from status import StatusBar
from level_window import LevelWindow
from window import Window
from char import Char

class IO(object):
	def __init__(self, window, msg_bar_size=2, status_bar_size=2):
		self.w = window
		self.w.keypad(1)
		self.rows, self.cols = self.w.getmaxyx()
		self.level_rows = self.rows - msg_bar_size - status_bar_size
		self.level_cols = self.cols

		self.m = MessageBar(self.w.derwin(msg_bar_size, 0, 0, 0), self)
		self.s = StatusBar(self.w.derwin(status_bar_size, 0,
							self.rows - status_bar_size, 0), self)
		self.l = LevelWindow(self.w.derwin(self.level_rows, 0,
											msg_bar_size, 0), self)
		self.a = Window(self.w)

	def drawmap(self, level):
		self.l.drawmap(level)

	def drawmemory(self, level):
		self.l.drawmemory(level)

	def drawlos(self, visibility, level, reverse=False):
		self.l.drawlos(visibility, level, reverse)

	def clearlos(self, visibility, level):
		self.l.clearlos(visibility, level)

	def drawline(self, startSquare, targetsquare, char=None):
		self.l.drawline(self, startSquare, targetsquare, char=None)

	def getstr(self, str):
		self.m.getstr(str)

	def msg(self, string):
		self.m.queue_msg(str(string))
	
	def refresh(self):
		self.m.update()
		self.s.update()
		self.l.update()
		curses.doupdate()

	def drawstar(self, square, color_=None):
		if color_ is None:
			color_ = color["green"]
		self.l.drawstar(square, color_)
	
	def drawblock(self, square, color_=None):
		if color_ is None:
			color_ = color["blue"]
		self.l.drawblock(square, color_)

	def getch(self, y=None, x=None):
		self.refresh()
		if y is not None and x is not None:
			return self.l.getch(y,x)
		else:
			return self.l.getch()

	def getch_from_list(self, list=map(ord, ('Y', 'y', 'N', 'n', '\n', ' ')),
					str=None):
		if str:
			self.msg(str)
		self.refresh()
		return self.l.getch_from_list()

	def drawpath(self, iterator):
		curses.curs_set(0)
		for x in iterator:
			self.drawstar(x)
		self.getch()
		curses.curs_set(1)
