import curses

from io import io
from tile import tiles
from colors import color
from constants import *

class EditLevel(object):
	def __init__(self, editor, l):
		self.editor = editor
		self.l = l
		self.y = 0
		self.x = 0
		self.my = self.l.rows-1
		self.mx = self.l.cols-1
		self.t = tiles["f"]
		self.funs = (self.point, self.rectangle, self.fill)
		self.f = self.point
		self.selected_tile = None
		io.s.add_element("t", "[T]ile: ", lambda: self.t.ch_visible.symbol)
		io.s.add_element("f", "[F]unction: ", lambda: self.f.func_name)
		self.actions()

		self.edit_level()

	def drawmap(self):
		io.drawmap(self.l)

	def actions(self):
		a = {}
		a[curses.KEY_DOWN] = self.move_cursor, S
		a[curses.KEY_LEFT] = self.move_cursor, W
		a[curses.KEY_RIGHT] = self.move_cursor, E
		a[curses.KEY_UP] = self.move_cursor, N
		a[ord('.')] = self.move_cursor, STOP
		a[ord('1')] = self.move_cursor, SW
		a[ord('2')] = self.move_cursor, S
		a[ord('3')] = self.move_cursor, SE
		a[ord('4')] = self.move_cursor, W
		a[ord('5')] = self.move_cursor, STOP
		a[ord('6')] = self.move_cursor, E
		a[ord('7')] = self.move_cursor, NW
		a[ord('8')] = self.move_cursor, N
		a[ord('9')] = self.move_cursor, NE
		a[ord('S')] = self.editor.save,
		a[ord('Q')] = self.editor.exit,

		self.actions = a

	def act(self, act):
		return act[0](*act[1:])
	
	def move_cursor(self, dir):
		self.y, self.x = self.y + DY[dir], self.x + DX[dir]
		if self.y < 0:
			self.y = 0
		if self.x < 0:
			self.x = 0
		if self.y > self.my:
			self.y = self.my
		if self.x > self.mx:
			self.x = self.mx

	def edit_level(self):
		while True:
			io.drawmap(self.l)
			ch = io.getch(self.y, self.x)
			if ch in self.actions:
				self.actions[ch][0](*self.actions[ch][1:])
			elif ch == ord('B'):
				return
			elif ch == ord('\n'):
				self.f()
			elif ch in (ord('t'), ord('T')):
				w = ["Pick a tile: "]
				r = [None]
				for value in sorted(tiles.values()):
					w.append(value.ch_visible)
					r.append(value)
				self.t = io.drawmenu(w, r)
			elif ch in (ord('f'), ord('F')):
				w = ["Pick a function: "]
				r = [None]
				for f in self.funs:
					w.append(f.func_name)
					r.append(f)
				self.f = io.drawmenu(w, r)

	def point(self):
		s = self.l.getsquare(self.y, self.x)
		s.tile = self.t

	def rectangle(self):
		if self.selected_tile is None:
			self.selected_tile = self.y, self.x
		else:
			y0, x0 = self.y, self.x
			y1, x1 = self.selected_tile
			for y in range(min(y0, y1), max(y0, y1)+1):
				for x in range(min(x0, x1), max(x0, x1)+1):
					s = self.l.getsquare(y, x)
					s.tile = self.t
			self.selected_tile = None
	
	def fill(self):
		for square in self.l.map:
			square.tile = self.t
