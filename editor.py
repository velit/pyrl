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

# key sets
_A = tuple(map(ord, "aA"))
_D = tuple(map(ord, "dD"))
_E = tuple(map(ord, "eE"))
_M = tuple(map(ord, "mM"))
_P = tuple(map(ord, "pP"))
_T = tuple(map(ord, "tT"))
_SELECT = tuple(map(ord, ">\n"))
_DEL = (curses.KEY_DC, )
_INSERT = (curses.KEY_IC, )
_HOME = (curses.KEY_HOME, )

# a few lines
_BACK = "[<] Back"
_QUIT = "[Q]uit"

_MAIN_ITEMS = ((
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
	_QUIT, 
), (0, 1, 5))

_MAP_ITEMS = ((
	"[E]dit",
	"Edit [T]iles",
	"",
	_BACK,
	_QUIT,
), (2, ))

_DUNGEON_ITEMS = ((
	"Edit",
	"Add a generated level",
	"Add a level",
	"",
	_BACK,
	_QUIT,
), (3, ))

class Editor(object):

	def __init__(self):
		self.data = DungeonProperties()
		self.modified = False
		try:
			self.load(ask=False)
		except:
			pass

		self.static_menu(_MAIN_ITEMS, self.main_menu_behaviour)

	def main_menu_behaviour(self, line, char):
		if char in _SELECT:
			if line == "View global tiles":
				self.menu(tiles, "Pick a tile to view", "both",
					self.view_global_tiles)

			elif line == "Edit maps":
				self.menu(self.data.tilemaps,
					"[A]dd/[D]elete a level, Edit [T]iles, [E]dit",
					"key", self.edit_map)

			elif line == "Edit dungeons":
				self.menu(self.data.dungeons,
					"[A]dd/[D]elete a dungeon, [E]dit",
					"key", self.edit_dungeon)

			elif line == "Save data":
				self.save()
			elif line == "Load data":
				self.load()
			elif line == "Export data":
				self.export()
			elif line == "Import data":
				self.import_data()
			elif line == _QUIT:
				self.safe_exit()

	def view_global_tiles(self, tiles, k, char):
		if char in _SELECT:
			self.menu(vars(tiles[k]), k, "both")

	def edit_map(self, maps, k, char):
		if char in _SELECT+_E:
			EditMap(self, maps[k])
		elif char in _D:
			self.delete_map(k)
		elif char in _A:
			self.add_map()
		elif char in _T:
			self.menu(maps[k].tiles, "[A]dd/[D]elete tile, [E]dit",
					"both", self.edit_tile)

	def edit_tile(self, tiles, k, char):
		if char in _A:
			self.add_tile(tiles)
		elif char in _D:
			self.delete_tile(tiles, k)
		elif char in _SELECT+_E:
			self.menu(vars(tiles[k]), k, "both", self.edit_tile_attribute)

	def edit_tile_attribute(self, tile_dict, k, char):
		if char in _SELECT+_E:
			self.edit_attribute(tile_dict, k)

	def edit_dungeon(self, dungeons, k, char):
		if char in _SELECT+_E:
			self.menu(dungeons[k],
					"[A]dd/[D]elete a ([P]redefined) level, Edit",
					"both", self.edit_dungeon_level)
		elif char in _A:
			self.add_dungeon()
		elif char in _D:
			self.delete_dungeon(k)

	def edit_dungeon_level(self, dungeon, i, char):
		if char in _SELECT+_E:
			self.menu(vars(dungeon[i]), "Level: "+str(i), "both",
					self.edit_dungeon_level_attr)
		elif char in _A:
			self.add_generated_dungeon_level(dungeon)
		elif char in _P:
			returns = self.menu(self.data.tilemaps,
					"Pick a tilemap for dungeon level", "key", "return")
			if returns is not None:
				__t, tilemap_handle, char2 = returns
				if char2 in _SELECT:
					self.add_static_dungeon_level(dungeon, tilemap_handle)
		elif char in _D:
			self.delete_dungeon_level(dungeon, i)

	def edit_dungeon_level_attr(self, level_dict, k, char):
		if char in _SELECT+_E:
			if k == "passageways":
				self.menu(level_dict[k], "[A]dd/[D]elete/[E]dit passageways",
						"both", self.edit_passageway)
			elif k == "tilemap_handle":
				pass
			else:
				self.edit_attribute(level_dict, k)

	def edit_passageway(self, passageways, k, char):
		if char in _SELECT+_E:
			pass
		elif char in _A:
			pass
		elif char in _D:
			self.delete_attribute(passageways, k, "passageway")

	def edit_attribute(self, dict_, key):
		if isinstance(dict_[key], bool):
			dict_[key] = io.a.getbool(key)
		elif isinstance(dict_[key], str):
			dict_[key] = io.a.getstr(key)
		elif isinstance(dict_[key], int):
			dict_[key] = io.a.getint(key)
		elif isinstance(dict_[key], Char):
			dict_[key] = Char(io.a.getchar(key), io.a.getcolor(key))
		else:
			return
		self.modified = True

	def static_menu(self, (lines, ignores), output_f=None, *f_args, **f_keys):
		i = 0
		while True:
			i, ch = io.a.draw_menu(i, lines, ignores)
			if ch == ord('<') and _BACK in lines or \
					lines[i] == _BACK and ch in _SELECT:
				return
			elif ch == ord('Q') or lines[i] == _QUIT and ch in _SELECT:
				self.safe_exit()
			elif output_f is not None:
				output_f(lines[i], ch, *f_args, **f_keys)


	def menu(self, container, str_, print_="key", output_f=None, *f_args,
			**f_keys):
		i = 0
		while True:
			lines = [str_, ""]
			keys = {}
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
					print_value = ("Tile handle:" + str(value.tilemap_handle))\
						if value.tilemap_handle else "Randomly generated"
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
				keys[tmp_i] = key

			lines.extend(("", _BACK, _QUIT))
			keys.update({len(lines)-2: _BACK, len(lines)-1: _QUIT})
			ignores = (0, 1, len(lines)-3)


			i, ch = io.a.draw_menu(i, lines, ignores)

			if ch == ord('<') or i == len(lines)-2 and ch in _SELECT:
				return
			elif ch == ord('Q') or i == len(lines)-1 and ch in _SELECT:
				self.safe_exit()
			elif output_f == "return":
				return container, keys[i], ch
			elif output_f is not None:
				if output_f(container, keys[i], ch, *f_args, **f_keys):
					return

	def modify_attribute_type(self, dict_, key):
		c = io.a.sel_getch(
				"Select new type: [B]ool, [S]tring, [I]nt, [C]har, [N]one",
				map(ord, "BbSsIiCcNn"))
		if c in map(ord, "bB"):
			dict_[key] = bool()
		elif c in map(ord, "sS"):
			dict_[key] = str()
		elif c in map(ord, "iI"):
			dict_[key] = int()
		elif c in map(ord, "cC"):
			dict_[key] = Char()
		elif c in map(ord, "nN"):
			dict_[key] = None
		else:
			return
		self.modified = True

	def add_attribute(self, dict_, key):
		handle = io.a.getstr("Attribute handle")
		dict_[handle] = None
		self.modified = True

	def add_map(self):
		handle = io.a.getstr("Map handle")
		self.data.tilemaps[handle] = TileMap(io.level_rows, io.level_cols, "f")
		self.modified = True

	def delete_map(self, handle):
		self.delete_attribute(self.data.tilemaps, handle, "map")

	def add_tile(self, tiles):
		handle = io.a.getstr("Tile handle")
		tiles[handle] = Tile()
		self.modified = True

	def delete_tile(self, tiles, handle):
		self.delete_attribute(tiles, handle, "tile")

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
		for key in self.data.tilemaps[tilemap_handle].squares:
			if key == "us":
				passageways[key] = "up"
			else:
				passageways[key] = "down"

		dungeon.append(DungeonNode(i, tilemap_handle, passageways))
		self.modified = True

	def delete_dungeon_level(self, dungeon, i):
		c = io.a.sel_getch("Are you sure you want to delete"
					" this dungeon level? [y/N]: ")
		if c in YES:
			del dungeon[i]
			self.modified = True

	def delete_attribute(self, dict_, key, str_):
		ch = io.a.sel_getch(
				"Are you sure you want to delete this "+str_+"? [y/N]: ")
		if ch in YES:
			del dict_[key]
			self.modified = True

	def save(self, ask=True):
		if ask:
			c = io.a.sel_getch("Are you sure you wish"
						" to save? [y/N] ")
			if c not in YES:
				return

		with open(path.join("editor_data", "data"), "w") as l:
			pickle.dump(self.data, l)

		self.modified = False

	def load(self, ask=True):
		if ask:
			c = io.a.sel_getch("Are you sure you wish"
						" to load? [y/N] ")
			if c not in YES:
				return

		with open(path.join("editor_data", "data"), "r") as f:
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
			ed = path.join("editor_data", "tiles")
			d = path.join("data")
			shutil.copy(ed, d)

		return True

	def import_data(self):
		raise NotImplementedError("This method isn't up to date")
		c = io.a.sel_getch("Are you sure you wish"
					" to import game data? [y/N] ")
		if c not in YES:
			return

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
