import curses
import colors
from char import Char

def draw(io, words, returns):
	a = _print_menu(io, words, returns)
	return _update_ui(io, words, returns, a)

def _print_menu(io, w, r):
	curses.curs_set(0)
	io.clear()
	a = []
	for word in w:
		y, x = io.getyx()
		if isinstance(word, Char):
			s = word.symbol
			col = word.color
		else:
			s = word
			col = colors.normal
		if len(s) > io.cols - x:
			y, x = io.gety() + 1, a[_first_r(r)][1]
		a.append((y, x))
		try:
			io.w.addstr(y, x, s, col)
			if io.getx() != io.cols - 1:
				io.move(io.gety(), io.getx() + 1)
			else:
				io.move(io.gety() + 1, a[_first_r(r)][1])
		except curses.error:
			pass
	return a

def _first_r(r):
	for i, x in enumerate(r):
		if x is not None:
			return i

def _update_ui(io, w, r, a):
	#selected word
	sw = 0
	sw = _roll_sw(sw, w, r)
	while True:
		c = _hilight_and_getch(io, sw, w, a)
		if c in (curses.KEY_RIGHT, ord('l')):
			sw = _roll_sw(sw, w, r, 1)
		elif c in (curses.KEY_LEFT, ord('h')):
			sw = _roll_sw(sw, w, r, -1)
		elif c == ord('\n') or c == ord('>'):
			curses.curs_set(1)
			return r[sw]

def _hilight_and_getch(io, sw, w, a):
	_print_menu_word(io, sw, w, a, True)
	c = io.w.getch()
	_print_menu_word(io, sw, w, a, False)
	return c

def _print_menu_word(io, sw, w, a, r):
	y, x = a[sw]
	if isinstance(w[sw], Char):
		s = w[sw].symbol
		col = w[sw].color
	else:
		s = str(w[sw])
		col = colors.normal
	r = colors.reverse if r else colors.normal
	try:
		io.w.addstr(y, x, s, col | r)
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
