import const.keys as KEY
import const.colors as COLOR
import const.game as GAME
import libtcodpy as libtcod

TCOD_COLOR = {}
TCOD_KEYS = {}
TCOD_IGNORE_KEYS = set()

def init():
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

def init_handle(handle):
	libtcod.console_set_default_background(handle, libtcod.black)
	libtcod.console_set_default_foreground(handle, libtcod.white)

def addch(handle, y, x, char):
	symbol, color = char
	libtcod.console_put_char_ex(handle, x, y, symbol, TCOD_COLOR[color], libtcod.black)

def addstr(handle, y, x, string, color=None):
	if color is None:
		libtcod.console_print(handle, x, y, string)
	else:
		raise NotImplemented("Not yet implemented")

def getch(handle=None):
	while True:
		key = libtcod.console_wait_for_keypress(False)

		if key.c != 0:
			if key.c == ord('c') and key.lctrl or key.rctrl:
				raise KeyboardInterrupt
			return chr(key.c)
		elif key.vk in TCOD_KEYS:
			return TCOD_KEYS[key.vk]
		elif key.vk not in TCOD_IGNORE_KEYS:
			return key.vk

def clear(handle):
	libtcod.console_clear(handle)

def blit(blit_args):
	libtcod.console_blit(*blit_args)

def prepare_flush(handle):
	raise NotImplementedError("Use blit(blit_data) !")
	rows, cols = get_dimensions(handle)
	libtcod.console_blit(handle, 0, 0, cols, rows, 0, 0, 0, 1.0, 1.0)

def flush():
	libtcod.console_flush()

def get_dimensions(handle):
	return libtcod.console_get_height(handle), libtcod.console_get_width(handle)

def subwindow(handle, rows, cols, y, x):
	return libtcod.console_new(cols, rows)
