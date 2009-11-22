import curses
from char import Char
from colors import color

class Window:
	def __init__(self, window):
		self.w = window
		self.w.keypad(1)

	def clear(self):
		self.w.erase()
		self.w.move(0,0)

	def update(self):
		self.w.noutrefresh()

	def getch(self, y=None, x=None):
		if y is None and x is None:
			return self.w.getch()
		else:
			return self.w.getch(y, x)

	def getCharacters(self, cont):
		c = self.w.getch()
		while c not in cont:
			c = self.w.getch()
		return c

	def getstr(self, str=None):
		self.clear()
		if str is not None:
			self.w.addstr(str)
		curses.echo()
		a = self.w.getstr()
		curses.noecho()
		return a

	def move(self, y, x):
		self.w.move(y, x)

	def refresh(self):
		self.update()
		curses.doupdate()

	def addstr(self, str):
		self.w.addstr(str)

	def getSelection(self, option_names, decisions, option_values=None, hilite_values=True):
		n = option_names
		v = option_values
		curses.curs_set(0)
		self.clear()

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
		while decisions[i] is None:
			i += 1
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
				while decisions[i] is None:
					i+= 1
					if i >= len(n):
						i -= len(n)
			elif c == curses.KEY_UP:
				i -= 1
				if i < 0:
					i += len(n)
				while decisions[i] is None:
					i -= 1
					if i < 0:
						i += len(n)
			elif c == ord('\n'):
				curses.curs_set(1)
				return decisions[i]
