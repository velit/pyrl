import curses
import colors
import const.game as GAME


class CursesWindow():

	def __init__(self, derwin):
		self.w = derwin
		self.rows, self.cols = self.w.getmaxyx()

	def addch(self, y, x, char):
		symbol, color = char
		if y != self.rows - 1 or x != self.cols - 1:
			self.w.addch(y, x, symbol.encode("ascii"), colors.CURSES_COLOR[color])
		else:
			self.w.insch(y, x, symbol.encode("ascii"), colors.CURSES_COLOR[color])

			# Writing to the last cell of a window raises an exception because
			# the automatic cursor move to the next cell is illegal. insch avoids
			# this but it can only be used on the last cell because it moves the line

	def addstr(self, string, color=None):
		if color is not None:
			self.w.addstr(string, colors.CURSES_COLOR[color])
		else:
			self.w.addstr(string)

	def mvaddstr(self, y, x, string, color=None):
		if color is not None:
			self.w.addstr(y, x, string, colors.CURSES_COLOR[color])
		else:
			self.w.addstr(y, x, string)

	def clear(self):
		self.w.erase()
		self.w.move(0, 0)

	def prepare_flush(self):
		self.w.noutrefresh()

	def flush(self):
		curses.doupdate()

	def move(self, y, x):
		self.w.move(y, x)

	def getch(self, coord=()):
		return self.w.getch(*coord)

	def get_cursor_pos(self):
		return self.w.getyx()

	def get_dimensions(self):
		return self.w.getmaxyx()

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
