import curses
import cPickle
import sys
from io import io
from colors import color
from tile import Tile
from char import Char
from map import Map

def save(data, name="data"):
	f = open(name, "w")
	cPickle.dump(data, f)
	f.close()

def load(name="data"):
	f = open(name, "r")
	a = cPickle.load(f)
	f.close()
	return a

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
			self.data = Data()
		self.modified = False

	def save(self):
		self.modified = False
		f = open("data", "w")
		cPickle.dump(self.data.tiles, f)
		f.close()

		return True

	def load(self):
		f = open("data", "r")
		self.data = Data()
		self.data.tiles = cPickle.load(f)
		f.close()
		#try:
		#	self.data.levels
		#except AttributeError:
		#	data = Data()
		#	data.tiles = self.data.tiles
		#	self.data = data

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

	def ui(self):
		n = ("Tile editor", "Level editor", "Save data", "Load data", "Exit")
		d = (self.tile_editor, self.level_editor, self.save, self.load, self.exit)
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
		while True:
			ch = io.getch(c.y, c.x)
			if ch == curses.KEY_LEFT:
				c.x -= 1
			elif ch == curses.KEY_RIGHT:
				c.x += 1
			elif ch == curses.KEY_UP:
				c.y -= 1
			elif ch == curses.KEY_DOWN:
				c.y += 1
			elif ch == ord('Q'):
				sys.exit(0)
			elif ch == ord('\n'):
				a = l.getSquare(c.y, c.x)
				a.tile = t
				io.l.drawChar(c.y, c.x, a.getVisibleChar())
			elif ch == ord('f'):
				t = tiles["f"]
