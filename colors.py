import curses
from const.colors import *

CURSES_COLOR = {}

def init_colors():
	d = CURSES_COLOR
	for x in range(7):
		curses.init_pair(x + 1, x, 0)

	d[GREY] = curses.color_pair(0)
	d[BLACK_ON_BLACK] = curses.color_pair(1)
	d[RED] = curses.color_pair(2)
	d[GREEN] = curses.color_pair(3)
	d[BROWN] = curses.color_pair(4)
	d[BLUE] = curses.color_pair(5)
	d[PURPLE] = curses.color_pair(6)
	d[CYAN] = curses.color_pair(7)

	d[WHITE] = curses.color_pair(0) | curses.A_BOLD
	d[BLACK] = curses.color_pair(1) | curses.A_BOLD
	d[LIGHT_RED] = curses.color_pair(2) | curses.A_BOLD
	d[LIGHT_GREEN] = curses.color_pair(3) | curses.A_BOLD
	d[YELLOW] = curses.color_pair(4) | curses.A_BOLD
	d[LIGHT_BLUE] = curses.color_pair(5) | curses.A_BOLD
	d[LIGHT_PURPLE] = curses.color_pair(6) | curses.A_BOLD
	d[LIGHT_CYAN] = curses.color_pair(7) | curses.A_BOLD

	d[NORMAL] = curses.A_NORMAL

	_temp = {}
	for key, value in d.items():
		_temp[key + MAKE_REVERSE] = value | curses.A_REVERSE
	d.update(_temp)

	d[BLINK] = curses.A_BLINK
	d[BOLD] = curses.A_BOLD
	d[DIM] = curses.A_DIM
	d[REVERSE] = curses.A_REVERSE
	d[STANDOUT] = curses.A_STANDOUT
	d[UNDERLINE] = curses.A_UNDERLINE
