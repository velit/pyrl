from char import Char
from creature import Creature
from random import choice
from templates import MonsterTemplate


#mons = (('k', "kobold", "him"), ('@', "bandit", "him"), ('g', "goblin", "him"),
#		('j', "jelly", "it"), ('c', "centipede", "it"))
#col = (("black", "black"), ("green", "light_green"),
#		("yellow", "yellow"), ("blue", "blue"))


mons = (
	MonsterTemplate("kobold", 10, Char('k', "green"), -3, 0),
	MonsterTemplate("goblin", 10, Char('g', "green"), -2, 0),
	MonsterTemplate("giant bat", 10, Char('B', "brown"), -3, 0),
	MonsterTemplate("orc", 10, Char('o', "green"), -1, 0),
	MonsterTemplate("giant worm", 10, Char('w', "brown"), 0, 0),
	MonsterTemplate("fire imp", 10, Char('I', "red"), 3, 0),
	MonsterTemplate("greater moloch", 10, Char('&', "light_yellow"), 18, 0),
)


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
