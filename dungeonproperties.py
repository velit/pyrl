import random

class DungeonProperties(object):
	"""Includes properties of generated dungeons."""
	def __init__(self):
		self.tilemaps = {}
		self.dungeons = {}

	def add_dungeon(self, dungeon_key):
		self.dungeons[dungeon_key] = []

	def del_dungeon(self, dungeon_key):
		del self.dungeons[dungeon_key]

	def add_random_level(self, dungeon_key):
		i = len(self.dungeons[dungeon_key])
		self.dungeons[dungeon_key].append(DungeonNode(i))

	def add_predefined_level(self, dungeon_key, level_key): 
		i = len(self.dungeons[dungeon_key])

		passageways = {}
		for key in self.tilemaps[level_key].squares:
			if key == "us":
				passageways[key] = "up"
			else:
				passageways[key] = "down"

		self.dungeons[dungeon_key].append(DungeonNode(i, False, level_key,
			passageways))

	def del_level(self, dungeon_key, i):
		del self.dungeons[dungeon_key][i]

class DungeonNode(object):
	def __init__(self, danger_level=0, tilemap_handle = None,
			passageways = {"us": "up", "ds": "down"}):
		self.danger_level = danger_level
		self.tilemap_handle = tilemap_handle
		self.passageways = passageways

class TileMap(list):
	"""A map containing the tiles of a level."""
	def __init__(self, y, x, t="f"):
		self.tiles = {}
		list.__init__(self, (t for x in range(y*x)))
		self.rows = y
		self.cols = x
		self.squares = {}

	def getsquare(self, y, x=None):
		if x is not None:
			return self[y*self.cols + x]
		else:
			return self.squares[y]

	def setsquare(self, y, x, tile):
		self[y*self.cols + x] = tile
