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
		self.s = StatusBar(self.w.derwin(status_bar_size, 0, self.rows - status_bar_size, 0), self)
		self.l = LevelWindow(self.w.derwin(self.level_rows, 0, msg_bar_size, 0), self)
		self.a = Window(self.w)

	def drawMemoryMap(self, map):
		self.l.drawMemoryMap(map)

	def drawMap(self, map):
		self.l.drawMap(map)

	def drawLos(self, visibility, level):
		self.l.drawLos(visibility, level)

	def clearLos(self, visibility, level):
		self.l.clearLos(visibility, level)

	def drawLine(self, startSquare, targetSquare, char=None):
		self.l.drawLine(self, startSquare, targetSquare, char=None)

	def getstr(self, str):
		self.m.getstr(str)

	def queueMsg(self, str):
		self.m.queueMsg(str)
	
	def msg(self, string):
		self.m.queueMsg(str(string))
	
	def refresh(self):
		self.m.update()
		self.s.update()
		self.l.update()
		curses.doupdate()

	def drawStar(self, square, col=None):
		if col is None:
			col = color["green"]
		self.l.drawStar(square, col)
	
	def drawBlock(self, square, col=None):
		if col is None:
			col = color["blue"]
		self.l.drawBlock(square, col)

	def getch(self, y=None, x=None):
		self.refresh()
		if y is not None and x is not None:
			return self.l.getch(y,x)
		else:
			return self.l.getch()

	def getCharacters(self, list):
		self.refresh()
		return self.l.getCharacters(list)
