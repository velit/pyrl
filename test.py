#!/usr/bin/python

import libtcodpy as w


def get():
	w.console_set_custom_font("terminal10x18_gs_ro.png", w.FONT_TYPE_GREYSCALE | w.FONT_LAYOUT_ASCII_INROW)
	w.console_init_root(40, 12,"Test", False)
	w.console_flush()
	return w
