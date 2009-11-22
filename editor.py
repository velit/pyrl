import curses
import cPickle
import sys
from io import io
from colors import color
from tile import Tile
from tile import tiles
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

class Cursor:
	def __init__(self, y, x):
		self.y = y
		self.x = x

class Data:
	def __init__(self):
		self.tiles = {}
		self.levels = {}

class Editor:
	def __init__(self):
		try:
			self.load()
		except IOError:
			self.data = Data()
		self.modified = False

	def save(self):
		self.modified = False
		f = open("data", "w")
		cPickle.dump(self.data, f)
		f.close()

		return True

	def load(self):
		f = open("data", "r")
		self.data = cPickle.load(f)
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
			while c not in map(ord, ('y', 'Y', 'n', 'N')):
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
		handle = io.a.getstr("Tile handle: ")
		self.data.tiles[handle] = Tile()
		self.modified = True
		return True

	def pick_tile(self):
		while True:
			n = []
			d = []
			v = []
			for key, value in self.data.tiles.iteritems():
				n.append(key)
				d.append(value)
				v.append(value.ch)
			n.append("----")
			d.append(None)
			n.append("Back")
			d.append(1)
			n.append("Exit")
			d.append(2)

			a = io.a.getSelection(n, d, v, False)
			if a == 1:
				break
			elif a == 2:
				self.exit()
			elif not self.edit_tile(a):
				break

		return True

	def edit_tile(self, tile):
		n = ("Name:       ", "Passable:   ", "Destroyable:", "See through:", "Tile char:  ", "------------", "Edit more", "Back", "Exit")
		d = (1, 2, 3, 4, 5, None, 6, 7, 8)
		while True:
			v = (tile.name, str(tile.passable), str(tile.destroyable), str(tile.see_through), tile.ch)
			s = io.a.getSelection(n, d, v)
			if s in (1,2,3,4,5):
				self.modified = True
			if s == 1:
				tile.name = io.a.getstr("Name: ")
			elif s == 2:
				passable = io.a.getstr("Passable [1/0]: ")
				if passable == "1":
					tile.passable = True
				elif passable == "0":
					tile.passable = False
			elif s == 3:
				destroyable = io.a.getstr("Destroyable [1/0]: ")
				if destroyable == "1":
					tile.destroyable = True
				elif destroyable == "0":
					tile.destroyable = False
			elif s == 4:
				see_through = io.a.getstr("See through [1/0]: ")
				if see_through == "1":
					tile.see_through = True
				elif see_through == "0":
					tile.see_through = False
			elif s == 5:
				ch = io.a.getstr("Tile char: ")
				while len(ch) != 1:
					ch = io.a.getstr("Tile char must be exactly one char: ")
				col = io.a.getstr("Tile color: [white/normal/black, red/green/yellow/blue/purple/cyan/, light_red/light_*]: ")
				while col not in color:
					col = io.a.getstr("Color must be a pre-existing color: ")
				tile.ch = Char(ch, color[col])
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
		handle = io.a.getstr("Level handle: ")
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
