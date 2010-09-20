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

def add_ebe(l, r, k):
	"""add an empty line, option to go back and exit to line selection"""
	l.extend(("", "Back [<]", "Exit [Q]"))
	r.extend((None, 1, 2))
	k[ord('<')] = 1
	k[ord('Q')] = 2

class Editor(object):
	def __init__(self):
		#self.tiles = tiles
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

		#with open(path.join("editor_data", "tiles"), "w") as t:
		#	pickle.dump(self.tiles, t)

		with open(path.join("editor_data", "maps"), "w") as l:
			pickle.dump(self.maps, l)

		self.modified = False

	#def staticise_maps(self):
	#	reverse = {}
	#	mapfile = []
	#	for k, v in tiles.iteritems():
	#		reverse[v] = k

	#	for key, map in self.maps.iteritems():
	#		mapdata = ([], key, map.rows, map.cols)
	#		for s in map:
	#			mapdata[0].append(reverse[s.tile])
	#		mapfile.append(mapdata)

	#	return mapfile

	def load(self, ask=True):
		if ask:
			c = io.a.getch_from_list(str="Are you sure you wish"
						" to load? [y/N] ")
			if c not in YES:
				return

		#with open(path.join("editor_data", "tiles"), "r") as f:
		#	self.tiles = pickle.load(f)

		with open(path.join("editor_data", "maps"), "r") as f:
			self.maps = pickle.load(f)

		self.modified = False

	#def generate_maps(self, mapfile):
	#	for map, key, y, x in mapfile:
	#		self.maps[key] = Map(y, x, (tiles[x] for x in map))

	def back(self):
		return True

	def exit(self):
		if self.modified:
			c = io.a.getch_from_list(str="The data has been modified;"
						" save before exit? [y/N] ")
			if c in YES:
				self.save(ask=False)
		exit()

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

	def main_menu(self):
		l = ("View global tiles", "Map editor", "Save data", "Load data",
					"Export data", "Import data", "Exit [Q]")
		r = (self.view_global_tiles, self.map_editor, self.save, self.load,
				self.export, self.import_data, self.exit)
		k = {ord('Q'): self.exit}
		i = 0
		while True:
			s = io.a.draw_menu(l, r, k, i)
			i = r.index(s)
			s()

	def view_global_tiles(self):
		for s in self.pick_dict(tiles, "tile to view"):
			self.view_tile(s)

	def tile_editor(self):
		l = ("Make a new tile", "Edit tiles", "Delete tiles", "Update tiles",
				"", "Back [<]", "Exit [Q]")
		r = (self.new_tile, self.pick_tile, self.delete_tile, self.update_tile,
					None, self.back, self.exit)
		k = {ord('<'): self.back, ord('Q'): self.exit}
		i = 0
		while True:
			s = io.a.draw_menu(l, r, k, i)
			i = r.index(s)
			if s():
				return

	def map_editor(self):
		l = ("Make a new map", "Edit maps", "Delete maps",
					"", "Back [<]", "Exit [Q]")
		r = (self.new_map, self.pick_map, self.delete_map,
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
		self.tiles[handle] = Tile()
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
			if s == 1:
				return
			elif s == 2:
				self.exit()
			else:
				i = r.index(s)
				yield s

	def pick_tile(self):
		for s in self.pick_dict(self.tiles, "tile to edit"):
			self.edit_tile(s)

	def delete_tile(self):
		for s in self.pick_dict(self.tiles, "tile to delete", True):
			c = io.a.getch_from_list(str="Are you sure you wish to delete"
						" this tile? [y/N]: ")
			if c in YES:
				del self.tiles[s]
				self.modified = True

	def update_tile(self):
		c = io.a.getch_from_list(str="Are you sure you wish to update"
					" all the tiles? [y/N]: ")
		if c in YES:
			for tile in self.tiles:
				d = []
				u = Tile()
				dict_tile = vars(self.tiles[tile])
				dict_u = vars(u)
				for i in dict_tile:
					if i not in dict_u:
						d.append(i)
				dict_u.update(dict_tile)
				for j in d:
					del dict_u[j]
				self.tiles[tile] = u
				self.modified = True

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
			if s == 1:
				return
			elif s == 2:
				self.exit()
			else:
				i = a.index(s[0])

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

	def new_map(self):
		handle = io.a.getstr("Map handle")
		self.maps[handle] = DummyMap(io.level_rows, io.level_cols, "f")
		self.modified = True

	def pick_map(self):
		for s in self.pick_dict(self.maps, "map to edit", False, True):
			EditMap(self, s)

	def delete_map(self):
		for s in self.pick_dict(self.maps, "map to delete", True, True):
			c = io.a.getch_from_list(str="Are you sure you want to delete"
						" this map? [y/N]: ")
			if c in YES:
				del self.maps[s]
				self.modified = True
