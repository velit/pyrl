import curses
import cPickle
import sys
import shutil
from os import path
from io import io
from colors import color
from tile import Tile, tiles
from char import Char
from level import Level

class Cursor(object):
	def __init__(self, y, x):
		self.y = y
		self.x = x

class Data(object):
	def __init__(self):
		self.tiles = {}
		self.levels = {}

class Editor(object):
	def __init__(self):
		try:
			self.load()
		except IOError:
			pass
		self.modified = False

	def save(self):
		self.modified = False
		t = open(path.join("editor_data", "tiles"), "w")
		cPickle.dump(self.data.tiles, t)
		t.close()

		l = open(path.join("editor_data", "levels"), "w")
		cPickle.dump(self.data.levels, l)
		l.close()

		return True

	def load(self):
		self.data = Data()

		f = open(path.join("editor_data", "tiles"), "r")
		self.data.tiles = cPickle.load(f)
		f.close()

		#f = open(path.join("editor_data", "levels"), "r")
		#self.data.levels = cPickle.load(f)
		#f.close()

		self.modified = False

		return True

	def back(self):
		return False

	def true(self):
		return True

	def exit(self):
		if self.modified:
			io.a.clear()
			io.a.addstr("The data has been modified; save before exit? [y/N] ")
			c = io.a.getch()
			while c not in map(ord, ('y', 'Y', 'n', 'N', '\n')):
				c = io.a.getch()
			if c == ord("y") or c == ord("Y"):
				self.save()
		sys.exit(0)

	def export(self):
		io.a.addstr("Are you sure? [y/N] ")
		c = io.a.getch()
		if c == ord('y'):
			t = path.join("editor_data", "tiles")
			l = path.join("editor_data", "levels")
			d = path.join("data")
			shutil.copy(t, d)
			shutil.copy (l, d)

		return True

	def ui(self):
		n = ("Tile editor", "Level editor", "Save data", "Load data", "Export data", "Exit")
		d = (self.tile_editor, self.level_editor, self.save, self.load, self.export, self.exit)
		while io.a.getSelection(n, d)():
			pass


	def tile_editor(self):
		n = ("Make a new tile", "Edit tiles", "----------",  "Back", "Exit")
		d = (self.new_tile, self.pick_tile, None, self.back, self.exit)
		while io.a.getSelection(n, d)():
			pass

		return True

	def new_tile(self):
		handle = io.a.getstr("Tile handle")
		self.data.tiles[handle] = Tile()
		self.modified = True
		return True

	def pick_tile(self):
		while True:
			tiles = self.data.tiles
			n = []
			v = []
			d = []
			for key, value in tiles.iteritems():
				n.append(key)
				v.append(value.visible_ch)
				d.append(value)
			n.append("----")
			d.append(None)
			n.append("Back")
			d.append(1)
			n.append("Exit")
			d.append(2)

			s = io.a.getSelection(n, d, v, False)
			if s == 1:
				break
			elif s == 2:
				self.exit()
			elif not self.edit_tile(s):
				break

		return True

	def edit_tile(self, tile):
		i = 0
		while True:
			n = []
			v = []
			d = []
			a = sorted(vars(tile))
			for key in a:
				value = getattr(tile, key)
				n.append(key)
				if isinstance(value, Char):
					v.append(value)
				else:
					v.append(str(value))
				d.append((key, value))

			n.append("")
			d.append(None)
			n.append("Edit more")
			d.append(1)
			n.append("Back")
			d.append(2)
			n.append("Exit")
			d.append(3)
			s = io.a.getSelection(n, d, v, i)
			if s == 1:
				return True
			elif s == 2:
				return False
			elif s == 3:
				self.exit()
			else:
				i = a.index(s[0])
				self.modified = True
				if isinstance(s[1], bool):
					setattr(tile, s[0], io.a.getbool(s[0]))
				elif isinstance(s[1], str):
					setattr(tile, s[0], io.a.getstr(s[0]))
				elif isinstance(s[1], int):
					setattr(tile, s[0], io.a.getint(s[0]))
				elif isinstance(s[1], Char):
					setattr(tile, s[0], Char(io.a.getchar(s[0]), io.a.getcolor(s[0])))
				else:
					self.exit()

	def edit_tile_alt(self, tile):
		n = ("Name:       ", "Passable:   ", "Destroyable:", "See through:", "Tile char:  ", "------------", "Edit more", "Back", "Exit")
		d = (1, 2, 3, 4, 5, None, 6, 7, 8)
		while True:
			v = (tile.name, str(tile.passable), str(tile.destroyable), str(tile.see_through), tile.ch)
			s = io.a.getSelection(n, d, v)
			if s in (1,2,3,4,5):
				self.modified = True
			if s == 1:
				tile.name = io.a.getstr("Name")
			elif s == 2:
				tile.passable = io.a.getbool("Passable")
			elif s == 3:
				tile.destroyable = io.a.getbool("Destroyable")
			elif s == 4:
				tile.see_through = io.a.getbool("See through")
			elif s == 5:
				tile.ch = Char(io.a.getchar("Tile char"), io.a.getcolor("Tile color"))
			elif s == 6:
				return True
			elif s == 7:
				return False
			elif s == 8:
				self.exit()

	def level_editor(self):
		n = ("Make a new level", "Edit levels", "-----------", "Back", "Exit")
		d = (self.new_level, self.pick_level, None, self.back, self.exit)
		while io.a.getSelection(n,d)():
			pass
		return True

	def new_level(self):
		handle = io.a.getstr("Level handle")
		self.data.levels[handle] = Map(20, 80, False)
		self.modified = True
		return True

	def pick_level(self):
		while True:
			n = []
			d = []
			for key, value in self.data.levels.iteritems():
				n.append(key)
				d.append(value)
			n.append("----")
			d.append(None)
			n.append("Back")
			d.append(1)
			n.append("Exit")
			d.append(2)

			a = io.a.getSelection(n, d)
			if a == 1:
				break
			elif a == 2:
				self.exit()
			elif not self.edit_level(a):
				break

		return True

	def edit_level(self, l):
		io.drawMap(l.map)
		t = tiles["f"]
		c = Cursor(0,0)
		my, mx = l.dimensions
		moves = map(ord, ('1', '2', '3', '4', '5', '6', '7', '8', '9'))
		moves.append(curses.KEY_UP)
		moves.append(curses.KEY_DOWN)
		moves.append(curses.KEY_LEFT)
		moves.append(curses.KEY_RIGHT)
		while True:
			ch = io.getch(c.y, c.x)
			if ch in moves:
				if ch in (ord('1'), ord('2'), ord('3'), curses.KEY_DOWN):
					c.y += 1
				if ch in (ord('1'), ord('4'), ord('7'), curses.KEY_LEFT):
					c.x -= 1
				if ch in (ord('9'), ord('8'), ord('7'), curses.KEY_UP):
					c.y -= 1
				if ch in (ord('9'), ord('6'), ord('3'), curses.KEY_RIGHT):
					c.x += 1
				if c.y < 0:
					c.y += my
				if c.x < 0:
					c.x += mx
				if c.y >= my:
					c.y -= my
				if c.x >= mx:
					c.x -= mx
			elif ch == ord('Q'):
				self.exit()
			elif ch == ord('S'):
				self.save()
			elif ch == ord('B'):
				return True
			elif ch == ord('\n'):
				a = l.getSquare(c.y, c.x)
				a.tile = t
				io.l.drawChar(c.y, c.x, a.getVisibleChar())
			elif ch == ord('1'):
				t = tiles["f"]
			elif ch == ord('2'):
				t = tiles["w"]
			elif ch == ord('3'):
				t = tiles["us"]
			elif ch == ord('4'):
				t = tiles["ds"]
			elif ch == ord('5'):
				t = tiles["r"]
