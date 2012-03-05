import const.keys as KEY
import const.colors as COLOR
import curses
import curses.ascii

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
	curses.nonl()

	CURSES_KEYS = {
		curses.ascii.CR: KEY.ENTER,
		curses.ascii.TAB: KEY.TAB,
		curses.ascii.SP: KEY.SPACE,
		curses.KEY_UP: KEY.UP,
		curses.KEY_DOWN: KEY.DOWN,
		curses.KEY_LEFT: KEY.LEFT,
		curses.KEY_RIGHT: KEY.RIGHT,
		curses.KEY_HOME: KEY.HOME,
		curses.KEY_END: KEY.END,
		curses.KEY_NPAGE: KEY.PAGE_DOWN,
		curses.KEY_PPAGE: KEY.PAGE_UP,
		curses.KEY_A1: KEY.NUMPAD_7,
		curses.KEY_A3: KEY.NUMPAD_9,
		curses.KEY_B2: KEY.NUMPAD_5,
		curses.KEY_C1: KEY.NUMPAD_1,
		curses.KEY_C3: KEY.NUMPAD_3,
		curses.KEY_IC: KEY.INSERT,
		curses.KEY_DC: KEY.DELETE,
		curses.KEY_BACKSPACE: KEY.BACKSPACE,
		curses.KEY_FIND: KEY.NUMPAD_7,
		curses.KEY_SELECT: KEY.NUMPAD_1,
		curses.KEY_F1: KEY.F1,
		curses.KEY_F2: KEY.F2,
		curses.KEY_F3: KEY.F3,
		curses.KEY_F4: KEY.F4,
		curses.KEY_F5: KEY.F5,
		curses.KEY_F6: KEY.F6,
		curses.KEY_F7: KEY.F7,
		curses.KEY_F8: KEY.F8,
		curses.KEY_F9: KEY.F9,
		curses.KEY_F10: KEY.F10,
		curses.KEY_F11: KEY.F11,
		curses.KEY_F12: KEY.F12,
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

			COLOR.BASE_DARK_BLUE: curses.COLOR_BLUE,
			COLOR.BASE_DARK_BROWN: curses.COLOR_YELLOW,

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
	elif ch == curses.ascii.ESC:
		window.timeout(0)
		second_ch = window.getch()
		window.nodelay(False)
		if second_ch != curses.ERR:
			ch = curses.ascii.alt(second_ch)
		else:
			return KEY.ESC
	ch = curses.ascii.unctrl(ch)
	if '^' in ch:
		return ch.lower()
	else:
		return ch

def clear(window):
	window.clear()

def erase(window):
	window.erase()

def blit(window, blit_args):
	window.noutrefresh()

def redraw(window):
	window.redrawwin()

def flush():
	curses.doupdate()

def get_dimensions(window):
	return window.getmaxyx()

def subwindow_handle(parent_window, child_rows, child_cols, parent_offset_y, parent_offset_x):
	# ncurses doesn't use blitting
	return parent_window.derwin(child_rows, child_cols, parent_offset_y, parent_offset_x), None

def suspend(window):
	curses.endwin()

def move(window, y, x):
	window.move(y, x)

def get_cursor_pos(window):
	return window.getyx()
