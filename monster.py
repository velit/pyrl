from char import Char
from creature import Creature
from random import choice
from colors import color

mons = (('k', "kobold", "him"), ('@', "bandit", "him"), ('g', "goblin", "him"), ('j', "jelly", "it"), ('c', "centipede", "it"))
col = (("black", color["black"]), ("green", color["light_green"]), ("yellow", color["yellow"]), ("blue", color["blue"]))

class Monster(Creature):
	def __init__(self, game, level):
		super(Monster, self).__init__(game, level)
		m = choice(mons)
		c = choice(col)
		self.name = c[0] + " " + m[1]
		self.ch = Char(m[0], c[1])
		self.n = m[2]

	def act(self):
		if self.has_los(self.g.p):
			self.move(self.g.p.square.y, self.g.p.square.x)
		else:
			Creature.act(self)
