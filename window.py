import curses
from char import Char
from colors import color
from constants import YES, NO, DEFAULT

class Window(object):
	def __init__(self, window):
		self.w = window
		self.w.keypad(1)

	def clear(self):
		self.w.erase()
		self.w.move(0,0)

	def update(self):
		self.w.noutrefresh()

	def getch(self, y=None, x=None, str=None):
		if str:
			self.clear_and_print(str)
		if y is None and x is None:
			return self.w.getch()
		else:
			return self.w.getch(y, x)

	def getch_from_list(self, list=YES | NO | DEFAULT, str=None):
		if str:
			self.clear_and_print(str)
		c = self.w.getch()
		while c not in list:
			c = self.w.getch()
		return c

	def clear_and_print(self, str):
		self.clear()
		self.w.addstr(str)

	def _getstr(self, print_str=None):
		self.clear_and_print(print_str)
		curses.echo()
		str = self.w.getstr()
		curses.noecho()
		return str

	def getbool(self, print_str=None):
		while True:
			input = self._getstr(print_str + " [1/0]: ")
			if input == "" or input == "0":
				return False
			elif input == "1":
				return True

	def getchar(self, print_str=None):
		while True:
			input = self._getstr(print_str + " [char]: ")
			if input == "":
				return " "
			elif len(input) == 1:
				return input

	def getcolor(self, print_str=None):
		while True:
			input = self._getstr(print_str + "[white/normal/black/red/green/"
										"yellow/blue/purple/cyan/light_*]: ")
			if input == "":
				return color["normal"]
			elif input in color:
				return color[input]

	def getint(self, print_str=None):
		while True:
			input = self._getstr(print_str + " [int]: ")
			if input == "":
				return 0
			try:
				return int(input)
			except ValueError:
				pass

	def getstr(self, str=None):
		return self._getstr(str + " [str]: ")

	def getmaxyx(self):
		return self.w.getmaxyx()

	def move(self, y, x):
		self.w.move(y, x)

	def refresh(self):
		self.update()
		curses.doupdate()

	def addstr(self, str):
		self.w.addstr(str)

	def _getch(self):
		return self.w.getch()

	def _print_selection_values(self, i, x, n, v, reverse=True):
		len_n = len(n[i])
		if v is not None and i < len(v) and reverse:
			self.w.addstr(i, len_n, " "*(x-len_n), color["reverse"])
			if isinstance(v[i], Char):
				self.w.addstr(i, x, v[i].symbol, v[i].color | color["reverse"])
			else:
				self.w.addstr(i, x, v[i], color["reverse"])
		elif v is not None and i < len(v):
			self.w.addstr(i, len_n, " "*(x-len_n))
			if isinstance(v[i], Char):
				self.w.addstr(i, x, v[i].symbol, v[i].color)
			else:
				self.w.addstr(i, x, v[i])

	def get_selection(self, option_names, decisions, option_values=None,
					keys=(), i=0):
		n = option_names
		v = option_values
		curses.curs_set(0)
		self.clear()
		
		# go through names which have values on the same line and match the
		# indent level to the longest name
		indent = 0
		for row_i in range(len(n)):
			try:
				if v[row_i] and len(n[row_i]) > indent:
					indent = len(n[row_i])
			except:
				pass

		# if we had values and thus an indent, add one space so the options
		# wont be glued together
		if indent: indent += 1

		# print all the names and their values if there are any
		for y, name in enumerate(n):
			if isinstance(name, Char):
				self.w.addstr(y, 0, name.symbol, name.color)
			else:
				self.w.addstr(y, 0, name)

		if v is not None:
			for y, name in enumerate(v):
				if name is not None:
					if isinstance(name, Char):
						self.w.addstr(y, indent, name.symbol, name.color)
					else:
						self.w.addstr(y, indent, name)

		#ui
		while decisions[i] is None:
			i += 1
			if i >= len(n):
				i = 0
		while True:
			self.w.addstr(i, 0, n[i], color["reverse"])
			self._print_selection_values(i, indent, n, v)
			c = self.w.getch()
			self._print_selection_values(i, indent, n, v, False)
			self.w.addstr(i, 0, n[i])

			if c in keys:
				return keys[c]
			elif c == curses.KEY_DOWN:
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
			elif c == ord('\n') or c == ord('>'):
				curses.curs_set(1)
				return decisions[i]
