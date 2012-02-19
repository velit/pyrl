import const.keys as KEY
import const.colors as COLOR
import curses

CURSES_KEYS = {
	curses.KEY_LEFT: KEY.LEFT,
	curses.KEY_RIGHT: KEY.RIGHT,
	curses.KEY_UP: KEY.UP,
	curses.KEY_DOWN: KEY.DOWN,
}

CURSES_ATTR = {
	COLOR.BASE_BLACK: curses.COLOR_BLACK,
	COLOR.BASE_RED: curses.COLOR_RED,
	COLOR.BASE_GREEN: curses.COLOR_GREEN,
	COLOR.BASE_BROWN: curses.COLOR_YELLOW,
	COLOR.BASE_BLUE: curses.COLOR_BLUE,
	COLOR.BASE_PURPLE: curses.COLOR_MAGENTA,
	COLOR.BASE_CYAN: curses.COLOR_CYAN,
	COLOR.BASE_GREY: curses.COLOR_WHITE,

	COLOR.BASE_DARK: curses.COLOR_BLACK + 8,
	COLOR.BASE_LIGHT_RED: curses.COLOR_RED + 8,
	COLOR.BASE_LIGHT_GREEN: curses.COLOR_GREEN + 8,
	COLOR.BASE_YELLOW: curses.COLOR_YELLOW + 8,
	COLOR.BASE_LIGHT_BLUE: curses.COLOR_BLUE + 8,
	COLOR.BASE_LIGHT_PURPLE: curses.COLOR_MAGENTA + 8,
	COLOR.BASE_LIGHT_CYAN: curses.COLOR_CYAN + 8,
	COLOR.BASE_WHITE: curses.COLOR_WHITE + 8,
}

class CursesColorDict(dict):
	def __init__(self):
		dict.__init__(self)
		self.pair_nr = 0

	def __getitem__(self, key):
		try:
			return dict.__getitem__(self, key)
		except KeyError:
			fg, bg = key
			self.pair_nr += 1
			curses.init_pair(self.pair_nr, CURSES_ATTR[fg], CURSES_ATTR[bg])
			color_pair = curses.color_pair(self.pair_nr)
			self[key] = color_pair
			return color_pair

CURSES_COLOR = CursesColorDict()


def init():
	curses.curs_set(0)

def init_handle(window):
	window.keypad(True)

def addch(window, y, x, char):
	symbol, color = char
	maxY, maxX = window.getmaxyx()
	try:
		window.addch(y, x, symbol, CURSES_COLOR[color])
	except curses.error:
		if y!= maxY or x != maxX:
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
			if y != maxY or x != maxX:
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
