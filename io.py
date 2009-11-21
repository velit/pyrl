import curses
import _curses
from colors import color
from message import MessageBar
from status import StatusBar
from level_window import LevelWindow
from char import Char

class IO:
	def __init__(self, window, msg_bar_size=2, status_bar_size=2):
		self.w = window
		self.w.keypad(1)
		self.rows, self.cols = self.w.getmaxyx()
		self.level_rows = self.rows - msg_bar_size - status_bar_size
		self.level_cols = self.cols

		self.m = MessageBar(self.w.derwin(msg_bar_size, 0, 0, 0), self)
		self.s = StatusBar(self.w.derwin(status_bar_size, 0, self.rows - status_bar_size, 0), self)
		self.l = LevelWindow(self.w.derwin(self.level_rows, 0, msg_bar_size, 0), self)

	def drawMemoryMap(self, map):
		self.l.drawMemoryMap(map)

	def drawMap(self, map):
		self.l.drawMap(self, map)

	def drawLos(self):
		self.l.drawLos()

	def clearLos(self):
		self.l.clearLos()

	def drawLine(self, startSquare, targetSquare, char=None):
		self.l.drawLine(self, startSquare, targetSquare, char=None)

	def getStr(self, str):
		self.clear()
		self.w.addstr(0,0,str)
		curses.echo()
		a = self.w.getstr()
		curses.noecho()
		return a

	def queueMsg(self, str):
		self.m.queueMsg(str)
	
	def clearMsgArea(self):
		self.m.clearMsgArea()

	def clear(self):
		self.w.clear()

	def refreshWindows(self):
		self.m.update()
		self.s.update()
		self.l.update()
		curses.doupdate()

	def getch(self, y=None, x=None):
		self.refreshWindows()
		if y is not None:
			self.l.w.move(y,x)
		c = self.l.w.getch()
		self.clearMsgArea()
		return c

	def getCharacters(self, list):
		c = None
		self.refreshWindows()
		while c not in list:
			c = self.l.w.getch()
		self.clearMsgArea()
		return c

	def getSelection(self, option_names, decisions, option_values=None, hilite_values=True):
		n = option_names
		v = option_values
		curses.curs_set(0)
		self.clear()
		self.w.move(0,0)

		#printing options
		for i in range(len(n)):
			self.w.move(i, 0)
			self.w.addstr(n[i])
			if v is not None and i < len(v):
				self.w.addstr(" ")
				if isinstance(v[i], Char):
					self.w.addstr(v[i].symbol, v[i].color)
				else:
					self.w.addstr(v[i])
		#ui
		i = 0
		while True:
			if v is not None and i < len(v) and hilite_values:
				y = i
				x = len(n[i] + " ")
				if isinstance(v[i], Char):
					self.w.addstr(y, x, v[i].symbol, v[i].color | color["reverse"])
					c = self.w.getch()
					self.w.addstr(y, x, v[i].symbol, v[i].color)
				else:
					self.w.addstr(y, x, v[i], color["reverse"])
					c = self.w.getch()
					self.w.addstr(y, x, v[i])
			else:
				y = i
				x = 0
				self.w.addstr(y, x, n[i], color["reverse"])
				c = self.w.getch()
				self.w.addstr(y, x, n[i])

			if c == curses.KEY_DOWN:
				i += 1
				if i >= len(n):
					i -= len(n)
				if decisions[i] is None:
					i+= 1
					if i >= len(n):
						i -= len(n)
			elif c == curses.KEY_UP:
				i -= 1
				if i < 0:
					i += len(n)
				if decisions[i] is None:
					i -= 1
					if i < 0:
						i += len(n)
			elif c == ord('\n'):
				curses.curs_set(1)
				return decisions[i]
