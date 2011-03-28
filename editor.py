import curses
import pickle as pickle
import shutil
import sys

from os import path
from pio import io
from edit_map import EditMap
from map import TileMap
from level_templates import LevelTemplates, LevelTemplate
from tile import Tile
from tiles import tiles
from char import Char
from const.game import YES, NO, DEFAULT, SET_LEVEL

# key sets
_A = tuple(map(ord, "aA"))
_D = tuple(map(ord, "dD"))
_E = tuple(map(ord, "eE"))
_M = tuple(map(ord, "mM"))
_P = tuple(map(ord, "pP"))
_S = tuple(map(ord, "sS"))
_T = tuple(map(ord, "tT"))
_V = tuple(map(ord, "vV"))
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
	"Reset data",
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


class Editor():

	def __init__(self, load=True):
		self.templs = LevelTemplates()
		self.tilemaps = {}
		self.modified = False
		if load:
			self.load(ask=False)

		self.static_menu(_MAIN_ITEMS, self.main_menu_behaviour)

	def main_menu_behaviour(self, line, char):
		if char in _SELECT:
			if line == "View global tiles":
				self.menu(tiles, "Pick a tile to view", "both",
					self.view_global_tiles)

			elif line == "Edit maps":
				self.menu(self.tilemaps, "[A]dd/[D]el, Edit [T]iles, "
					"[V]iew entrances, [E]dit", "key", self.edit_map)

			elif line == "Edit dungeons":
				self.menu(self.templs,
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
			elif line == "Reset data":
				self.reset()
			elif line == _QUIT:
				self.safe_exit()

	def view_global_tiles(self, tiles, k, char):
		if char in _SELECT:
			self.menu(vars(tiles[k]), k, "both")

	def edit_map(self, maps, k, char):
		if char in _SELECT + _E:
			EditMap(self, maps[k])
		elif char in _D:
			self.delete_map(k)
		elif char in _A:
			self.add_map()
		elif char in _T:
			self.menu(maps[k].tile_dict, "[A]dd/[D]elete tile, [E]dit",
					"both", self.edit_tile)
		elif char in _V:
			self.menu(maps[k].entrance_locs, "View only", "both")

	def edit_tile(self, tiles, k, char):
		if char in _A:
			self.add_tile(tiles)
		elif char in _D:
			self.delete_tile(tiles, k)
		elif char in _SELECT + _E:
			self.menu(vars(tiles[k]), k, "both", self.edit_tile_attribute)

	def edit_tile_attribute(self, tile_dict, k, char):
		if char in _SELECT + _E:
			self.edit_attribute(tile_dict, k)

	def edit_dungeon(self, dungeons, k, char):
		if char in _SELECT + _E:
			self.menu(dungeons[k],
					"[A]dd/[D]elete a ([P]redefined) level, Edit",
					"both", self.edit_dungeon_level)
		elif char in _A:
			self.add_dungeon()
		elif char in _D:
			self.delete_dungeon(k)

	def edit_dungeon_level(self, dungeon, i, char):
		if char in _SELECT + _E:
			self.menu(vars(dungeon[i]), "Level: " + str(i), "both",
					self.edit_dungeon_level_attr)
		elif char in _A:
			self.add_generated_dungeon_level(dungeon)
		elif char in _P:
			returns = self.menu(self.tilemaps,
					"Pick a tilemap for dungeon level", "key", "return")
			if returns is not None and returns[2] in _SELECT:
					self.add_static_dungeon_level(dungeon,
							self.tilemaps[returns[1]])
		elif char in _D:
			self.delete_dungeon_level(dungeon, i)

	def edit_dungeon_level_attr(self, level_dict, k, char):
		if char in _SELECT + _E:
			if k == "passages":
				self.menu(level_dict[k],
						"Pick exit destination, [A]dd/[D]elete",
						"both", self.edit_passages)
			elif k == "tilemap_key":
				pass
			else:
				self.edit_attribute(level_dict, k)

	def edit_passages(self, passages, k, char):
		if char in _SELECT + _S:
			d_r = self.menu(self.templs,
					"Pick a dungeon for passage exit", "key", "return")
			if d_r is not None and d_r[2] in _SELECT:
				l_r = self.menu(d_r[0][d_r[1]],
						"Pick a level for passage exit", "both", "return")
				if l_r is not None and l_r[2] in _SELECT:
					t_r = self.menu(l_r[0][l_r[1]].passages,
							"Pick a passage pair", "key", "return")
					if t_r is not None and t_r[2] in _SELECT:
						passages[k] = (SET_LEVEL, (d_r[1], l_r[1], t_r[1]))

		elif char in _A:
			pass
		elif char in _D:
			self.delete_attribute(passages, k, "passage")

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

	def static_menu(self, lines_ignores, output_f=None, *f_args, **f_keys):
		(lines, ignores) = lines_ignores
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
				kv = sorted(container.items())
			else:
				kv = container

			for key, value in kv:
				if isinstance(value, Tile):
					print_value = value.ch_visible
				elif isinstance(value, LevelTemplate) and value.tilemap is None:
					print_value = "Randomly generated"
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
				tuple(map(ord, "BbSsIiCcNn")))
		if c in tuple(map(ord, "bB")):
			dict_[key] = bool()
		elif c in tuple(map(ord, "sS")):
			dict_[key] = str()
		elif c in tuple(map(ord, "iI")):
			dict_[key] = int()
		elif c in tuple(map(ord, "cC")):
			dict_[key] = Char()
		elif c in tuple(map(ord, "nN")):
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
		self.tilemaps[handle] = TileMap()
		self.modified = True

	def delete_map(self, handle):
		self.delete_attribute(self.tilemaps, handle, "map")

	def add_tile(self, tiles):
		handle = io.a.getstr("Tile handle")
		tiles[handle] = Tile()
		self.modified = True

	def delete_tile(self, tiles, handle):
		self.delete_attribute(tiles, handle, "tile")

	def add_dungeon(self):
		handle = io.a.getstr("Dungeon handle")
		self.templs.add_dungeon_template(handle)
		self.modified = True

	def delete_dungeon(self, handle):
		c = io.a.sel_getch("Are you sure you want to delete"
					" this dungeon? [y/N]: ")
		if c in YES:
			del self.templs[handle]
			self.modified = True

	def add_generated_dungeon_level(self, dungeon):
		self.templs.add_random_level_template(dungeon)
		self.modified = True

	def add_static_dungeon_level(self, dungeon, tilemap_key):
		self.templs.add_predefined_level_template(dungeon, tilemap_key)
		self.modified = True

	def delete_dungeon_level(self, dungeon, i):
		c = io.a.sel_getch("Are you sure you want to delete"
					" this dungeon level? [y/N]: ")
		if c in YES:
			del dungeon[i]
			self.modified = True

	def delete_attribute(self, dict_, key, str_):
		ch = io.a.sel_getch(
				"Are you sure you want to delete this {}? [y/N]: ".format(str_))
		if ch in YES:
			del dict_[key]
			self.modified = True

	def save(self, ask=True):
		if ask:
			c = io.a.sel_getch("Are you sure you wish"
						" to save? [y/N] ")
			if c not in YES:
				return

		with open(path.join("editor_data", "level_templates"), "wb") as l:
			pickle.dump(self.templs, l)

		self.modified = False

	def load(self, ask=True):
		if ask:
			c = io.a.sel_getch("Are you sure you wish"
						" to load? [y/N] ")
			if c not in YES:
				return

		try:
			with open(path.join("editor_data", "level_templates"), "rb") as f:
				self.templs = pickle.load(f)
		except IOError:
			io.a.sel_getch("Something went wrong with loading, resetting to "
						"default values.")
			self.templs = LevelTemplates()

		self.modified = False

	def reset(self, ask=True):
		if ask:
			c = io.a.sel_getch("Are you sure you wish to reset settings to"
					"their default values?")
			if c not in YES:
				return
		self.templs = LevelTemplates()
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
			ed = path.join("editor_data", "level_templates")
			d = path.join("data")
			shutil.copy(ed, d)

		return True

	def import_data(self):
		c = io.a.sel_getch("Are you sure you wish"
					" to import game data? [y/N] ")
		if c not in YES:
			return

		with open(path.join("data", "level_templates"), "rb") as f:
			self.templs = pickle.load(f)

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
