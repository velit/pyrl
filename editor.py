import curses
import pickle as pickle
import shutil
import sys

from os import path
from io import io
from edit_map import EditMap
from map import Map
from dungeonproperties import DungeonProperties, TileMap, DungeonNode
from tile import Tile, tiles
from char import Char
from constants import YES, NO, DEFAULT

def add_ebe(lrk_tuple):
	l, r, k, = lrk_tuple
	l.extend(("", "[<] Back", "[Q]uit"))
	r.extend((None, "Back", "Exit"))
	k.update({ord('<'): "Back", ord('Q'): "Exit"})

class Editor(object):
	def __init__(self):
		self.data = DungeonProperties()
		self.modified = False
		try:
			self.load(ask=False)
		except:
			pass

		self.main_menu_items = (
			("View global tiles", "Editor", "Save data",
			"Load data", "Export data", "Import data", "[Q]uit"),

			(self.view_global_tiles, self.editor_menu, self.save,
			self.load, self.export, self.import_data, self.safe_exit),

			{ord('Q'): self.safe_exit})

		self.editor_menu_items = (
			["Make a new map", "Edit maps", "Delete maps",
			"", "Make a new dungeon", "Edit dungeons", "Delete dungeons"],

			[self.new_map, self.edit_maps, self.delete_maps, None,
			self.new_dungeon, self.edit_dungeons, self.delete_dungeons], {})

		self.map_menu_items = (
			["Edit", "Edit tiles", "Make a new tile", "Delete tiles"],
			["Edit", "Edit tiles", "Make a new tile", "Delete tiles"], {})

		self.dungeon_menu_items = (
			["Edit", "Add a generated level", "Add a level", "Delete a level"],
			["Edit", "Add a generated level", "Add a level", "Delete a level"],
			{})

		add_ebe(self.editor_menu_items)
		add_ebe(self.map_menu_items)
		add_ebe(self.dungeon_menu_items)
		#self.menu(self.data.dungeons["main"], "Pick a level to delete",
		#		(self.delete_dungeon_level, self.data.dungeons["main"],
		#			"key", "key"))
		self.static_menu(self.main_menu_items)

	def editor_menu(self):
		self.static_menu(self.editor_menu_items)

	def edit_maps(self):
		self.menu(self.data.tilemaps, "Pick a map to edit",
				output_f=self.edit_map)

	def edit_map(self, map):
		self.static_menu(self.map_menu_items, self.map_menu, (map,))

	def map_menu(self, decision, map):
		if decision == "Edit":
			EditMap(self, map)
		elif decision == "Edit tiles":
			self.menu(map.tiles, "Pick a tile to edit", "both", "value",
					self.pick_attribute)
		elif decision == "Make a new tile":
			self.new_tile(map.tiles)
		elif decision == "Delete tiles":
			self.menu(map.tiles, "Pick a tile to delete", "both", "key",
					self.delete_tile, (map.tiles,))

	def edit_dungeons(self):
		self.menu(self.data.dungeons, "Pick a dungeon to edit", "key",
				"value", self.edit_dungeon)

	def edit_dungeon(self, dungeon):
		self.static_menu(self.dungeon_menu_items, self.dungeon_menu,
				(dungeon,))

	def dungeon_menu(self, decision, dungeon):
		if decision == "Edit":
			self.menu(dungeon, "Pick a level to edit", "both", "value",
					self.pick_attribute)
			#self.menu(vars(dungeon[0]), "Read Only", "both", "neither")
		elif decision == "Add a generated level":
			self.add_generated_dungeon_level(dungeon)
		elif decision == "Add a level":
			pass
		elif decision == "Delete a level":
			self.menu(dungeon, "Pick a level to delete", "both", "key",
					self.delete_dungeon_level, (dungeon,))

	def view_global_tiles(self):
		self.menu(tiles, "Pick a tile to view", "both", "value",
				self.view_tile)

	def view_tile(self, tile):
		self.menu(vars(tile), "Read Only", "both", "neither")

	def delete_maps(self):
		self.menu(self.data.tilemaps, "Pick a map to delete", "key", "key",
				self.delete_map)

	def delete_dungeons(self):
		self.menu(self.data.dungeons, "Pick a dungeon to delete", "key", "key",
				self.delete_dungeon)

	def pick_attribute(self, tile):
		self.menu(vars(tile), "Pick an attribute to edit", "both", "both",
				self.edit_attribute, (vars(tile),))

	def edit_attribute(self, attr_tuple, dict_):
		key, value = attr_tuple
		self.modified = True
		if isinstance(value, bool):
			dict_[key] = io.a.getbool(key)
			#setattr(tile, key, io.a.getbool(key))
		elif isinstance(value, str):
			dict_[key] = io.a.getstr(key)
			#setattr(tile, key, io.a.getstr(key))
		elif isinstance(value, int):
			dict_[key] = io.a.getint(key)
			#setattr(tile, key, io.a.getint(key))
		elif isinstance(value, Char):
			dict_[key] = Char(io.a.getchar(key), io.a.getcolor(key))
			#setattr(tile, key, Char(io.a.getchar(key),
			#	io.a.getcolor(key)))
		elif isinstance(value, dict):
			self.menu(value, "Pick an attribute to edit", "both", "both",
					self.edit_attribute, (value,))
		else:
			raise TypeError("Attempt to modify unsupported type: "+key)

	def edit_dict(self, attr_tuple, dict):
		pass

	def static_menu(self, menu, output_f=None, f_args=(), f_keys={}):
		i = 0
		while True:
			d = io.a.draw_menu(menu[0], menu[1], menu[2], i)
			i = menu[1].index(d)
			if d == "Back":
				return
			elif d == "Exit":
				self.safe_exit()
			elif output_f is None:
				d()
			else:
				output_f(d, *f_args, **f_keys)

	def menu(self, container, str_, print_="key", return_="value",
			output_f=None, f_args=(), f_keys={}):
		i = 0
		while True:
			l = [str_, ""]
			r = [None, None]
			k = {}

			if isinstance(container, list):
				kv = enumerate(container)
			elif isinstance(container, dict):
				kv = sorted(container.iteritems())
			else:
				kv = container

			for key, value in kv:
				if isinstance(value, Tile):
					print_value = value.ch_visible
				elif isinstance(value, DungeonNode):
					print_value = ("Tile handle:"+
						str(value.tilemap_handle))
				else:
					print_value = value

				if print_ == "both":
					l.append((key, print_value))
				elif print_ == "key":
					l.append(key)
				elif print_ == "value":
					l.append(print_value)
				else:
					l.append("N/A")

				if return_ == "both":
					r.append((key, value))
				elif return_ == "key":
					r.append(key)
				elif return_ == "value":
					r.append(value)
				else:
					r.append(lambda: None)
			add_ebe((l,r,k))

			d = io.a.draw_menu(l, r, k, i)
			i = r.index(d)
			if d == "Back":
				return
			elif d == "Exit":
				self.safe_exit()
			elif output_f is None:
				d()
			else:
				output_f(d, *f_args, **f_keys)


	def new_map(self):
		handle = io.a.getstr("Map handle")
		self.data.tilemaps[handle] = TileMap(io.level_rows, io.level_cols, "f")
		self.modified = True

	def delete_map(self, handle):
		c = io.a.sel_getch("Are you sure you want to delete"
					" this map? [y/N]: ")
		if c in YES:
			del self.data.tilemaps[handle]
			self.modified = True

	def new_tile(self, tiles):
		handle = io.a.getstr("Tile handle")
		tiles[handle] = Tile()
		self.modified = True

	def delete_tile(self, handle, tiles):
		c = io.a.sel_getch("Are you sure you wish to delete"
				" this tile? [y/N]: ")
		if c in YES:
			del tiles[handle]
			self.modified = True

	def new_dungeon(self):
		handle = io.a.getstr("Dungeon handle")
		self.data.add_dungeon(handle)
		self.modified = True

	def delete_dungeon(self, handle):
		c = io.a.sel_getch("Are you sure you want to delete"
					" this dungeon? [y/N]: ")
		if c in YES:
			self.data.del_dungeon(handle)
			self.modified = True

	def add_generated_dungeon_level(self, dungeon):
		i = len(dungeon)
		dungeon.append(DungeonNode(i))
		self.modified = True

	def add_static_dungeon_level(self, dungeon, tilemap_handle):
		i = len(dungeon)

		passageways = {}
		for key in self.tilemaps[level_key].squares:
			if key == "us":
				passageways[key] = "up"
			else:
				passageways[key] = "down"

		dungeon.append(DungeonNode(i, False, tilemap_handle, passageways))
		self.modified = True

	def delete_dungeon_level(self, i, dungeon):
		c = io.a.sel_getch("Are you sure you want to delete"
					" this dungeon level? [y/N]: ")
		if c in YES:
			del dungeon[i]
			self.modified = True

	def save(self, ask=True):
		if ask:
			c = io.a.sel_getch("Are you sure you wish"
						" to save? [y/N] ")
			if c not in YES:
				return

		with open(path.join("editor_data", "maps"), "w") as l:
			pickle.dump(self.data, l)

		self.modified = False

	def load(self, ask=True):
		if ask:
			c = io.a.sel_getch("Are you sure you wish"
						" to load? [y/N] ")
			if c not in YES:
				return

		with open(path.join("editor_data", "maps"), "r") as f:
			self.data = pickle.load(f)

		self.modified = False

	def export(self):
		if self.modified:
			c = io.a.sel_getch(str="Data has been modified;"
						" save before exporting editor data? [y/N] ")
			if c in YES:
				self.save(ask=False)

		c = io.a.sel_getch("Are you sure you wish to export"
						" all data to pyrl? [y/N] ")
		if c in YES:
			t = path.join("editor_data", "tiles")
			l = path.join("editor_data", "maps")
			d = path.join("data")
			shutil.copy(t, d)
			shutil.copy(l, d)

		return True

	def import_data(self):
		c = io.a.sel_getch("Are you sure you wish"
					" to import game data? [y/N] ")
		if c not in YES:
			return

		#with open(path.join("data", "tiles"), "r") as f:
		#	self.tiles = pickle.load(f)

		with open(path.join("data", "maps"), "r") as f:
			self.data = pickle.load(f)

		self.modified = True

	def safe_exit(self):
		if self.modified:
			c = io.a.sel_getch("The data has been modified;"
						" save before exit? [y/N] ")
			if c in YES:
				self.save(ask=False)
		exit()

	def update_tile(self, tiles):
		c = io.a.sel_getch("Are you sure you wish to update"
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
