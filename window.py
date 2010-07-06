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

	def _get_indentation_level(self, rows):
		indent = 0
		# if lines in rows has second words, find out indentation level
		ii = isinstance
		if any(not ii(l, str) for l in rows):
			for l in rows:
				if not ii(l, str):
					if ii(l[0], Char):
						indent = max(indent, 1)
					else:
						indent = max(indent, len(l[0]))
			indent += 1 #leave room between words
		return indent

	def _print_selection_word(self, y, x, word, reverse=False):
		r = color["reverse"] if reverse else color["normal"]
		if isinstance(word, Char):
			self.w.addstr(y, x, word.symbol, word.color | r)
		else:
			self.w.addstr(y, x, str(word), r)

	def _print_selection_line(self, y, line, indent, reverse=False):
		if not isinstance(line, str):
			l = len(line[0])
			self._print_selection_word(y, 0, line[0], reverse)
			self._print_selection_word(y, l, " "*(indent-l), reverse)
			self._print_selection_word(y, indent, line[1], reverse)
		else:
			self._print_selection_word(y, 0, line, reverse)

	def _print_selection(self, rows, indent):
		for y, line in enumerate(rows):
			self._print_selection_line(y, line, indent)

	def _print_select_getch(self, y, line, indent):
		self._print_selection_line(y, line, indent, True)
		c = self.w.getch()
		self._print_selection_line(y, line, indent, False)
		return c

	def _roll_i(self, i, n, d, a=0):
		i += a
		if i >= len(n):
			i = 0
		elif i < 0:
			i = len(n)-1

		s = a if a else 1
		while d[i] is None:
			i += s
			if i >= len(n):
				i = 0
			elif i < 0:
				i = len(n)-1
		return i

	def get_selection(self, print_lines, decisions, keys=(), i=0):
		curses.curs_set(0)
		self.clear()

		n = print_lines
		d = decisions
		indent = self._get_indentation_level(n)

		self._print_selection(n, indent)

		#ui
		i = self._roll_i(i, n, d)
		while True:
			c = self._print_select_getch(i, n[i], indent)
			if c in keys:
				return keys[c]
			elif c in (curses.KEY_DOWN, ord('j')):
				i = self._roll_i(i, n, d, 1)
			elif c in (curses.KEY_UP, ord('k')):
				i = self._roll_i(i, n, d, -1)
			elif c == ord('\n') or c == ord('>'):
				curses.curs_set(1)
				return decisions[i]
