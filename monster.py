from char import Char
from creature import Creature
from random import choice

mons = (('k', "kobold", "him"), ('@', "bandit", "him"), ('g', "goblin", "him"),
		('j', "jelly", "it"), ('c', "centipede", "it"))
col = (("black", "black"), ("green", "light_green"),
		("yellow", "yellow"), ("blue", "blue"))


class Monster(Creature):

	def __init__(self, game, level, template=None):
		super(Monster, self).__init__(game, level)
		if template is None:
			m = choice(mons)
			c = choice(col)
			self.name = c[0] + " " + m[1]
			self.ch = Char(m[0], c[1])
			self.n = m[2]
		else:
			self.name = template.name
			self.ch = template.ch
			self.hp = template.base_hp

	def act(self):
		if self.has_los(self.g.p.getsquare()):
			self.act_towards(*self.g.p.getsquare().getloc())
		else:
			self.move_random()
