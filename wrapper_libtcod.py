import const.keys as KEY
import const.colors as COLOR
import const.game as GAME
import libtcodpy as libtcod

TCOD_COLOR = {
	COLOR.BASE_BLACK: libtcod.Color(0, 0, 0),
	COLOR.BASE_RED: libtcod.Color(175, 0, 0),
	COLOR.BASE_GREEN: libtcod.Color(0, 175, 0),
	COLOR.BASE_BLUE: libtcod.Color(0, 0, 175),
	COLOR.BASE_PURPLE: libtcod.Color(175, 0, 175),
	COLOR.BASE_CYAN: libtcod.Color(0, 175, 175),
	COLOR.BASE_YELLOW: libtcod.Color(255, 255, 95),
	COLOR.BASE_BROWN: libtcod.Color(150, 75, 0),

	COLOR.BASE_LIGHT_RED: libtcod.Color(255, 95, 95),
	COLOR.BASE_LIGHT_GREEN: libtcod.Color(95, 255, 95),
	COLOR.BASE_LIGHT_BLUE: libtcod.Color(95, 95, 255),
	COLOR.BASE_LIGHT_PURPLE: libtcod.Color(255, 95, 255),
	COLOR.BASE_LIGHT_CYAN: libtcod.Color(95, 255, 255),

	COLOR.BASE_WHITE: libtcod.Color(255, 255, 255),
	COLOR.BASE_LIGHT: libtcod.Color(218, 218, 218),
	COLOR.BASE_NORMAL: libtcod.Color(187, 187, 187),
	COLOR.BASE_LIGHT_GRAY: libtcod.Color(168, 168, 168),
	COLOR.BASE_GRAY: libtcod.Color(138, 138, 138),
	COLOR.BASE_DARK_GRAY: libtcod.Color(108, 108, 108),
	COLOR.BASE_DARK: libtcod.Color(78, 78, 78),
	COLOR.BASE_DARKER: libtcod.Color(48, 48, 48),
	COLOR.BASE_DARKEST: libtcod.Color(20, 20, 20),
	COLOR.BASE_BLACK: libtcod.Color(0, 0, 0),
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

def draw(handle, char_payload_sequence):
	f = libtcod.console_put_char_ex
	COLOR_LOOKUP = TCOD_COLOR
	for y, x, (symbol, (fg, bg)) in char_payload_sequence:
		f(handle, x, y, symbol, COLOR_LOOKUP[fg], COLOR_LOOKUP[bg])

def draw_reverse(handle, char_payload_sequence):
	f = libtcod.console_put_char_ex
	COLOR_LOOKUP = TCOD_COLOR
	for y, x, (symbol, (fg, bg)) in char_payload_sequence:
		f(handle, x, y, symbol, COLOR_LOOKUP[bg], COLOR_LOOKUP[fg])

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

def blit(handle, blit_args):
	if blit_args is not None:
		libtcod.console_blit(*blit_args)

def flush():
	libtcod.console_flush()

def get_dimensions(handle):
	return libtcod.console_get_height(handle), libtcod.console_get_width(handle)

def subwindow_handle(parent_handle, child_rows, child_cols, parent_offset_y, parent_offset_x):
	child_handle = libtcod.console_new(child_cols, child_rows)

	blit_args = (
			child_handle,                     # blitted window
			0, 0, child_cols, child_rows,     # the area of new window that will be blitted
			parent_handle,                    # target of the blit
			parent_offset_x, parent_offset_y, # where to blit in target
			1.0, 1.0                          # transparency
	)

	return child_handle, blit_args
	
def toggle_fullscreen():
	if libtcod.console_is_fullscreen():
		libtcod.console_set_fullscreen(False)
	else:
		libtcod.console_set_fullscreen(True)

def suspend(handle):
	pass
