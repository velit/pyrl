import curses
from char import Char
from colors import color

class Window(object):
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

	def clear_and_print(self, str=None):
		self.clear()
		if str is not None:
			self.w.addstr(str)

	def _getstr(self, print_str=None):
		self.clear_and_print(print_str)
		curses.echo()
		str = self.w.getstr()
		curses.noecho()
		return str

	def getstr(self, str=None):
		return self._getstr(str + " [str]: ")

	def getint(self, print_str=None):
		while True:
			input = self._getstr(print_str + " [int]: ")
			try:
				return int(input)
			except ValueError:
				pass

	def getbool(self, print_str=None):
		while True:
			input = self._getstr(print_str + " [1/0]: ")
			if input == "1":
				return True
			elif input == "0":
				return False

	def getchar(self, print_str=None):
		while True:
			input = self._getstr(print_str + " [char]: ")
			if len(input) == 1:
				return input

	def getcolor(self, print_str=None):
		while True:
			input = self._getstr(print_str + " [white/normal/black, red/green/yellow/blue/purple/cyan/, light_red/light_*]: ")
			if input in color:
				return color[input]

	def move(self, y, x):
		self.w.move(y, x)

	def refresh(self):
		self.update()
		curses.doupdate()

	def addstr(self, str):
		self.w.addstr(str)

	def _getch(self):
		return self.w.getch()

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
