import curses

from random import random

from io import io
from tile import tiles, PassageTile
from map import Map
from constants import DIR

class EditMap(object):
	def __init__(self, editor, tilemap):
		self.editor = editor
		self.map = tilemap
		self.y = 0
		self.x = 0
		self.my = self.map.rows-1
		self.mx = self.map.cols-1
		self.t = "f"
		self.funs = (self.point, self.rectangle, self.fill, self.randomize)
		self.f = self.point
		self.selected_tile = None
		io.s.add_element("t", "Tile: ", lambda:
				self.map.tiles[self.t].ch_visible.symbol if self.t in
				self.map.tiles else tiles[self.t].ch_visible.symbol)
		io.s.add_element("f", "Function: ", lambda: self.f.func_name)
		io.s.add_element("k", "Keys: ", lambda: "tyf")
		self.actions()

		self.edit_map()

	def drawmap(self):
		io.drawtilemap(self.map)

	def actions(self):
		a = {}
		a[curses.KEY_DOWN] = self.move_cursor, DIR.S
		a[curses.KEY_LEFT] = self.move_cursor, DIR.W
		a[curses.KEY_RIGHT] = self.move_cursor, DIR.E
		a[curses.KEY_UP] = self.move_cursor, DIR.N
		a[ord('.')] = self.move_cursor, DIR.STOP
		a[ord('1')] = self.move_cursor, DIR.SW
		a[ord('2')] = self.move_cursor, DIR.S
		a[ord('3')] = self.move_cursor, DIR.SE
		a[ord('4')] = self.move_cursor, DIR.W
		a[ord('5')] = self.move_cursor, DIR.STOP
		a[ord('6')] = self.move_cursor, DIR.E
		a[ord('7')] = self.move_cursor, DIR.NW
		a[ord('8')] = self.move_cursor, DIR.N
		a[ord('9')] = self.move_cursor, DIR.NE
		a[ord('S')] = self.editor.save,
		a[ord('Q')] = self.editor.safe_exit,

		self.actions = a

	def act(self, act):
		return act[0](*act[1:])
	
	def move_cursor(self, dir):
		self.y, self.x = self.y + DIR.DY[dir], self.x + DIR.DX[dir]
		if self.y < 0:
			self.y = 0
		if self.x < 0:
			self.x = 0
		if self.y > self.my:
			self.y = self.my
		if self.x > self.mx:
			self.x = self.mx

	def edit_map(self):
		while True:
			self.drawmap()
			ch = io.getch(self.y, self.x)
			if ch in self.actions:
				self.actions[ch][0](*self.actions[ch][1:])
			elif ch in map(ord, "B<"):
				return
			elif ch == ord('\n'):
				self.f()
				if isinstance(self.map.gettile(self.t), PassageTile):
					self.map.squares[self.map.gettile(self.t).passage] \
							= (self.y, self.x)
				self.editor.modified = True
			elif ch in map(ord, "tT"):
				w = ["Pick a tile:"]
				r = [None]
				for key in sorted(tiles):
					w.append(key)
					r.append(key)
				self.t = io.drawmenu(w, r)
			elif ch in (ord('y'), ord('Y')):
				w = ["Pick a tile:"]
				r = [None]
				for key in sorted(self.map.tiles):
					w.append(key)
					r.append(key)
				self.t = io.drawmenu(w, r)
			elif ch in (ord('f'), ord('F')):
				w = ["Pick a function:"]
				r = [None]
				for f in self.funs:
					w.append(f.func_name)
					r.append(f)
				self.f = io.drawmenu(w, r)

	def point(self):
		self.map.setsquare(self.y, self.x, self.t)

	def rectangle(self):
		if self.selected_tile is None:
			self.selected_tile = self.y, self.x
		else:
			y0, x0 = self.y, self.x
			y1, x1 = self.selected_tile
			for y in range(min(y0, y1), max(y0, y1)+1):
				for x in range(min(x0, x1), max(x0, x1)+1):
					s = self.map.setsquare(y, x, self.t)
			self.selected_tile = None
	
	def fill(self):
		for x in range(len(self.map)):
			self.map[x] = self.t

	def randomize(self):
		for i in range(len(self.map)):
			if random() < 0.3:
				self.map[i] = self.t
