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

BACK = "[<] Back"
QUIT = "[Q]uit"

MAIN_ITEMS = ((
	"Welcome to the pyrl editor",
	"",
	"View global tiles",
	"Edit maps",
	"Edit dungeons",
	"",
	"Save data",
	"Load data",
	"Export data",
	"Import data",
	QUIT, 
), (0, 1, 5))

MAP_ITEMS = ((
	"Edit",
	"Edit tiles",
	"",
	BACK,
	QUIT,
), (2, ))

DUNGEON_ITEMS = ((
	"Edit",
	"Add a generated level",
	"Add a level",
	"Delete a level",
	"",
	BACK,
	QUIT,
), (4, ))

SELECT = (ord('\n'), ord('>'))
DEL = 330
INSERT = 331
HOME = 262

class Editor(object):

	def __init__(self):
		self.data = DungeonProperties()
		self.modified = False
		try:
			self.load(ask=False)
		except:
			pass

		self.static_menu(MAIN_ITEMS, self.main_menu_behaviour)

	def main_menu_behaviour(self, choice, char):
		if char in SELECT:
			if choice == "View global tiles":
				self.menu(tiles, "Pick a tile to view", "both", "value",
					self.view_global_tiles)

			elif choice == "Edit maps":
				self.menu(self.data.tilemaps,
					"[Del]ete, [Ins]ert, [T]iles, Edit",
					"key", "key", self.edit_map, (self.data.tilemaps, ))

			elif choice == "Edit dungeons":
				self.menu(self.data.dungeons,
					"[Del]ete, [Ins]ert, Edit",
					"key", "key", self.edit_dungeon, (self.data.dungeons, ))

			elif choice == "Save data":
				self.save()
			elif choice == "Load data":
				self.load()
			elif choice == "Export data":
				self.export()
			elif choice == "Import data":
				self.import_data()
			elif choice == QUIT:
				self.safe_exit()

	def edit_map(self, maps, key, char):
		if char in SELECT:
			self.static_menu(MAP_ITEMS, self.map_menu, (maps[key], ))
		elif char == DEL:
			self.delete_map(key)
		elif char == INSERT:
			self.add_map()
		elif char in (ord('T'), ord('t')):
			self.menu(maps[key].tiles, "[Del]ete, [Ins]ert, Edit",
					"both", "key", self.edit_tile, (maps[key].tiles, ))

	def edit_dungeon(self, dungeons, key, char):
		if char in SELECT:
			self.static_menu(DUNGEON_ITEMS,
					self.dungeon_menu, (dungeons[key], ))
		elif char == DEL:
			self.delete_dungeon(key)
		elif char == INSERT:
			self.add_dungeon()

	def edit_tile(self, tiles, key, char):
		if char in SELECT:
			self.menu(vars(tiles[key]),
					"Pick an attribute to edit",
					"both", "key", self.edit_attribute, (vars(tiles[key]), ))
		elif char == DEL:
			self.delete_tile(tiles, key)
		elif char == INSERT:
			self.add_tile(tiles)

	def map_menu(self, map, decision, char):
		if decision == "Edit":
			EditMap(self, map)
		elif decision == "Edit tiles":
			self.menu(map.tiles, "Pick a tile to edit", "both", "value",
					self.pick_attribute)
		elif decision == "Make a new tile":
			self.add_tile(map.tiles)
		elif decision == "Delete tiles":
			self.menu(map.tiles, "Pick a tile to delete", "both", "key",
					self.delete_tile, (map.tiles,))

	def dungeon_menu(self, dungeon, decision, char):
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

	def view_global_tiles(self, tile, char):
		if char not in SELECT: return

		self.menu(vars(tile), "Read Only", "both", "neither")

	def pick_attribute(self, tile, char):
		if char not in SELECT: return

		self.menu(vars(tile), "Pick an attribute to edit", "both", "key",
				self.edit_attribute, (vars(tile), ))

	def edit_attribute(self, dict_, key, char, protected=True,
			modifiable=()):
		if char == INSERT and not protected:
			handle = io.a.getstr("Attribute handle")
			dict_[handle] = None
		elif char in (HOME, ord('m'), ord('M')) and not protected:
			self.modify_attribute(dict_, key)
		elif char == DELETE and not protected:
			ch = io.a.sel_getch(
					"Are you sure you want to delete this attribute? [y/N]: ")
			if ch in YES:
				del dict_[key]
		elif char in SELECT:
			self.modified = True
			if isinstance(dict_[key], bool):
				dict_[key] = io.a.getbool(key)
			elif isinstance(dict_[key], str):
				dict_[key] = io.a.getstr(key)
			elif isinstance(dict_[key], int):
				dict_[key] = io.a.getint(key)
			elif isinstance(dict_[key], Char):
				dict_[key] = Char(io.a.getchar(key), io.a.getcolor(key))
			elif dict_[key] == None and not protected:
				self.modify_attribute(dict_, key)
			elif isinstance(dict_[key], dict):
				self.menu(dict_[key], "Pick an attribute to edit",
						"both", "key", self.edit_attribute, (dict_[key], ))
			else:
				raise TypeError("Attempt to modify unsupported type: "+key)

	def modify_attribute(self, dict_, key):
		c = io.a.sel_getch("[B]ool, [S]tring, [I]nt, [C]har, [N]one",
				map(ord, "BbSsIiCcNn"))
		if c in map(ord, "Bb"):
			dict_[key] = bool()
		elif c in map(ord, "Ss"):
			dict_[key] = str()
		elif c in map(ord, "Ii"):
			dict_[key] = int()
		elif c in map(ord, "Cc"):
			dict_[key] = Char()
		elif c in map(ord, "Nn"):
			dict_[key] = None

	def edit_dict(self, attr_tuple, dict):
		pass

	def static_menu(self, (lines, ignores),
			output_f=None, f_args=(), f_keys={}):
		i = 0
		while True:
			i, ch = io.a.draw_menu(i, lines, ignores)
			if ch == ord('<') and BACK in lines or \
					lines[i] == BACK and ch in SELECT:
				return
			elif ch == ord('Q') or lines[i] == QUIT and ch in SELECT:
				self.safe_exit()
			elif output_f is not None:
				f_keys["char"] = ch
				output_f(*(f_args + (lines[i], )), **f_keys)


	def menu(self, container, str_, print_="key", return_="value",
			output_f=None, f_args=(), f_keys={}):
		i = 0
		while True:
			lines = [str_, ""]
			returns = {}
			ignores = None

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
					print_value = ("Tile handle:"+ str(value.tilemap_handle))
				else:
					print_value = value

				tmp_i = len(lines)
				if print_ == "both":
					lines.append((key, print_value))
				elif print_ == "key":
					lines.append(key)
				elif print_ == "value":
					lines.append(print_value)
				else:
					lines.append("N/A")

				if return_ == "both":
					returns[tmp_i] = key, value
				elif return_ == "key":
					returns[tmp_i] = key
				elif return_ == "value":
					returns[tmp_i] = value
				else:
					returns[tmp_i] = None

			lines.extend(("", BACK, QUIT))
			returns.update({len(lines)-2: BACK, len(lines)-1: QUIT})
			ignores = (0, 1, len(lines)-3)


			i, ch = io.a.draw_menu(i, lines, ignores)

			if i == len(lines)-2 or ch == ord('<'):
				if ch in SELECT + (ord('<'), ):
					return
			elif i == len(lines)-1 or ch == ord('Q'):
				if ch in SELECT + (ord('Q'), ):
					self.safe_exit()
			elif ch == ord('<') or i == len(lines)-2 and ch in SELECT:
				return
			elif ch == ord('Q') or i == len(lines)-1 and ch in SELECT:
				self.safe_exit()
			elif output_f is not None:
				f_keys["char"] = ch
				output_f(*(f_args + (returns[i], )), **f_keys)


	def add_map(self):
		handle = io.a.getstr("Map handle")
		self.data.tilemaps[handle] = TileMap(io.level_rows, io.level_cols, "f")
		self.modified = True

	def delete_map(self, handle):
		c = io.a.sel_getch("Are you sure you want to delete"
					" this map? [y/N]: ")
		if c in YES:
			del self.data.tilemaps[handle]
			self.modified = True

	def add_tile(self, tiles):
		handle = io.a.getstr("Tile handle")
		tiles[handle] = Tile()
		self.modified = True

	def delete_tile(self, tiles, handle):
		c = io.a.sel_getch("Are you sure you wish to delete"
				" this tile? [y/N]: ")
		if c in YES:
			del tiles[handle]
			self.modified = True

	def add_dungeon(self):
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
