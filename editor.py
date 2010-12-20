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

def add_ebe(lrk_tuple):
	l, r, k, = lrk_tuple
	l.extend(("", "[<] Back", "[Q]uit"))
	r.extend((None, BACK, EXIT))
	k.update({ord('<'): BACK, ord('Q'): EXIT})

class Editor(object):
	def __init__(self):
		self.maps = {}
		self.modified = False
		try:
			self.load(ask=False)
		except IOError:
			pass

		self.main_menu_items = (
			("View global tiles", "Map editor", "Save data",
			"Load data", "Export data", "Import data", "[Q]uit"),

			(self.view_global_tiles, self.map_menu, self.save,
			self.load, self.export, self.import_data, self.exit),

			{ord('Q'): self.exit})

		self.map_menu_items = (
			["Make a new map", "Edit maps", "Delete maps"],
			[self.new_map, self.edit_maps, self.delete_maps], {})

		self.map_edit_menu_items = (
			["Edit", "Edit tiles", "Make a new tile", "Delete tiles"],
			["Edit", "Edit tiles", "Make a new tile", "Delete tiles"], {})

		add_ebe(self.map_menu_items)
		add_ebe(self.map_edit_menu_items)
		self.static_menu(self.main_menu_items)

	def map_menu(self):
		self.static_menu(self.map_menu_items)

	def edit_map(self, map):
		self.static_menu(self.map_edit_menu_items, (self.map_edit_menu, map))

	def view_global_tiles(self):
		self.dict_menu(tiles, "Pick a tile to view", self.view_tile,
				output_matrix=(1,1))

	def view_tile(self, tile):
		self.dict_menu(vars(tile), "Defined in source: Read Only", None, True,
				(1,1), (0,0))

	def edit_maps(self):
		self.dict_menu(self.maps, "Pick a map to edit", self.edit_map,
				not_tile=True)

	def delete_maps(self):
		self.dict_menu(self.maps, "Pick a map to delete", self.delete_map,
				True, return_matrix=(1,0)) 

	def map_edit_menu(self, s, map):
		if s == "Edit":
			EditMap(self, map)
		elif s == "Edit tiles":
			self.dict_menu(map.tiles, "Pick a tile to edit",
					self.pick_attribute, output_matrix=(1,1))
		elif s == "Make a new tile":
			self.new_tile(map.tiles)
		elif s == "Delete tiles":
			self.dict_menu(map.tiles, "Pick a tile to delete",
					(self.delete_tile, map.tiles), False, (1,1), (1,0))


	def pick_attribute(self, tile):
		self.dict_menu(vars(tile), "Pick an attribute to edit",
				(self.edit_attribute, tile), True, (1,1), (1,1))

	def edit_attribute(self, attr_tuple, tile):
		key, value = attr_tuple
		self.modified = True
		if isinstance(value, bool):
			setattr(tile, key, io.a.getbool(key))
		elif isinstance(value, str):
			setattr(tile, key, io.a.getstr(key))
		elif isinstance(value, int):
			setattr(tile, key, io.a.getint(key))
		elif isinstance(value, Char):
			setattr(tile, key, Char(io.a.getchar(key),
				io.a.getcolor(key)))
		else:
			raise TypeError("Attempt to modify unsupported type: "+key)

	def static_menu(self, menu, behaviour_f=None):
		i = 0
		while True:
			s = io.a.draw_menu(menu[0], menu[1], menu[2], i)
			i = menu[1].index(s)
			if s == BACK:
				return
			elif s == EXIT:
				exit()
			elif behaviour_f is None:
				s()
			else:
				behaviour_f[0](s, *behaviour_f[1:])

	def dict_menu(self, dict, str, behaviour_f=None, not_tile=False,
			output_matrix=(1,0), return_matrix=(0,1)):
		i = 0
		lkey = output_matrix[0]
		lvalue = output_matrix[1]
		rkey = return_matrix[0]
		rvalue = return_matrix[1]
		while True:
			l = [str, ""]
			r = [None, None]
			k = {}
			for key, value in sorted(dict.iteritems()):
				if not_tile:
					print_value = value
				else:
					print_value = value.ch_visible

				if lkey and lvalue:
					l.append((key, print_value))
				elif lkey and not lvalue:
					l.append(key)
				elif not lkey and lvalue:
					l.append(print_value)
				else:
					l.append("N/A")

				if rkey and rvalue:
					r.append((key, value))
				elif rkey and not rvalue:
					r.append(key)
				elif not rkey and rvalue:
					r.append(value)
				else:
					r.append(lambda: None)
			add_ebe((l,r,k))

			s = io.a.draw_menu(l, r, k, i)
			i = r.index(s)
			if s == BACK:
				return
			elif s == EXIT:
				exit()
			elif behaviour_f is None:
				try:
					s()
				except TypeError:
					s[0](*s[1:])
			else:
				try:
					behaviour_f(s)
				except TypeError:
					behaviour_f[0](s, *behaviour_f[1:])

	def new_map(self):
		handle = io.a.getstr("Map handle")
		self.maps[handle] = DummyMap(io.level_rows, io.level_cols, "f")
		self.modified = True

	def delete_map(self, key):
		c = io.a.getch_from_list(str="Are you sure you want to delete"
					" this map? [y/N]: ")
		if c in YES:
			del self.maps[key]
			self.modified = True

	def new_tile(self, tiles):
		handle = io.a.getstr("Tile handle")
		tiles[handle] = Tile()
		self.modified = True

	def delete_tile(self, key, tiles):
		c = io.a.getch_from_list(str="Are you sure you wish to delete"
				" this tile? [y/N]: ")
		if c in YES:
			del tiles[key]
			self.modified = True

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

	def exit(self):
		if self.modified:
			c = io.a.getch_from_list(str="The data has been modified;"
						" save before exit? [y/N] ")
			if c in YES:
				self.save(ask=False)
		exit()

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
