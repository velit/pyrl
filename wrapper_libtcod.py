import const.keys as KEY
import const.colors as COLOR
import const.game as GAME
import libtcodpy as libtcod

TCOD_COLOR = {
	COLOR.BASE_BLACK: libtcod.black,
	COLOR.BASE_RED: libtcod.red,
	COLOR.BASE_GREEN: libtcod.green,
	COLOR.BASE_BROWN: libtcod.Color(150, 75, 0),
	COLOR.BASE_BLUE: libtcod.blue,
	COLOR.BASE_PURPLE: libtcod.purple,
	COLOR.BASE_CYAN: libtcod.cyan,
	COLOR.BASE_GREY: libtcod.light_gray,

	COLOR.BASE_DARK: libtcod.darkest_grey,
	COLOR.BASE_LIGHT_RED: libtcod.light_red,
	COLOR.BASE_LIGHT_GREEN: libtcod.light_green,
	COLOR.BASE_YELLOW: libtcod.yellow,
	COLOR.BASE_LIGHT_BLUE: libtcod.light_blue,
	COLOR.BASE_LIGHT_PURPLE: libtcod.light_purple,
	COLOR.BASE_LIGHT_CYAN: libtcod.light_cyan,
	COLOR.BASE_WHITE: libtcod.white,

	COLOR.NORMAL: libtcod.white,
}

TCOD_KEYS = {
	libtcod.KEY_LEFT: KEY.LEFT,
	libtcod.KEY_RIGHT: KEY.RIGHT,
	libtcod.KEY_UP: KEY.UP,
	libtcod.KEY_DOWN: KEY.DOWN,
}

TCOD_IGNORE_KEYS = set([
	libtcod.KEY_SHIFT,
	libtcod.KEY_CONTROL,
	libtcod.KEY_ALT,
])

def init():
	libtcod.console_set_custom_font("terminal10x18_gs_ro.png",
			libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
	libtcod.console_init_root(GAME.MIN_SCREEN_COLS, GAME.MIN_SCREEN_ROWS, GAME.GAME_NAME,
			False, libtcod.RENDERER_SDL)

def init_handle(handle):
	libtcod.console_set_default_background(handle, libtcod.black)
	libtcod.console_set_default_foreground(handle, libtcod.white)

def addch(handle, y, x, char):
	symbol, (fg, bg) = char
	libtcod.console_put_char_ex(handle, x, y, symbol, TCOD_COLOR[fg], TCOD_COLOR[bg])

def addstr(handle, y, x, string, color=None):
	if color is None:
		libtcod.console_print(handle, x, y, string)
	else:
		raise NotImplemented("Not yet implemented")

def getch(handle=None):
	while True:
		key = libtcod.console_wait_for_keypress(False)
		
		if key.vk == libtcod.KEY_ENTER and key.lalt:
			toggle_fullscreen()
		elif key.c == ord('c') and key.lctrl or key.rctrl:
			raise KeyboardInterrupt
		elif key.c != 0:
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
	
def toggle_fullscreen():
	if libtcod.console_is_fullscreen():
		libtcod.console_set_fullscreen(False)
	else:
		libtcod.console_set_fullscreen(True)
