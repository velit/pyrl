import curses
import pickle as pickle
import shutil

from os import path
from io import io
from colors import color
from tile import Tile, tiles
from char import Char
from level import Level
from constants import YES, NO, DEFAULT

def add_ebe(n, d, k):
	"""add an empty line, option to go back and exit to line selection"""
	n.extend(("", "Back [<]", "Exit [Q]"))
	d.extend((None, 1, 2))
	k[ord('<')] = 1
	k[ord('Q')] = 2

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
			self.load(ask=False)
		except IOError:
			pass
		self.modified = False

	def save(self, ask=True):
		if ask:
			c = io.a.getch_from_list(str="Are you sure you wish"
						" to save? [y/N] ")
			if c not in YES:
				return True

		with open(path.join("editor_data", "tiles"), "w") as t:
			pickle.dump(self.data.tiles, t)

		with open(path.join("editor_data", "levels"), "w") as l:
			pickle.dump(self.data.levels, l)

		self.modified = False
		return True

	def load(self, ask=True):
		if ask:
			c = io.a.getch_from_list(str="Are you sure you wish"
						" to load? [y/N] ")
			if c not in YES:
				return True

		self.data = Data()

		with open(path.join("editor_data", "tiles"), "r") as f:
			self.data.tiles = pickle.load(f)

		with open(path.join("editor_data", "levels"), "r") as f:
			self.data.levels = pickle.load(f)

		self.modified = False
		return True

	def back(self):
		return True

	def exit(self):
		if self.modified:
			c = io.a.getch_from_list(str="The data has been modified;"
						" save before exit? [y/N] ")
			if c in (ord("y"), ord("Y")):
				self.save(ask=False)
		exit()

	def export(self):
		c = io.a.getch_from_list(str="Are you sure you wish to export"
						" all data to pyrl? [y/N] ")
		if c in (ord('y'), ord('Y')):
			t = path.join("editor_data", "tiles")
			l = path.join("editor_data", "levels")
			d = path.join("data")
			shutil.copy(t, d)
			shutil.copy(l, d)

		return True

	def ui(self):
		n = ("Tile editor", "Level editor", "Save data", "Load data",
					"Export data", "Exit [Q]")
		d = (self.tile_editor, self.level_editor, self.save, self.load,
				self.export, self.exit)
		k = {ord('Q'): self.exit}
		i = 0
		while True:
			s = io.a.get_selection(n, d, k, i)
			i = d.index(s)
			s()

	def tile_editor(self):
		n = ("Make a new tile", "Edit tiles", "Delete tiles", "",
					"Back [<]", "Exit [Q]")
		d = (self.new_tile, self.pick_tile, self.delete_tile, None,
					self.back, self.exit)
		k = {ord('<'): self.back, ord('Q'): self.exit}
		i = 0
		while True:
			s = io.a.get_selection(n, d, k, i)
			i = d.index(s)
			if s():
				return

	def new_tile(self):
		handle = io.a.getstr("Tile handle")
		self.data.tiles[handle] = Tile("name", '@', '@', False, False, False )
		self.modified = True

	def level_editor(self):
		n = ("Make a new level", "Edit levels", "Delete levels",
					"", "Back [<]", "Exit [Q]")
		d = (self.new_level, self.pick_level, self.delete_level,
					None, self.back, self.exit)
		k = {ord('<'): self.back, ord('Q'): self.exit}
		i = 0
		while True:
			s = io.a.get_selection(n, d, k, i)
			i = d.index(s)
			if s():
				return

	def new_level(self):
		handle = io.a.getstr("Level handle")
		self.data.levels[handle] = Level()
		self.modified = True

	def pick_tile(self):
		i = 0
		while True:
			n = ["Pick a tile to edit", ""]
			d = [None, None]
			k = {}
			for key, value in sorted(self.data.tiles.iteritems()):
				n.append((key, value.visible_ch))
				d.append(value)
			add_ebe(n, d, k)

			s = io.a.get_selection(n, d, k, i)
			if s == 1:
				return
			elif s == 2:
				self.exit()
			else:
				i = d.index(s)
				self.edit_tile(s)

	def delete_tile(self):
		i = 0
		while True:
			n = ["Pick a tile to delete", ""]
			d = [None, None]
			k = {}
			for key, value in sorted(self.data.tiles.iteritems()):
				n.append((key, value.visible_ch))
				d.append(value)
			add_ebe(n, d, k)

			s = io.a.get_selection(n, d, k, i)
			if s == 1:
				return
			elif s == 2:
				self.exit()
			else:
				i = d.index(s)
				c = io.a.getch_from_list(str="Are you sure you wish to delete"
							" this tile? [y/N]: ")
				if c in YES:
					del self.data.tiles[n[d.index(s)][0]]
					self.modified = True

	def edit_tile(self, tile):
		i = 0
		while True:
			n = ["Pick an attribute to edit"]
			v = [None]
			d = [None]
			k = {}
			a = sorted(vars(tile))
			for key in a:
				value = getattr(tile, key)
				n.append((key, value))
				d.append((key, value))

			add_ebe(n, d, k)

			s = io.a.get_selection(n, d, k, i)
			if s == 1:
				return
			elif s == 2:
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
					setattr(tile, s[0], Char(io.a.getchar(s[0]),
						io.a.getcolor(s[0])))
				else:
					raise TypeError("Attempt to modify unsupported type:"+
							s[0])

	def pick_level(self):
		i = 0
		while True:
			n = ["Pick a level to edit", ""]
			d = [None, None]
			k = {}
			a = sorted(self.data.levels.iteritems())
			for key, value in a:
				n.append(key)
				d.append(value)
			add_ebe(n, d, k)

			s = io.a.get_selection(n, d, k, i)
			if s == 1:
				return
			elif s == 2:
				self.exit()
			else:
				i = d.index(s)
				self.edit_level(s)

	def delete_level(self):
		i = 0
		while True:
			n = ["Pick a level to delete", ""]
			d = [None, None]
			k = {}
			for key, value in sorted(self.data.levels.iteritems()):
				n.append(key)
				d.append(value)
			add_ebe(n, d, k)

			s = io.a.get_selection(n, d, k, i)
			if s == 1:
				return
			elif s == 2:
				self.exit()
			else:
				i = d.index(s)
				c = io.a.getch_from_list(str="Are you sure you want to delete"
							" this level? [y/N]: ")
				if c in YES:
					del self.data.levels[n[d.index(s)]]
					self.modified = True

	def edit_level(self, l):
		io.drawmap(l)
		t = tiles["f"]
		c = Cursor(0,0)
		my, mx = l.rows, l.cols
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
				return
			elif ch == ord('\n'):
				a = l.getsquare(c.y, c.x)
				a.tile = t
				io.l.drawchar(c.y, c.x, a.get_visible_char())
			elif ch == ord('f'):
				t = tiles["f"]
			elif ch == ord('w'):
				t = tiles["w"]
			elif ch == ord('<'):
				t = tiles["us"]
			elif ch == ord('>'):
				t = tiles["ds"]
			elif ch == ord('r'):
				t = tiles["r"]
