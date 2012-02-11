from __future__ import with_statement
import curses
import pickle as pickle
import shutil
import sys

from os import path
from pio import io
from template_structure import TemplateStructure
from tile import Tile
from tiles import tiles
from char import Char
from templates import MapTemplate, LevelTemplate
from const.game import YES, NO, DEFAULT, SET_LEVEL
from editor.tilemap_editor import TileMapEditor
from itertools import imap
from io import open

# key sets
_A = tuple(imap(ord, u"aA"))
_D = tuple(imap(ord, u"dD"))
_E = tuple(imap(ord, u"eE"))
_M = tuple(imap(ord, u"mM"))
_P = tuple(imap(ord, u"pP"))
_S = tuple(imap(ord, u"sS"))
_T = tuple(imap(ord, u"tT"))
_V = tuple(imap(ord, u"vV"))
_SELECT = tuple(imap(ord, u">\n"))
_DEL = (curses.KEY_DC, )
_INSERT = (curses.KEY_IC, )
_HOME = (curses.KEY_HOME, )

# a few lines
_BACK = u"[<] Back"
_QUIT = u"[Q]uit"

_MAIN_ITEMS = ((
	u"Welcome to the pyrl editor",
	u"",
	u"View global tiles",
	u"Edit tilemaps",
	u"Edit dungeons",
	u"",
	u"Save data",
	u"Load data",
	u"Reset data",
	u"Export data",
	u"Import data",
	_QUIT,
), (0, 1, 5))

_MAP_ITEMS = ((
	u"[E]dit",
	u"Edit [T]iles",
	u"",
	_BACK,
	_QUIT,
), (2, ))

_DUNGEON_ITEMS = ((
	u"Edit",
	u"Add a generated level",
	u"Add a level",
	u"",
	_BACK,
	_QUIT,
), (3, ))


class Editor():

	def __init__(self, load=True, open_menu=True):
		self.templates = TemplateStructure()
		self.tilemaps = {}
		if load:
			self.load(ask=False)
		self.modified = False

		self.static_menu(_MAIN_ITEMS, self.main_menu_behaviour)

	def reset(self, ask=True):
		if ask and io.sel_getch(u"Reset values? [y/N]") in YES:
			self.__init__(load=False, open_menu=False)

	def save(self, ask=True):
		if ask and io.sel_getch(u"Save? [y/N] ") not in YES:
			return
		try:
			with open(path.join(u"editor", u"data"), u"wb") as fp:
				pickle.dump(self.templates, fp)

			with open(path.join(u"editor", u"maptemplates"), u"wb") as fp:
				pickle.dump(self.tilemaps, fp)

		except IOError, exc:
			io.sel_getch(u"{}, data still saved in memory".format(exc))
		else:
			self.modified = False

	def load(self, ask=True):
		if ask and io.sel_getch(u"Load? [y/N] ") not in YES:
			return
		try:
			with open(path.join(u"editor", u"data"), u"rb") as fp:
				self.templates = pickle.load(fp)
		except IOError, exc:
			io.sel_getch(u"{}, resetting.".format(exc))

		try:
			with open(path.join(u"editor", u"maptemplates"), u"rb") as fp:
				self.tilemaps = pickle.load(fp)
		except IOError, exc:
			io.sel_getch(u"{}, resetting.".format(exc))

		self.modified = False

	def export(self):
		if self.modified and io.sel_getch(u"Save before export? [y/N]") in YES:
			self.save(ask=False)
		if io.sel_getch(u"Export data to pyrl? [y/N]") in YES:
			ed = path.join(u"editor", u"data")
			d = path.join(u"data")
			try:
				shutil.copy(ed, d)
			except IOError, exc:
				io.sel_getch(exc)

	def import_data(self):
		if io.sel_getch(u"Import game data to memory? [y/N] ") not in YES:
			return
		try:
			with open(path.join(u"data", u"data"), u"rb") as f:
				self.templates = pickle.load(f)
		except IOError, exc:
			io.sel_getch(exc)
		else:
			self.modified = True

	def safe_exit(self):
		if self.modified and io.sel_getch(u"Save before exit? [y/N] ") in YES:
			self.save(ask=False)
		exit()

	def main_menu_behaviour(self, line, char):
		if char in _SELECT:
			if line == u"View global tiles":
				self.menu(tiles, u"Pick a tile to view", u"both",
					self.view_global_tiles)

			elif line == u"Edit tilemaps":
				self.menu(self.tilemaps, u"[A]dd/[D]el, Edit [T]iles, "
					u"[V]iew entrances, [E]dit", u"key", self.edit_tilemap)

			elif line == u"Edit dungeons":
				self.menu(self.templates, u"[A]dd/[D]elete a dungeon, [E]dit",
					u"key", self.edit_dungeon)

			elif line == u"Save data":
				self.save()
			elif line == u"Load data":
				self.load()
			elif line == u"Export data":
				self.export()
			elif line == u"Import data":
				self.import_data()
			elif line == u"Reset data":
				self.reset()
			elif line == _QUIT:
				self.safe_exit()

	def view_global_tiles(self, tiles, k, char):
		if char in _SELECT:
			self.menu(vars(tiles[k]), k, u"both")

	def edit_tilemap(self, maps, k, char):
		if char in _SELECT + _E:
			TileMapEditor(self, maps[k])
		elif char in _D:
			self.delete_map(k)
		elif char in _A:
			self.add_map()
		elif char in _T:
			self.menu(maps[k].tile_dict, u"[A]dd/[D]elete tile, [E]dit",
					u"both", self.edit_tile)
		elif char in _V:
			self.menu(maps[k].entrance_locs, u"View only", u"both")

	def edit_tile(self, tiles, k, char):
		if char in _A:
			self.add_tile(tiles)
		elif char in _D:
			self.delete_tile(tiles, k)
		elif char in _SELECT + _E:
			self.menu(vars(tiles[k]), k, u"both", self.edit_tile_attribute)

	def edit_tile_attribute(self, tile_dict, k, char):
		if char in _SELECT + _E:
			self.edit_attribute(tile_dict, k)

	def edit_dungeon(self, dungeons, k, char):
		if char in _SELECT + _E:
			self.menu(dungeons[k],
					u"[A]dd/[D]elete a ([P]redefined) level, Edit",
					u"both", self.edit_dungeon_level)
		elif char in _A:
			self.add_dungeon()
		elif char in _D:
			self.delete_dungeon(k)

	def edit_dungeon_level(self, dungeon, i, char):
		if char in _SELECT + _E:
			self.menu(vars(dungeon[i]), u"Level: " + unicode(i), u"both",
					self.edit_dungeon_level_attr)
		elif char in _A:
			self.add_generated_dungeon_level(dungeon)
		elif char in _P:
			returns = self.menu(self.tilemaps,
					u"Pick a tilemap for dungeon level", u"key", u"return")
			if returns is not None and returns[2] in _SELECT:
					self.add_static_dungeon_level(dungeon,
							self.tilemaps[returns[1]])
		elif char in _D:
			self.delete_dungeon_level(dungeon, i)

	def edit_dungeon_level_attr(self, level_dict, k, char):
		if char in _SELECT + _E:
			if k == u"passages":
				self.menu(level_dict[k],
						u"Define passages, [A]dd/[D]elete",
						u"both", self.edit_passages)
			elif k == u"tilemap_key":
				pass
			else:
				self.edit_attribute(level_dict, k)

	def edit_passages(self, passages, k, char):
		if char in _SELECT + _S:
			d_r = self.menu(self.templates,
					u"Pick a dungeon for passage exit", u"key", u"return")
			if d_r is not None and d_r[2] in _SELECT:
				l_r = self.menu(d_r[0][d_r[1]],
						u"Pick a level for passage exit", u"both", u"return")
				if l_r is not None and l_r[2] in _SELECT:
					t_r = self.menu(l_r[0][l_r[1]].passages,
							u"Pick a passage pair", u"key", u"return")
					if t_r is not None and t_r[2] in _SELECT:
						passages[k] = (SET_LEVEL, (d_r[1], l_r[1], t_r[1]))

		elif char in _A:
			pass
		elif char in _D:
			self.delete_attribute(passages, k, u"passage")

	def edit_attribute(self, dict_, key):
		if isinstance(dict_[key], bool):
			dict_[key] = io.getbool(key, dict_[key])
		elif isinstance(dict_[key], unicode):
			dict_[key] = io.getstr(key, dict_[key])
		elif isinstance(dict_[key], int):
			dict_[key] = io.getint(key, dict_[key])
		elif isinstance(dict_[key], Char):
			dict_[key] = Char(io.getchar(key, dict_[key]),
					io.getcolor(key, dict_[key]))
		else:
			return
		self.modified = True

	def static_menu(self, lines_ignores, output_f=None, *f_args, **f_keys):
		(lines, ignores) = lines_ignores
		i = 0
		while True:
			i, ch = io.draw_menu(i, lines, ignores)
			if ch == ord(u'<') and _BACK in lines or \
					lines[i] == _BACK and ch in _SELECT:
				return
			elif ch == ord(u'Q') or lines[i] == _QUIT and ch in _SELECT:
				self.safe_exit()
			elif output_f is not None:
				output_f(lines[i], ch, *f_args, **f_keys)

	def menu(self, container, str_, print_=u"key", output_f=None, *f_args,
			**f_keys):
		i = 0
		while True:
			lines = [str_, u""]
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
				elif isinstance(value, LevelTemplate) and value.template is None:
					print_value = u"Randomly generated"
				elif isinstance(value, dict):
					print_value = u'dict'
				elif isinstance(value, list):
					print_value = u'list'
				else:
					print_value = value

				tmp_i = len(lines)
				if print_ == u"both":
					lines.append((key, print_value))
				elif print_ == u"key":
					lines.append(key)
				elif print_ == u"value":
					lines.append(print_value)
				else:
					lines.append(u"N/A")
				keys[tmp_i] = key

			lines.extend((u"", _BACK, _QUIT))
			keys.update({len(lines)-2: _BACK, len(lines)-1: _QUIT})
			ignores = (0, 1, len(lines)-3)


			i, ch = io.draw_menu(i, lines, ignores)

			if ch == ord(u'<') or i == len(lines)-2 and ch in _SELECT:
				return
			elif ch == ord(u'Q') or i == len(lines)-1 and ch in _SELECT:
				self.safe_exit()
			elif output_f == u"return":
				return container, keys[i], ch
			elif output_f is not None:
				if output_f(container, keys[i], ch, *f_args, **f_keys):
					return

	def modify_attribute_type(self, dict_, key):
		c = io.sel_getch(
				u"Select new type: [B]ool, [S]tring, [I]nt, [C]har, [N]one",
				tuple(imap(ord, u"BbSsIiCcNn")))
		if c in tuple(imap(ord, u"bB")):
			dict_[key] = bool()
		elif c in tuple(imap(ord, u"sS")):
			dict_[key] = unicode()
		elif c in tuple(imap(ord, u"iI")):
			dict_[key] = int()
		elif c in tuple(imap(ord, u"cC")):
			dict_[key] = Char()
		elif c in tuple(imap(ord, u"nN")):
			dict_[key] = None
		else:
			return
		self.modified = True

	def add_attribute(self, dict_, key):
		handle = io.getstr(u"Attribute handle", u"handle")
		dict_[handle] = None
		self.modified = True

	def add_map(self):
		handle = io.getstr(u"Map handle", u"map")
		self.tilemaps[handle] = MapTemplate()
		self.modified = True

	def delete_map(self, handle):
		self.delete_attribute(self.tilemaps, handle, u"map")

	def add_tile(self, tiles):
		handle = io.getstr(u"Tile handle", u"tile")
		tiles[handle] = Tile()
		self.modified = True

	def delete_tile(self, tiles, handle):
		self.delete_attribute(tiles, handle, u"tile")

	def add_dungeon(self):
		handle = io.getstr(u"Dungeon handle", u"dungeon")
		self.templates.add_dungeon_template(handle)
		self.modified = True

	def delete_dungeon(self, handle):
		c = io.sel_getch(u"Are you sure you want to delete"
					u" this dungeon? [y/N]: ")
		if c in YES:
			del self.templates[handle]
			self.modified = True

	def add_generated_dungeon_level(self, dungeon):
		self.templates.add_random_level_template(dungeon)
		self.modified = True

	def add_static_dungeon_level(self, dungeon, tilemap_key):
		self.templates.add_predefined_level_template(dungeon, tilemap_key)
		self.modified = True

	def delete_dungeon_level(self, dungeon, i):
		c = io.sel_getch(u"Are you sure you want to delete"
					u" this dungeon level? [y/N]: ")
		if c in YES:
			del dungeon[i]
			self.modified = True

	def delete_attribute(self, dict_, key, str_):
		ch = io.sel_getch(
				u"Are you sure you want to delete this {}? [y/N]: ".format(str_))
		if ch in YES:
			del dict_[key]
			self.modified = True

	def update_tile(self, tiles):
		c = io.sel_getch(u"Are you sure you wish to update"
					u" all the tiles? [y/N]: ")
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
