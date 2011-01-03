import curses
import _curses
import colors

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

		self.m = MessageBar(self.w.derwin(msg_bar_size, 0, 0, 0))
		self.s = StatusBar(self.w.derwin(status_bar_size, 0,
							self.rows - status_bar_size, 0))
		self.l = LevelWindow(self.w.derwin(self.level_rows, 0,
											msg_bar_size, 0))
		self.a = Window(self.w)

	def drawmap(self, map):
		self.l.drawmap(map)

	def drawmemory(self, map):
		self.l.drawmemory(map)

	def drawtilemap(self, tilemap):
		self.l.drawtilemap(tilemap)

	def drawmenu(self, words, returns):
		return self.m.draw_h_menu(words, returns)

	def drawlos(self, visibility, *color_shift):
		self.l.drawlos(visibility, *color_shift)

	def clearlos(self, visibility, level):
		self.l.clearlos(visibility, level)

	def drawline(self, startSquare, targetsquare, *char):
		self.l.drawline(self, startSquare, targetsquare, *char)

	def getstr(self, *str):
		self.refresh()
		return self.m.getstr(*str)

	def msg(self, message):
		self.m.queue_msg(str(message))
	
	def refresh(self):
		self.m.update()
		self.s.update()
		self.l.update()
		curses.doupdate()

	def drawstar(self, square, *col):
		self.l.drawstar(square, *col)
	
	def drawblock(self, square, *col):
		self.l.drawblock(square, *col)

	def getch(self, *args, **keys):
		self.refresh()
		return self.l.getch(*args, **keys)

	def sel_getch(self, print_str=None, *args, **keys):
		if print_str is not None:
			self.msg(print_str)
		self.refresh()
		return self.l.sel_getch(None, *args, **keys)

	def drawpath(self, iterator):
		curses.curs_set(0)
		for x in iterator:
			self.drawstar(x)
		self.getch()
		curses.curs_set(1)
