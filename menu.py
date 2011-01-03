import curses
import colors
from char import Char
from collections import Sequence

def draw(io, start_line, lines, line_ignores):
	indt = _get_indent(lines)
	_print_menu(io, indt, lines)
	return _update_ui(io, start_line, indt, lines, line_ignores)

def _get_len(obj):
	try:
		return len(obj)
	except TypeError:
		return len(str(obj))

def _get_indent(lines, column=0):
	indt = 0
	# if any line has second words, find out indentation level
	for l in lines:
		if not isinstance(l, str):
			try:
				o = l[column]
				indt = max(indt, _get_len(o)+1)
			except IndexError:
				continue

	return indt

def _print_menu(io, indt, lines):
	curses.curs_set(0)
	io.clear()
	for y in range(len(lines)):
		_print_menu_line(io, y, indt, lines)

def _update_ui(io, start_line, indt, lines, line_ignores):
	i = _roll_index(start_line, lines, line_ignores)
	while True:
		ch = _hilight_and_getch(io, i, indt, lines)
		if ch in (curses.KEY_DOWN, ord('j')):
			i = _roll_index(i, lines, line_ignores, 1)
		elif ch in (curses.KEY_UP, ord('k')):
			i = _roll_index(i, lines, line_ignores, -1)
		else:
			curses.curs_set(1)
			return i, ch

def _hilight_and_getch(io, line_i, indt, lines):
	_print_menu_line(io, line_i, indt, lines, True)
	c = io.w.getch()
	_print_menu_line(io, line_i, indt, lines, False)
	return c

def _roll_index(start_line, lines, ignores, add=0):
	i = start_line + add
	direction = add if add else 1
	while True:
		if i >= len(lines):
			i = 0
		if i < 0:
			i = len(lines)-1
		if i not in ignores:
			break
		i += direction
	return i

def _print_menu_line(io, line_i, indt, lines, reverse_color=False):
	i = line_i
	line = lines[i]
	reverse = colors.reverse if reverse_color else colors.normal
	if not isinstance(line, str) and isinstance(lines, Sequence):
		ln = _get_len(line[0])
		_print_menu_word(io, i, 0, line[0], reverse)
		_print_menu_word(io, i, ln, " "*(indt-ln), reverse)
		_print_menu_word(io, i, indt, line[1], reverse)
	else:
		_print_menu_word(io, i, 0, line, reverse)

def _print_menu_word(io, y, x, word, reverse_color):
	if isinstance(word, Char):
		try:
			io.w.addstr(y, x, word.symbol, colors.d[word.color] | reverse_color)
		except curses.error:
			pass
	else:
		try:
			io.w.addstr(y, x, str(word), reverse_color)
		except curses.error:
			pass
