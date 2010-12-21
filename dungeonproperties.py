import random

class DungeonProperties(object):
	"""Includes properties of generated dungeons."""
	def __init__(self):
		self.tilemaps = {}
		self.dungeon_structure = {}

	def add_dungeon(self, dungeon_key):
		self.dungeon_structure[dungeon_key] = []

	def del_dungeon(self, dungeon_key):
		del self.dungeon_structure[dungeon_key]

	def add_random_dungeon_structure(self, dungeon_key):
		i = len(self.dungeon_structure[dungeon_key])
		self.dungeon_structure[dungeon_key].append(DungeonStructureNode(i))

	def add_predefined_dungeon_structure(self, dungeon_key, level_key): 
		i = len(self.dungeon_structure[dungeon_key])

		passageways = {}
		for key in self.tilemaps[level_key].squares:
			if key == "us":
				passageways[key] = "up"
			else:
				passageways[key] = "down"

		self.dungeon_structure[dungeon_key].append(DungeonStructureNode(i,
			False, level_key, passageways))

	def del_dungeon_structure(self, dungeon_key, i):
		del self.dungeon_structure[dungeon_key][i]

	def add_tilemap(self, tilemap):
		pass

class DungeonStructureNode(object):
	def __init__(self, danger_level=0, randomize = True, level_key = None,
			passageways = {"us": "up", "ds": "down"}):
		self.danger_level = danger_level
		self.randomize = randomize
		self.level_key = level_key
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
