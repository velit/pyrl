#!/usr/bin/python

import libtcodpy as libtcod

libtcod.console_set_custom_font("consolas12x12_gs_tc.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(40, 25,"pyrl", False)
libtcod.console_put_char_ex(None, 0, 0, '@', libtcod.green, libtcod.black)
libtcod.console_print(None, 2, 0, "penis")

while not libtcod.console_is_window_closed():
	key = libtcod.console_check_for_keypress()
	if not libtcod.console_credits_render(10, 10, False):
		libtcod.console_flush()
	else:
		break
