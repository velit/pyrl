import const.keys as KEY
import const.colors as COLOR
import curses

class Curses256ColorDict(dict):
	def __init__(self, CURSES_ATTR):
		dict.__init__(self)
		self.pair_nr = 0
		self.CURSES_ATTR = CURSES_ATTR

	def __getitem__(self, key):
		try:
			return dict.__getitem__(self, key)
		except KeyError:
			fg, bg = key
			self.pair_nr += 1
			curses.init_pair(self.pair_nr, self.CURSES_ATTR[fg], self.CURSES_ATTR[bg])
			color_pair = curses.color_pair(self.pair_nr)
			self[key] = color_pair
			return color_pair

class CursesColorDict(dict):

	BASIC_COLORS = (COLOR.BASE_NORMAL, COLOR.BASE_WHITE, COLOR.BASE_BLACK, COLOR.BASE_RED,
			COLOR.BASE_GREEN, COLOR.BASE_BLUE, COLOR.BASE_PURPLE, COLOR.BASE_CYAN,
			COLOR.BASE_BROWN, COLOR.BASE_DARK_GRAY, COLOR.BASE_GRAY, COLOR.BASE_LIGHT_GRAY)

	def __init__(self, CURSES_ATTR):
		dict.__init__(self)
		self.pair_nr = 0
		self.CURSES_ATTR = CURSES_ATTR

	def __getitem__(self, key):
		try:
			return dict.__getitem__(self, key)
		except KeyError:
			fg, bg = key
			self.pair_nr += 1
			curses.init_pair(self.pair_nr, self.CURSES_ATTR[fg], self.CURSES_ATTR[bg])
			if fg not in self.BASIC_COLORS:
				color_pair = curses.color_pair(self.pair_nr) | curses.A_BOLD
			else:
				color_pair = curses.color_pair(self.pair_nr)
			self[key] = color_pair
			return color_pair

CURSES_COLOR = None
CURSES_KEYS = None



def init():
	global CURSES_COLOR
	global CURSES_KEYS

	curses.curs_set(0)


	CURSES_KEYS = {
		curses.KEY_LEFT: KEY.LEFT,
		curses.KEY_RIGHT: KEY.RIGHT,
		curses.KEY_UP: KEY.UP,
		curses.KEY_DOWN: KEY.DOWN,
	}

	if curses.COLORS == 256:
		CURSES_ATTR = {
			COLOR.BASE_RED: 124,
			COLOR.BASE_GREEN: 34,
			COLOR.BASE_BLUE: 21,
			COLOR.BASE_PURPLE: 129,
			COLOR.BASE_CYAN: 37,
			COLOR.BASE_YELLOW: 227,
			COLOR.BASE_BROWN: 130,

			COLOR.BASE_DARK_BLUE: 19,
			COLOR.BASE_DARK_BROWN: 94,

			COLOR.BASE_LIGHT_RED: 203,
			COLOR.BASE_LIGHT_GREEN: 83,
			COLOR.BASE_LIGHT_BLUE: 63,
			COLOR.BASE_LIGHT_PURPLE: 207,
			COLOR.BASE_LIGHT_CYAN: 87,

			COLOR.BASE_WHITE: 231,
			COLOR.BASE_LIGHT: 253,
			COLOR.BASE_NORMAL: curses.COLOR_WHITE,
			COLOR.BASE_LIGHT_GRAY: 248,
			COLOR.BASE_GRAY: 245,
			COLOR.BASE_DARK_GRAY: 242,
			COLOR.BASE_DARK: 239,
			COLOR.BASE_DARKER: 236,
			COLOR.BASE_DARKEST: 233,
			COLOR.BASE_BLACK: 16,
		}

		CURSES_COLOR = Curses256ColorDict(CURSES_ATTR)

	else:
		CURSES_ATTR = {
			COLOR.BASE_BLACK: curses.COLOR_BLACK,
			COLOR.BASE_RED: curses.COLOR_RED,
			COLOR.BASE_GREEN: curses.COLOR_GREEN,
			COLOR.BASE_BROWN: curses.COLOR_YELLOW,
			COLOR.BASE_BLUE: curses.COLOR_BLUE,
			COLOR.BASE_PURPLE: curses.COLOR_MAGENTA,
			COLOR.BASE_CYAN: curses.COLOR_CYAN,
			COLOR.BASE_GRAY: curses.COLOR_WHITE,

			COLOR.BASE_LIGHT_RED: curses.COLOR_RED,
			COLOR.BASE_LIGHT_GREEN: curses.COLOR_GREEN,
			COLOR.BASE_YELLOW: curses.COLOR_YELLOW,
			COLOR.BASE_LIGHT_BLUE: curses.COLOR_BLUE,
			COLOR.BASE_LIGHT_PURPLE: curses.COLOR_MAGENTA,
			COLOR.BASE_LIGHT_CYAN: curses.COLOR_CYAN,

			COLOR.BASE_WHITE: curses.COLOR_WHITE,
			COLOR.BASE_LIGHT: curses.COLOR_WHITE,
			COLOR.BASE_NORMAL: curses.COLOR_WHITE,
			COLOR.BASE_LIGHT_GRAY: curses.COLOR_WHITE,
			COLOR.BASE_GRAY: curses.COLOR_WHITE,
			COLOR.BASE_DARK_GRAY: curses.COLOR_WHITE,
			COLOR.BASE_DARK: curses.COLOR_BLACK,
			COLOR.BASE_DARKER: curses.COLOR_BLACK,
			COLOR.BASE_DARKEST: curses.COLOR_BLACK,
		}
		CURSES_COLOR = CursesColorDict(CURSES_ATTR)



def init_handle(window):
	window.keypad(True)

def addch(window, y, x, char):
	symbol, color = char
	maxY, maxX = window.getmaxyx()
	try:
		window.addch(y, x, symbol, CURSES_COLOR[color])
	except curses.error:
		if y != maxY - 1 or x != maxX - 1:
			raise
	# Writing to the last cell of a window raises an exception because
	# the automatic cursor move to the next cell is illegal.

def addstr(window, y, x, string, color=None):
	if color is not None:
		window.addstr(y, x, string, CURSES_COLOR[color])
	else:
		window.addstr(y, x, string)

def draw(window, char_payload_sequence):
	maxY, maxX = window.getmaxyx()
	f = window.addch
	COLOR_LOOKUP = CURSES_COLOR
	for y, x, (symbol, color) in char_payload_sequence:
		try:
			f(y, x, symbol, COLOR_LOOKUP[color])
		except curses.error:
			if y != maxY - 1 or x != maxX - 1:
				raise

def draw_reverse(window, char_payload_sequence):
	maxY, maxX = window.getmaxyx()
	f = window.addch
	COLOR_LOOKUP = CURSES_COLOR
	for y, x, (symbol, (fg, bg)) in char_payload_sequence:
		try:
			f(y, x, symbol, COLOR_LOOKUP[bg, fg])
		except curses.error:
			if y != maxY - 1 or x != maxX - 1:
				raise

def getch(window):
	ch = window.getch()
	if ch in CURSES_KEYS:
		return CURSES_KEYS[ch]
	else:
		try:
			key = chr(ch)
			return key
		except ValueError:
			return ch

def clear(window):
	window.erase()
	window.move(0, 0)

def prepare_flush(window):
	window.noutrefresh()

def flush():
	curses.doupdate()

def get_dimensions(window):
	return window.getmaxyx()

def subwindow(window, rows, cols, y, x):
	return window.derwin(rows, cols, y, x)

def move(window, y, x):
	window.move(y, x)

def get_cursor_pos(window):
	return window.getyx()
