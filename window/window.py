import curses
import menu
import menu_h
import colors
import const.game as GAME


class Window:

	def __init__(self, window):
		self.w = window
		self.w.keypad(1)
		self.rows, self.cols = self.w.getmaxyx()

	def clear(self):
		self.w.erase()
		self.w.move(0, 0)

	def update(self):
		self.w.noutrefresh()

	def addch(self, y, x, char):
		symbol, color = char
		if (y, x) == (self.rows - 1, self.cols - 1):
			try:
				self.w.addch(y, x, symbol.encode("ascii"), colors.CURSES_COLOR[color])
			except curses.error:
				pass
			# Writing to the last cell of a window raises an exception because
			# the automatic cursor move to the next cell is illegal, this is
			# the only way to write to the last cell in the current wrapper
			# according to my knowledge
		else:
			self.w.addch(y, x, symbol.encode("ascii"), colors.CURSES_COLOR[color])

	def getch(self, *a, **k):
		return self.w.getch(*a, **k)

	def gety(self):
		return self.w.getyx()[0]

	def getx(self):
		return self.w.getyx()[1]

	def getyx(self):
		return self.w.getyx()

	def notify(self, print_str=None):
		return self.sel_getch(print_str, char_list=GAME.DEFAULT)

	def sel_getch(self, print_str=None, char_list=GAME.ALL):
		if print_str is not None:
			self.clear_and_print(print_str)
		c = self.getch()
		while c not in char_list:
			c = self.getch()
		return c

	def clear_and_print(self, print_str):
		self.clear()
		self.w.addstr(print_str)

	def _getstr(self, print_str=None):
		self.clear_and_print(print_str)
		curses.echo()
		return_str = self.w.getstr().decode(GAME.ENCODING)
		curses.noecho()
		return return_str

	def getbool(self, print_str=None, default=False):
		while True:
			input = self.sel_getch(print_str + " [T/F]: ",
					list(map(ord, "01fFtT\n")))
			if input in list(map(ord, "0fF")):
				return False
			elif input in list(map(ord, "1tT")):
				return True
			else:
				return default

	def getchar(self, print_str=None, default="."):
		while True:
			input = self._getstr(print_str + " [char]: ")
			if input == "":
				return default
			elif len(input) == 1:
				return input

	def getcolor(self, print_str=None, default="normal"):
		while True:
			#TODO: might want to change to getch?
			input = self._getstr(print_str + "[white/normal/black/red/green/"
										"yellow/blue/purple/cyan/light_*]: ")
			if input == "":
				return default
			elif input in colors.d:
				return input

	def getint(self, print_str=None, default=0):
		while True:
			input = self._getstr(print_str + " [int]: ")
			if input == "":
				return default
			try:
				return int(input)
			except ValueError:
				pass

	def getstr(self, print_str=None, default=""):
		str_ = self._getstr(print_str + " [str]: ")
		return str_ if str_ != "" else default

	def getmaxyx(self):
		return self.w.getmaxyx()

	def move(self, y, x):
		self.w.move(y, x)

	def refresh(self):
		self.update()
		curses.doupdate()

	def addstr(self, *a, **k):
		if len(a) == 4 or len(a) == 2:
			self.w.addstr(*(a[:-1] + (colors.d[a[-1]],)))
		else:
			self.w.addstr(*a, **k)

	def wrap_print(self, words):
		self.clear()
		str = words
		cur_line = 0
		skip_all = False
		while True:
			if cur_line < self.lines - 1:
				if len(str) < self.width:
					self.w.addstr(cur_line, 0, str)
					break
				else:
					a = self.wrapper.wrap(str)
					self.w.addstr(cur_line, 0, a[0])
					str = " ".join(a[1:])
					cur_line += 1
			elif cur_line == self.lines - 1:
				if len(str) < self.width:
					self.w.addstr(cur_line, 0, str)
					break
				else:
					a = self.last_line_wrapper.wrap(str)
					self.w.addstr(cur_line, 0, a[0] + self.more_str)
					if not skip_all:
						c = self.getch_from_list(list=(ord('\n'), ord(' ')))
						if c == ord('\n'):
							skip_all = True
					str = " ".join(a[1:])
					cur_line = 0
					self.clear()
		self.msgqueue = ""

	def draw_menu(self, *a, **k):
		return menu.draw(self, *a, **k)

	def draw_h_menu(self, *a, **k):
		return menu_h.draw(self, *a, **k)
