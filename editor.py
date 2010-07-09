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

def add_ebe(l, r, k):
	"""add an empty line, option to go back and exit to line selection"""
	l.extend(("", "Back [<]", "Exit [Q]"))
	r.extend((None, 1, 2))
	k[ord('<')] = 1
	k[ord('Q')] = 2

class Editor(object):
	def __init__(self):
		self.tiles = {}
		self.levels = {}
		self.modified = False
		try:
			self.load(ask=False)
		except IOError:
			pass
		self.main_menu()

	def save(self, ask=True):
		if ask:
			c = io.a.getch_from_list(str="Are you sure you wish"
						" to save? [y/N] ")
			if c not in YES:
				return

		with open(path.join("editor_data", "tiles"), "w") as t:
			pickle.dump(self.tiles, t)

		with open(path.join("editor_data", "levels"), "w") as l:
			pickle.dump(self.levels, l)

		self.modified = False

	def load(self, ask=True):
		if ask:
			c = io.a.getch_from_list(str="Are you sure you wish"
						" to load? [y/N] ")
			if c not in YES:
				return

		with open(path.join("editor_data", "tiles"), "r") as f:
			self.tiles = pickle.load(f)

		with open(path.join("editor_data", "levels"), "r") as f:
			self.levels = pickle.load(f)

		self.modified = False

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
			r = path.join("data")
			shutil.copy(t, d)
			shutil.copy(l, d)

		return True

	def main_menu(self):
		l = ("Tile editor", "Level editor", "Save data", "Load data",
					"Export data", "Exit [Q]")
		r = (self.tile_editor, self.level_editor, self.save, self.load,
				self.export, self.exit)
		k = {ord('Q'): self.exit}
		i = 0
		while True:
			s = io.a.draw_menu(l, r, k, i)
			i = r.index(s)
			s()

	def tile_editor(self):
		l = ("Make a new tile", "Edit tiles", "Delete tiles", "",
					"Back [<]", "Exit [Q]")
		r = (self.new_tile, self.pick_tile, self.delete_tile, None,
					self.back, self.exit)
		k = {ord('<'): self.back, ord('Q'): self.exit}
		i = 0
		while True:
			s = io.a.draw_menu(l, r, k, i)
			i = r.index(s)
			if s():
				return

	def level_editor(self):
		l = ("Make a new level", "Edit levels", "Delete levels",
					"", "Back [<]", "Exit [Q]")
		r = (self.new_level, self.pick_level, self.delete_level,
					None, self.back, self.exit)
		k = {ord('<'): self.back, ord('Q'): self.exit}
		i = 0
		while True:
			s = io.a.draw_menu(l, r, k, i)
			i = r.index(s)
			if s():
				return

	def new_tile(self):
		handle = io.a.getstr("Tile handle")
		self.tiles[handle] = Tile("name", '@', '@', False, False, False )
		self.modified = True

	def pick_tile(self):
		i = 0
		while True:
			l = ["Pick a tile to edit", ""]
			r = [None, None]
			k = {}
			for key, value in sorted(self.tiles.iteritems()):
				l.append((key, value.visible_ch))
				r.append(value)
			add_ebe(l, r, k)

			s = io.a.draw_menu(l, r, k, i)
			if s == 1:
				return
			elif s == 2:
				self.exit()
			else:
				i = r.index(s)
				self.edit_tile(s)

	def delete_tile(self):
		i = 0
		while True:
			l = ["Pick a tile to delete", ""]
			r = [None, None]
			k = {}
			for key, value in sorted(self.tiles.iteritems()):
				l.append((key, value.visible_ch))
				r.append(value)
			add_ebe(l, r, k)

			s = io.a.draw_menu(l, r, k, i)
			if s == 1:
				return
			elif s == 2:
				self.exit()
			else:
				i = r.index(s)
				c = io.a.getch_from_list(str="Are you sure you wish to delete"
							" this tile? [y/N]: ")
				if c in YES:
					del self.tiles[l[r.index(s)][0]]
					self.modified = True

	def edit_tile(self, tile):
		i = 0
		while True:
			l = ["Pick an attribute to edit", ""]
			r = [None, None]
			k = {}
			a = sorted(vars(tile))
			for key in a:
				value = getattr(tile, key)
				l.append((key, value))
				r.append((key, value))

			add_ebe(l, r, k)

			s = io.a.draw_menu(l, r, k, i)
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

	def new_level(self):
		handle = io.a.getstr("Level handle")
		self.levels[handle] = Level()
		self.modified = True

	def pick_level(self):
		i = 0
		while True:
			l = ["Pick a level to edit", ""]
			r = [None, None]
			k = {}
			a = sorted(self.levels.iteritems())
			for key, value in a:
				l.append(key)
				r.append(value)
			add_ebe(l, r, k)

			s = io.a.draw_menu(l, r, k, i)
			if s == 1:
				return
			elif s == 2:
				self.exit()
			else:
				i = r.index(s)
				self.edit_level(s)

	def delete_level(self):
		i = 0
		while True:
			l = ["Pick a level to delete", ""]
			r = [None, None]
			k = {}
			for key, value in sorted(self.levels.iteritems()):
				l.append(key)
				r.append(value)
			add_ebe(l, r, k)

			s = io.a.draw_menu(l, r, k, i)
			if s == 1:
				return
			elif s == 2:
				self.exit()
			else:
				i = r.index(s)
				c = io.a.getch_from_list(str="Are you sure you want to delete"
							" this level? [y/N]: ")
				if c in YES:
					del self.levels[l[r.index(s)]]
					self.modified = True

	def edit_level(self, l):
		self.modified = True
		io.drawmap(l)
		t = tiles["f"]
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
				a = l.getsquare(y, x)
				a.tile = t
				io.l.drawchar(y, x, a.get_visible_char())
			elif ch == ord('t'):
				w = ["Pick a tile: "]
				r = [None]
				a = sorted(tiles.iteritems())
				for key, value in a:
					w.append(key)
					r.append(value)
				t = io.drawmenu(w, r)

