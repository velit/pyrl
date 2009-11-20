import curses
import _curses
from colors import color
from message import MessageBar
from status import StatusBar
from level_window import LevelWindow

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
		return self.m.getStr(str)

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

	def getSelection(self, options):
		curses.curs_set(0)
		self.clear()
		selection = 0
		self.w.move(0,0)
		for option in options:
			self.w.addstr(option[0]+"\n")
		while True:
			self.w.addstr(selection, 0, options[selection][0], color["reverse"])
			c = self.w.getch()
			self.w.addstr(selection, 0, options[selection][0])
			if c == curses.KEY_DOWN:
				selection += 1
				if selection >= len(options):
					selection -= len(options)
			elif c == curses.KEY_UP:
				selection -= 1
				if selection < 0:
					selection += len(options)
			elif c == ord('\n'):
				curses.curs_set(1)
				return options[selection][1]()
