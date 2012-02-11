import const.game as GAME
import const.keys as KEY
import const.colors as COLOR
import curses

from itertools import imap

CURSES_COLOR = {}
CURSES_KEYS = {}

def init_module():
	curses.curs_set(0)

	c = CURSES_COLOR
	k = CURSES_KEYS
	for x in xrange(7):
		curses.init_pair(x + 1, x, 0)

	c[COLOR.GRAY] = curses.color_pair(0)
	c[COLOR.BLACK_ON_BLACK] = curses.color_pair(1)
	c[COLOR.RED] = curses.color_pair(2)
	c[COLOR.GREEN] = curses.color_pair(3)
	c[COLOR.BROWN] = curses.color_pair(4)
	c[COLOR.BLUE] = curses.color_pair(5)
	c[COLOR.PURPLE] = curses.color_pair(6)
	c[COLOR.CYAN] = curses.color_pair(7)

	c[COLOR.WHITE] = curses.color_pair(0) | curses.A_BOLD
	c[COLOR.BLACK] = curses.color_pair(1) | curses.A_BOLD
	c[COLOR.LIGHT_RED] = curses.color_pair(2) | curses.A_BOLD
	c[COLOR.LIGHT_GREEN] = curses.color_pair(3) | curses.A_BOLD
	c[COLOR.YELLOW] = curses.color_pair(4) | curses.A_BOLD
	c[COLOR.LIGHT_BLUE] = curses.color_pair(5) | curses.A_BOLD
	c[COLOR.LIGHT_PURPLE] = curses.color_pair(6) | curses.A_BOLD
	c[COLOR.LIGHT_CYAN] = curses.color_pair(7) | curses.A_BOLD

	c[COLOR.NORMAL] = curses.A_NORMAL

	_temp = {}
	for key, value in c.iteritems():
		_temp[key + COLOR.MAKE_REVERSE] = value | curses.A_REVERSE
	c.update(_temp)

	c[COLOR.BLINK] = curses.A_BLINK
	c[COLOR.BOLD] = curses.A_BOLD
	c[COLOR.DIM] = curses.A_DIM
	c[COLOR.REVERSE] = curses.A_REVERSE
	c[COLOR.STANDOUT] = curses.A_STANDOUT
	c[COLOR.UNDERLINE] = curses.A_UNDERLINE

	k[curses.KEY_LEFT] = KEY.LEFT
	k[curses.KEY_RIGHT] = KEY.RIGHT 
	k[curses.KEY_UP] = KEY.UP
	k[curses.KEY_DOWN] = KEY.DOWN


class CursesWindow(object):

	def __init__(self, derwin):
		self.w = derwin
		self.w.keypad(True)
		self.rows, self.cols = self.w.getmaxyx()

	def addch(self, y, x, char):
		symbol, color = char
		if y != self.rows - 1 or x != self.cols - 1:
			self.w.addch(y, x, symbol.encode(u"ascii"), CURSES_COLOR[color])
		else:
			self.w.insch(y, x, symbol.encode(u"ascii"), CURSES_COLOR[color])

			# Writing to the last cell of a window raises an exception because
			# the automatic cursor move to the next cell is illegal. insch avoids
			# this but it can only be used on the last cell because it moves the line

	def addstr(self, y, x, string, color=None):
		if color is not None:
			self.w.addstr(y, x, string.encode(u"ascii"), CURSES_COLOR[color])
		else:
			self.w.addstr(y, x, string.encode(u"ascii"))

	def getch(self):
		ch = self.w.getch()
		if ch in CURSES_KEYS:
			return CURSES_KEYS[ch]
		else:
			try:
				key = chr(ch)
				return key
			except ValueError:
				return ch

	def clear(self):
		self.w.erase()
		self.w.move(0, 0)

	def prepare_flush(self):
		self.w.noutrefresh()

	def flush(self):
		curses.doupdate()

	def get_dimensions(self):
		return self.w.getmaxyx()

	def subwindow(self, nlines, ncols, y, x):
		return self.w.derwin(nlines, ncols, y, x)

	def move(self, y, x):
		self.w.move(y, x)

	def get_cursor_pos(self):
		return self.w.getyx()

	def _getstr(self, print_str=None):
		self.clear_and_print(print_str)
		curses.echo()
		return_str = self.w.getstr().decode(GAME.ENCODING)
		curses.noecho()
		return return_str

	def getbool(self, print_str=None, default=False):
		while True:
			input = self.sel_getch(print_str + u" [T/F]: ",
					list(imap(ord, u"01fFtT\n")))
			if input in list(imap(ord, u"0fF")):
				return False
			elif input in list(imap(ord, u"1tT")):
				return True
			else:
				return default

	def getchar(self, print_str=None, default=u"."):
		while True:
			input = self._getstr(print_str + u" [char]: ")
			if input == u"":
				return default
			elif len(input) == 1:
				return input

	def getcolor(self, print_str=None, default=u"normal"):
		while True:
			#TODO: might want to change to getch?
			input = self._getstr(print_str + u"[white/normal/black/red/green/"
										u"yellow/blue/purple/cyan/light_*]: ")
			if input == u"":
				return default
			elif input in CURSES_COLOR:
				return input

	def getint(self, print_str=None, default=0):
		while True:
			input = self._getstr(print_str + u" [int]: ")
			if input == u"":
				return default
			try:
				return int(input)
			except ValueError:
				pass

	def getstr(self, print_str=None, default=u""):
		str_ = self._getstr(print_str + u" [str]: ")
		return str_ if str_ != u"" else default
