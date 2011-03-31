import path

from bresenham import bresenham
from monster import Monster
from map import Map
from pio import io
from rdg import generateMap
from const.game import PASSAGE_RANDOM


class Level():

	def __init__(self, game, world_loc, level_template=None):
		self.g = game
		self.world_loc = world_loc

		self.creatures = []
		self.creature_squares = {}

		if level_template.map_not_rdg:
			template = level_template.template
		else:
			rows, cols = level_template.template
			template = generateMap(rows, cols, level_template.passages)

		self.map = Map(template)
		for x in range(100):
			self.addcreature(Monster(self.g, self))

	def getsquare(self, *args, **kwords):
		if "creature" in kwords:
			return self.creature_squares[kwords["creature"]]
		else:
			return self.map.getsquare(*args, **kwords)

	def get_free_square(self, *args, **kwords):
		return self.map.get_free_square(*args, **kwords)

	def get_random_square(self, *args, **kwords):
		return self.map.get_random_square(*args, **kwords)

	def visit_square(self, y, x):
		if self.legal_loc(y, x):
			s = self.getsquare(y, x)
			s.visit()
			self.g.p.visibility.add((s.y, s.x))

	def see_through(self, y, x):
		return self.legal_loc(y, x) and self.getsquare(y, x).see_through()

	def legal_loc(self, *args, **kwords):
		return self.map.legal_loc(*args, **kwords)

	def drawmap(self):
		io.drawmap(self.map)

	def drawmemory(self):
		io.drawmemory(self.map)

	def addcreature(self, creature, square=None):
		if square is None:
			square = self.get_free_square()
		self.creatures.append(creature)
		self.creature_squares[creature] = square
		square.creature = creature

	def removecreature(self, creature):
		square = self.getsquare(creature=creature)
		self.g.p.visi_mod.add(square.getloc())
		square.creature = None
		self.creatures.remove(creature)

	def movecreature(self, creature, new_square):
		old_square = self.getsquare(creature=creature)
		self.g.p.visi_mod.add(old_square.getloc())
		self.g.p.visi_mod.add(new_square.getloc())
		old_square.creature = None
		new_square.creature = creature
		self.creature_squares[creature] = new_square

	def killall(self):
		self.creatures.remove(self.g.p)
		while self.creatures:
			s = self.creatures.pop().getsquare()
			self.g.p.visi_mod.add(s.getloc())
			s.creature = None
		self.creatures.append(self.g.p)

	def neighbor_nodes(self, y, x):
		for j in range(y - 1, y + 2):
			for i in range(x - 1, x + 2):
				if not ((y == j and x == i) and self.legal_loc(y, x) and
						self.getsquare(j, i).tile_passable()):
					yield self.getsquare(j, i)

	def path(self, start, goal):
		return path.path(start, goal, self)

	def get_closest_in_square(self, creature, radius):
		y, x = self.square.y, self.square.x
		for i in range(radius * 2):
			c = self.getsquare(y - radius, x - radius + i).creature
			if c:
				return c
			c = self.getsquare(y - radius + i, x + radius).creature
			if c:
				return c
			c = self.getsquare(y + radius, x + radius - i).creature
			if c:
				return c
			c = self.getsquare(y + radius - i, x - radius).creature
			if c:
				return c
		else:
			return False

	def get_closest_creatureFromArea(self, creature):
		y, x = self.square.y, self.square.x
		radius = min(self.rows - y, y, self.cols - x, x)
		for i in range(1, radius):
			c = self.get_closest_in_square(creature, i)
			if c:
				return c
		else:
			return False

	def get_closest_creature(self, target_creature):
		tcreature_square = target_creature.square
		ty, tx = tcreature_square.y, tcreature_square.x
		best, cre = None, None
		for creature in self.creatures:
			creature_square = creature.square
			y, x = creature_square.y, creature_square.x
			a = (ty - y) ** 2 + (tx - x) ** 2
			if a > 0:
				if best is None:
					best = a
					cre = creature
				elif a < best:
					best = a
					cre = creature
		return cre

	def check_los(self, startSquare, targetsquare):
		y0, x0 = startSquare.y, startSquare.x
		y1, x1 = targetsquare.y, targetsquare.x
		g = self.getsquare
		return all(g(y, x).see_through() for y, x in bresenham(y0, x0, y1, x1))
