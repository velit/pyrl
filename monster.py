from char import Char
from creature import Creature
from random import choice
from monster_file import MonsterFile


class Monster(Creature):

	def __init__(self, game, monster_file):
		super().__init__(game)
		self.name = monster_file.name
		self.char = monster_file.char
		self.hp = monster_file.base_hp

	def act(self):
		if self.has_los(self.g.player.getsquare()):
			self.act_towards(*self.g.player.getsquare().getcoord())
		else:
			self.move_random()
