import curses

from random import random
from pio import io
from tiles import tiles, gettile
from map import Map
from const.directions import *


class TileMapEditor():

	def __init__(self, main, tilemap):
		self.main = main
		self.tilemap = tilemap
		self.y = 0
		self.x = 0
		self.my = self.tilemap.rows-1
		self.mx = self.tilemap.cols-1
		self.t = "f"
		self.funs = (self.point, self.rectangle, self.fill, self.randomize)
		self.f = self.point
		self.selected_tile = None
		io.s.add_element("t", "Tile: ", lambda:
				gettile(self.t, self.tilemap.tile_dict).ch_visible.symbol)
		io.s.add_element("f", "Function: ", lambda: self.f.__name__)
		io.s.add_element("k", "Keys: ", lambda: "tyf")
		self.actions()

		self.edit()

	def drawmap(self):
		io.drawtilemap(self.tilemap)

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
		a[ord('S')] = self.main.save,
		a[ord('Q')] = self.main.safe_exit,

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

	def edit(self):
		while True:
			self.drawmap()
			ch = io.getch(self.y, self.x)
			if ch in self.actions:
				self.actions[ch][0](*self.actions[ch][1:])
			elif ch in tuple(map(ord, "B<")):
				return
			elif ch == ord('\n'):
				self.f()
				t = self.tilemap.gettile(self.y, self.x)
				if t.exit_point is not None:
					self.tilemap.entrance_locs[t.exit_point] = (self.y, self.x)
				self.main.modified = True
			elif ch in tuple(map(ord, "tT")):
				w = ["Pick a tile:"]
				r = [None]
				for key in sorted(tiles):
					w.append(key)
					r.append(key)
				self.t = io.drawmenu(w, r)
			elif ch in (ord('y'), ord('Y')):
				w = ["Pick a tile:"]
				r = [None]
				for key in sorted(self.tilemap.tile_dict):
					w.append(key)
					r.append(key)
				self.t = io.drawmenu(w, r)
			elif ch in (ord('f'), ord('F')):
				w = ["Pick a function:"]
				r = [None]
				for f in self.funs:
					w.append(f.__name__)
					r.append(f)
				self.f = io.drawmenu(w, r)

	def point(self):
		self.tilemap.setsquare(self.y, self.x, self.t)

	def rectangle(self):
		if self.selected_tile is None:
			self.selected_tile = self.y, self.x
		else:
			y0, x0 = self.y, self.x
			y1, x1 = self.selected_tile
			for y in range(min(y0, y1), max(y0, y1) + 1):
				for x in range(min(x0, x1), max(x0, x1) + 1):
					s = self.tilemap.setsquare(y, x, self.t)
			self.selected_tile = None

	def fill(self):
		for x in range(len(self.tilemap)):
			self.tilemap[x] = self.t

	def randomize(self):
		for i in range(len(self.tilemap)):
			if random() < 0.3:
				self.tilemap[i] = self.t
