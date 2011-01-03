import random

from tile import tiles
from constants import PASSAGE_UP, PASSAGE_DOWN, UP, DOWN

class DungeonProperties(object):
	"""Includes properties of generated dungeons."""
	def __init__(self):
		self.tilemaps = {}
		self.dungeons = {}

	def add_dungeon(self, dungeon_key):
		self.dungeons[dungeon_key] = []

	def del_dungeon(self, dungeon_key):
		del self.dungeons[dungeon_key]

	def add_random_level(self, dungeon):
		i = len(dungeon)
		dungeon.append(DungeonNode(i))

	def add_predefined_level(self, dungeon, tilemap_key):
		i = len(dungeon)

		passageways = {}
		for key in self.tilemaps[tilemap_key].squares:
			if key == PASSAGE_UP:
				passageways[key] = UP
			elif key == PASSAGE_DOWN:
				passageways[key] = DOWN
			else:
				raise NotImplementedError

		dungeon.append(DungeonNode(i, tilemap_key, passageways))

	def del_level(self, dungeon_key, i):
		del self.dungeons[dungeon_key][i]

	def gettilemap(self, key):
		return self.tilemaps[key]

	def getdungeon(self, key):
		return self.dungson[key]

class DungeonNode(object):
	def __init__(self, danger_level=0, tilemap_handle=None, passageways=None):
		self.danger_level = danger_level
		self.tilemap_handle = tilemap_handle
		if passageways is None:
			self.passageways = {PASSAGE_UP: UP, PASSAGE_DOWN: DOWN}
		else:
			self.passageways = passageways
