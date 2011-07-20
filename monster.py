from char import Char
from creature import Creature
from random import choice
from monster_file import MonsterFile


class Monster(Creature):

	def __init__(self, game, monster_file=None):
		super().__init__(game)
		if monster_file is None:
			m = choice(mons)
			c = choice(col)
			self.name = c[0] + " " + m[1]
			self.ch = Char(m[0], c[1])
			self.n = m[2]
		else:
			self.name = monster_file.name
			self.ch = monster_file.ch
			self.hp = monster_file.base_hp

	def act(self):
		if self.has_los(self.g.player.getsquare()):
			self.act_towards(*self.g.player.getsquare().getcoord())
		else:
			self.move_random()
