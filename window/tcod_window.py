import const.keys as KEY
import const.colors as COLOR
import const.game as GAME
import libtcodpy as libtcod

TCOD_COLOR = {}
TCOD_KEYS = {}
TCOD_IGNORE_KEYS = set()

def init_module():
	libtcod.console_set_custom_font("terminal10x18_gs_ro.png",
			libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
	libtcod.console_init_root(GAME.MIN_SCREEN_COLS, GAME.MIN_SCREEN_ROWS, GAME.GAME_NAME, False)
	c = TCOD_COLOR
	k = TCOD_KEYS
	i = TCOD_IGNORE_KEYS

	c[COLOR.GRAY] = libtcod.light_gray
	c[COLOR.BLACK_ON_BLACK] = libtcod.black
	c[COLOR.RED] = libtcod.red
	c[COLOR.GREEN] = libtcod.green
	c[COLOR.BROWN] = libtcod.Color(150, 75, 0)
	c[COLOR.BLUE] = libtcod.blue
	c[COLOR.PURPLE] = libtcod.purple
	c[COLOR.CYAN] = libtcod.cyan

	c[COLOR.WHITE] = libtcod.white
	c[COLOR.BLACK] = libtcod.darkest_grey
	c[COLOR.LIGHT_RED] = libtcod.light_red
	c[COLOR.LIGHT_GREEN] = libtcod.light_green
	c[COLOR.YELLOW] = libtcod.yellow
	c[COLOR.LIGHT_BLUE] = libtcod.light_blue
	c[COLOR.LIGHT_PURPLE] = libtcod.light_purple
	c[COLOR.LIGHT_CYAN] = libtcod.light_cyan

	c[COLOR.NORMAL] = libtcod.white

	_temp = {}
	for key, value in c.iteritems():
		_temp[key + COLOR.MAKE_REVERSE] = value
	c.update(_temp)

	c[COLOR.BLINK] = libtcod.white
	c[COLOR.BOLD] = libtcod.white
	c[COLOR.DIM] = libtcod.white
	c[COLOR.REVERSE] = libtcod.white
	c[COLOR.STANDOUT] = libtcod.white
	c[COLOR.UNDERLINE] = libtcod.white

	k[libtcod.KEY_LEFT] = KEY.LEFT
	k[libtcod.KEY_RIGHT] = KEY.RIGHT 
	k[libtcod.KEY_UP] = KEY.UP
	k[libtcod.KEY_DOWN] = KEY.DOWN

	i.add(libtcod.KEY_SHIFT)
	i.add(libtcod.KEY_CONTROL)
	i.add(libtcod.KEY_ALT)


class TCODWindow(object):

	def __init__(self, offscreen_handler):
		self.w = offscreen_handler
		self.rows, self.cols = self.get_dimensions()
		libtcod.console_set_default_background(self.w, libtcod.black)
		libtcod.console_set_default_foreground(self.w, libtcod.white)
		
		self.subwindow_blit_args = []

	def addch(self, y, x, char):
		symbol, color = char
		libtcod.console_put_char_ex(self.w, x, y, symbol, TCOD_COLOR[color], libtcod.black)

	def addstr(self, y, x, string, color=None):
		if color is None:
			libtcod.console_print(self.w, x, y, string)
			#self.getch()
			#raise Exception(string)
		else:
			raise NotImplemented

	def getch(self):
		while True:
			key = libtcod.console_wait_for_keypress(False)

			if key.c != 0:
				return chr(key.c)
			elif key.vk in TCOD_KEYS:
				return TCOD_KEYS[key.vk]
			elif key.vk not in TCOD_IGNORE_KEYS:
				return key.vk

	def clear(self):
		libtcod.console_clear(self.w)

	def prepare_flush(self):
		pass

	def flush(self):
		for args in self.subwindow_blit_args:
			libtcod.console_blit(*args)
		libtcod.console_flush()

	def get_dimensions(self):
		return libtcod.console_get_height(self.w), libtcod.console_get_width(self.w)

	def subwindow(self, nlines, ncols, y, x):
		console = libtcod.console_new(ncols, nlines)
		assert console != 0
		self.subwindow_blit_args.append((console, 0, 0, ncols, nlines, self.w, x, y, 1.0, 1.0))
		return console
