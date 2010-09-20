import curses
import pickle as pickle
import shutil

from os import path
from io import io
from edit_map import EditMap
from map import Map
from dummy_map import DummyMap
from tile import Tile, tiles
from char import Char
from constants import YES, NO, DEFAULT

BACK = 1
EXIT = 4

def add_ebe(l, r, k):
	"""add an empty line, option to go back and exit to line selection"""
	l.extend(("", "[<] Back", "[Q]uit"))
	r.extend((None, BACK, EXIT))
	k[ord('<')] = BACK
	k[ord('Q')] = EXIT

class Editor(object):
	def __init__(self):
		self.maps = {}
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

		with open(path.join("editor_data", "maps"), "w") as l:
			pickle.dump(self.maps, l)

		self.modified = False

	def load(self, ask=True):
		if ask:
			c = io.a.getch_from_list(str="Are you sure you wish"
						" to load? [y/N] ")
			if c not in YES:
				return

		with open(path.join("editor_data", "maps"), "r") as f:
			self.maps = pickle.load(f)

		self.modified = False

	def export(self):
		if self.modified:
			c = io.a.getch_from__list(str="Data has been modified;"
						" save before exporting editor data? [y/N] ")
			if c in YES:
				self.save(ask=False)

		c = io.a.getch_from_list(str="Are you sure you wish to export"
						" all data to pyrl? [y/N] ")
		if c in YES:
			t = path.join("editor_data", "tiles")
			l = path.join("editor_data", "maps")
			d = path.join("data")
			shutil.copy(t, d)
			shutil.copy(l, d)

		return True

	def import_data(self):
		c = io.a.getch_from_list(str="Are you sure you wish"
					" to import game data? [y/N] ")
		if c not in YES:
			return

		#with open(path.join("data", "tiles"), "r") as f:
		#	self.tiles = pickle.load(f)

		with open(path.join("data", "maps"), "r") as f:
			self.maps = pickle.load(f)

		self.modified = True

	def back(self):
		return True

	def exit(self):
		if self.modified:
			c = io.a.getch_from_list(str="The data has been modified;"
						" save before exit? [y/N] ")
			if c in YES:
				self.save(ask=False)
		exit()

	def exec_ebe(self, s):
		if s == EXIT:
			self.exit()
		else:
			return s == BACK

	def main_menu(self):
		l = ["View global tiles", "Map editor", "[S]ave data",
				"[L]oad data", "Export data", "Import data", "[Q]uit"]
		r = [self.view_global_tiles, self.map_editor, self.save, self.load,
				self.export, self.import_data, self.exit]
		k = {ord('Q'): self.exit, ord('S'): self.save, ord('L'): self.load}
		i = 0
		while True:
			s = io.a.draw_menu(l, r, k, i)
			i = r.index(s)
			s()

	def view_global_tiles(self):
		for s in self.pick_dict(tiles, "tile to view"):
			self.view_tile(s)

	def view_tile(self, tile):
		i = 0
		while True:
			l = []
			r = []
			k = {}
			a = sorted(vars(tile))
			for key in a:
				value = getattr(tile, key)
				l.append((key, value))
				r.append((key, value))

			add_ebe(l, r, k)

			s = io.a.draw_menu(l, r, k, i)
			if s == BACK:
				return
			elif s == EXIT:
				self.exit()
			else:
				i = a.index(s[0])

	def map_editor(self):
		l = ["Make a new map", "Edit maps", "Delete maps"]
		r = [self.new_map, self.pick_map, self.delete_map]
		k = {}
		add_ebe(l, r, k)
		i = 0
		while True:
			s = io.a.draw_menu(l, r, k, i)
			i = r.index(s)
			if self.exec_ebe(s):
				return
			else:
				s()

	def new_tile(self, tiles):
		handle = io.a.getstr("Tile handle")
		tiles[handle] = Tile()
		self.modified = True

	def pick_dict(self, dict, str, give_key=False, map=False):
		i = 0
		while True:
			l = ["Pick a "+str, ""]
			r = [None, None]
			k = {}
			for key, value in sorted(dict.iteritems()):
				if map:
					l.append(key)
				else:
					l.append((key, value.ch_visible))
				if give_key:
					r.append(key)
				else:
					r.append(value)
			add_ebe(l, r, k)

			s = io.a.draw_menu(l, r, k, i)
			if self.exec_ebe(s):
				return
			else:
				i = r.index(s)
				yield s

	def edit_map(self, map):
		l = ["Edit", "Edit tiles", "Make a new tile", "Delete tiles"]
		r = [EditMap, self.pick_tile, self.new_tile, self.delete_tile]
		k = {}
		add_ebe(l, r, k)
		i = 0
		while True:
			s = io.a.draw_menu(l, r, k, i)
			i = r.index(s)
			if self.exec_ebe(s):
				return
			else:
				if s == EditMap:
					s(self, map)
				else:
					s(map.tiles)


	def pick_tile(self, tiles):
		for s in self.pick_dict(tiles, "tile to edit"):
			self.edit_tile(s)

	def delete_tile(self, tiles):
		for s in self.pick_dict(tiles, "tile to delete", True):
			c = io.a.getch_from_list(str="Are you sure you wish to delete"
						" this tile? [y/N]: ")
			if c in YES:
				del tiles[s]
				self.modified = True

	def update_tile(self, tiles):
		c = io.a.getch_from_list(str="Are you sure you wish to update"
					" all the tiles? [y/N]: ")
		if c in YES:
			for tile in tiles:
				d = []
				u = Tile()
				dict_tile = vars(tiles[tile])
				dict_u = vars(u)
				for i in dict_tile:
					if i not in dict_u:
						d.append(i)
				dict_u.update(dict_tile)
				for j in d:
					del dict_u[j]
				tiles[tile] = u
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
			if self.exec_ebe(s):
				return
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

	def new_map(self):
		handle = io.a.getstr("Map handle")
		self.maps[handle] = DummyMap(io.level_rows, io.level_cols, "f")
		self.modified = True

	def pick_map(self):
		for s in self.pick_dict(self.maps, "map to edit", False, True):
			self.edit_map(s)

	def delete_map(self):
		for s in self.pick_dict(self.maps, "map to delete", True, True):
			c = io.a.getch_from_list(str="Are you sure you want to delete"
						" this map? [y/N]: ")
			if c in YES:
				del self.maps[s]
				self.modified = True
