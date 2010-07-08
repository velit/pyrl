import curses
from char import Char
from colors import color

def draw(io, lines, returns, keys=(), start_line=0):
	indent = _get_indent(lines)
	_print_menu(io, lines, indent)
	return _update_ui(io, lines, returns, keys, start_line, indent)

def _update_ui(io, l, r, k, sl, i):
	sl = _roll_sl(sl, l, r)
	while True:
		c = _hilight_and_getch(io, sl, l, i)
		if c in k:
			curses.curs_set(1)
			return k[c]
		elif c in (curses.KEY_DOWN, ord('j')):
			sl = _roll_sl(sl, l, r, 1)
		elif c in (curses.KEY_UP, ord('k')):
			sl = _roll_sl(sl, l, r, -1)
		elif c == ord('\n') or c == ord('>'):
			curses.curs_set(1)
			return r[sl]

def _get_indent(lines):
	i = 0
	# if any line has second words, find out indentation level
	ii = isinstance
	if any(not ii(l, str) for l in lines):
		for l in lines:
			if not ii(l, str):
				if ii(l[0], Char):
					i = max(i, 1)
				else:
					i = max(i, len(l[0]))
		i += 1 #leave room between words
	return i

def _print_menu(io, l, i):
	curses.curs_set(0)
	io.clear()
	for y, line in enumerate(l):
		_print_menu_line(io, y, i, l)

def _print_menu_line(io, sl, i, l, reverse=False):
	r = color["reverse"] if reverse else color["normal"]
	if not isinstance(l[sl], str):
		ln = len(l[sl][0])
		_print_menu_word(io, sl, 0, l[sl][0], r)
		_print_menu_word(io, sl, ln, " "*(i-ln), r)
		_print_menu_word(io, sl, i, l[sl][1], r)
	else:
		_print_menu_word(io, sl, 0, l[sl], r)

def _print_menu_word(io, y, x, word, r):
	if isinstance(word, Char):
		io.w.addstr(y, x, word.symbol, word.color | r)
	else:
		io.w.addstr(y, x, str(word), r)

def _hilight_and_getch(io, sl, l, i):
	_print_menu_line(io, sl, i, l, True)
	c = io.w.getch()
	_print_menu_line(io, sl, i, l, False)
	return c

def _roll_sl(sl, l, r, add=0):
	sl += add
	#stepper
	s = -1 if add < 0 else 1

	while True:
		if sl >= len(l):
			sl = 0
		elif sl < 0:
			sl = len(l)-1
		if r[sl] is not None:
			break
		sl += s
	return sl
