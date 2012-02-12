import const.keys as KEY
import const.colors as COLOR
import curses

CURSES_COLOR = {}
CURSES_KEYS = {}

def init():
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


def init_handle(window):
	window.keypad(True)

def addch(window, y, x, char):
	symbol, color = char
	maxY, maxX = window.getmaxyx()
	if y != maxY - 1 or x != maxX - 1:
		window.addch(y, x, symbol, CURSES_COLOR[color])
	else:
		window.insch(y, x, symbol, CURSES_COLOR[color])

		# Writing to the last cell of a window raises an exception because
		# the automatic cursor move to the next cell is illegal. insch avoids
		# this but it can only be used on the last cell because it moves the line

def addstr(window, y, x, string, color=None):
	if color is not None:
		window.addstr(y, x, string, CURSES_COLOR[color])
	else:
		window.addstr(y, x, string)

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
