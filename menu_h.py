import curses
from char import Char
from colors import color

def draw(io, words, returns):
	_print_menu(io, words)
	return _update_ui(io, words, returns)

def _print_menu(io, w):
	curses.curs_set(0)
	io.clear()
	i = 0
	for word in w:
		if isinstance(word, Char):
			s = word.symbol
			col = word.color
			i += 4
		else:
			s = str(word)
			col = color["normal"]
			i += len(word) + 1
		try:
			io.w.addstr(0, i, s, col)
		except curses.error:
				pass
		pass

def _update_ui(io, w, r):
	#selected word
	sw = 0
	sw = _roll_sw(sw, w, r)
	while True:
		c = _hilight_and_getch(io, sw, w)
		if c in (curses.KEY_RIGHT, ord('l')):
			sw = _roll_sw(sw, w, r, 1)
		elif c in (curses.KEY_LEFT, ord('h')):
			sw = _roll_sw(sw, w, r, -1)
		elif c == ord('\n') or c == ord('>'):
			curses.curs_set(1)
			return r[sw]

def _hilight_and_getch(io, sw, w):
	_print_menu_word(io, sw, w, True)
	c = io.w.getch()
	_print_menu_word(io, sw, w, False)
	return c

def _print_menu_word(io, sw, w, r):
	if isinstance(w[sw], Char):
		s = w[sw].symbol
		col = w[sw].color
	else:
		s = str(w[sw])
		col = color["normal"]
	r = color["reverse"] if r else color["normal"]
	i = 0
	for x in w[:sw]:
		if isinstance(x, Char):
			i += 2
		else:
			i += len(x) + 1
	try:
		io.w.addstr(0, i, s, col | r)
	except curses.error:
		pass

def _roll_sw(sw, w, r, add=0):
	sw += add
	#stepper
	s = -1 if add < 0 else 1

	while True:
		if sw >= len(w):
			sw = 0
		elif sw < 0:
			sw = len(w)-1
		if r[sw] is not None:
			break
		sw += s
	return sw
