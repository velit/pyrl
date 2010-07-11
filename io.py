import curses
import _curses

from colors import color
from w_message import MessageBar
from w_status import StatusBar
from w_level import LevelWindow
from window import Window
from char import Char
from constants import YES, NO, DEFAULT

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

	def drawmenu(self, words, returns):
		return self.m.draw_h_menu(words, returns)

	def drawlos(self, visibility, level, *reverse):
		self.l.drawlos(visibility, level, *reverse)

	def clearlos(self, visibility, level):
		self.l.clearlos(visibility, level)

	def drawline(self, startSquare, targetsquare, *char):
		self.l.drawline(self, startSquare, targetsquare, *char)

	def getstr(self, *str):
		self.m.getstr(*str)

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

	def getch(self, *args, **keys):
		self.refresh()
		return self.l.getch(*args, **keys)

	def getch_from_list(self, list=YES | NO | DEFAULT, str=None):
		if str is not None:
			self.msg(str)
		self.refresh()
		return self.l.getch_from_list(list)

	def drawpath(self, iterator):
		curses.curs_set(0)
		for x in iterator:
			self.drawstar(x)
		self.getch()
		curses.curs_set(1)
