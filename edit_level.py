import curses

from io import io
from tile import tiles
from colors import color

def point(y, x, t, l):
	s = l.getsquare(y, x)
	s.tile = t
	io.l.drawchar(y, x, s.get_visible_char())

class EditLevel(object):
	def edit_level(self, l):
		self.modified = True
		io.drawmap(l)
		t = tiles["f"]
		funs = [point]
		f = point
		io.s.add_element("t", "[T]ile: ", lambda: t.visible_ch.symbol)
		io.s.add_element("f", "[F]unction: ", lambda: f.func_name)
		y, x = 0, 0
		my, mx = l.rows, l.cols
		moves = map(ord, ('1', '2', '3', '4', '5', '6', '7', '8', '9'))
		moves.append(curses.KEY_UP)
		moves.append(curses.KEY_DOWN)
		moves.append(curses.KEY_LEFT)
		moves.append(curses.KEY_RIGHT)
		while True:
			ch = io.getch(y, x)
			if ch in moves:
				if ch in (ord('1'), ord('2'), ord('3'), curses.KEY_DOWN):
					y += 1
				if ch in (ord('1'), ord('4'), ord('7'), curses.KEY_LEFT):
					x -= 1
				if ch in (ord('9'), ord('8'), ord('7'), curses.KEY_UP):
					y -= 1
				if ch in (ord('9'), ord('6'), ord('3'), curses.KEY_RIGHT):
					x += 1
				if y < 0:
					y += my
				if x < 0:
					x += mx
				if y >= my:
					y -= my
				if x >= mx:
					x -= mx
			elif ch == ord('Q'):
				self.exit()
			elif ch == ord('S'):
				self.save()
			elif ch == ord('B'):
				return
			elif ch == ord('\n'):
				f(y, x, t, l)
			elif ch in (ord('t'), ord('T')):
				w = ["Pick a tile: "]
				r = [None]
				for key, value in sorted(tiles.iteritems()):
					w.append(key)
					r.append(value)
				t = io.drawmenu(w, r)
			elif ch in (ord('f'), ord('F')):
				w = ["Pick a function: "]
				r = [None]
				for f_ in funs:
					w.append(f_.func_name)
					r.append(f_)
				f = io.drawmenu(w, r)
