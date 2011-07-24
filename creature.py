from char import Char
from creature_stats import Stats
from const.game import OPTIMIZATION


class Creature:

	def __init__(self, creature_file):
		self.name = creature_file.name
		self.char = creature_file.char
		self.stat = Stats()
		self.hp = self.stat.max_hp
		self.loc = None
