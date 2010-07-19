import colors

from char import Char
from creature import Creature
from random import choice

mons = (('k', "kobold", "him"), ('@', "bandit", "him"), ('g', "goblin", "him"),
		('j', "jelly", "it"), ('c', "centipede", "it"))
col = (("black", colors.black), ("green", colors.light_green),
		("yellow", colors.yellow), ("blue", colors.blue))

class Monster(Creature):
	def __init__(self, game, level):
		super(Monster, self).__init__(game, level)
		m = choice(mons)
		c = choice(col)
		self.name = c[0] + " " + m[1]
		self.ch = Char(m[0], c[1])
		self.n = m[2]

	def act(self):
		if self.has_los(self.g.p.square):
			self.act_towards(self.g.p.square.y, self.g.p.square.x)
		else:
			self.move_random()
