import path

from bresenham import bresenham
from monster import Monster
from map import Map, TileMap
from pio import io
from rdg import generateLevel

class Level():
	def __init__(self, game, dungeon_key, dungeon_i, tilemap=None, passages=()):
		self.g = game
		self.rows, self.cols = io.level_rows, io.level_cols
		self.world_loc = (dungeon_key, dungeon_i)

		self.creatures = []

		if tilemap is None:
			generateLevel(self, passages)
			for x in range(100):
				self.addcreature(Monster(self.g, self))
		else:
			self.map = Map(tilemap)

	def getsquare(self, *args, **kwords):
		return self.map.getsquare(*args, **kwords)

	def get_free_square(self):
		return self.map.get_free_square()

	def get_random_square(self):
		return self.map.get_random_square()

	def visit_square(self, y, x):
		if self.legal_yx(y, x):
			s = self.getsquare(y, x)
			s.visit()
			self.g.p.visibility.add((s.y, s.x))

	def see_through(self, y, x):
		return self.legal_yx(y, x) and self.getsquare(y, x).see_through()

	def legal_yx(self, y, x):
		return 0 <= y < self.rows and 0 <= x < self.cols

	def drawmap(self):
		io.drawmap(self.map)

	def drawmemory(self):
		io.drawmemory(self.map)

	def addcreature(self, creature, square = None):
		if square is None:
			square = self.get_free_square()
		self.creatures.append(creature)
		square.creature = creature
		creature.square = square

	def movecreature(self, creature, square):
		self.g.p.visi_mod.add((square.y, square.x))
		self.g.p.visi_mod.add((creature.square.y, creature.square.x))
		square.creature = creature
		creature.square.creature = None
		creature.square = square

	def removecreature(self, creature):
		self.g.p.visi_mod.add((creature.square.y, creature.square.x))
		creature.square.creature = None
		self.creatures.remove(creature)

	def killall(self):
		self.creatures.remove(self.g.p)
		while self.creatures:
			c = self.creatures.pop()
			self.g.p.visi_mod.add((c.square.y, c.square.x))
			c.square.creature = None
		self.creatures.append(self.g.p)

	def neighbor_nodes(self, y, x):
		for j in range(y-1, y+2):
			for i in range(x-1, x+2):
				if not ((y == j and x == i) and self.legal_yx(y, x) and
						self.getsquare(j, i).tile_passable()):
					yield self.getsquare(j, i)

	def path(self, start, goal):
		return path.path(start, goal, self)

	def get_closest_in_square(self, creature, radius):
		y, x = self.square.y, self.square.x
		for i in range(radius*2):
			c = self.getsquare(y-radius, x-radius+i).creature
			if c: return c
			c = self.getsquare(y-radius+i, x+radius).creature
			if c: return c
			c = self.getsquare(y+radius, x+radius-i).creature
			if c: return c
			c = self.getsquare(y+radius-i, x-radius).creature
			if c: return c
		else:
			return False

	def get_closest_creatureFromArea(self, creature):
		y,x=self.square.y, self.square.x
		radius = min(self.rows-y, y, self.cols-x, x)
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
			a = (ty-y) ** 2 + (tx-x) ** 2
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
		g=self.getsquare
		return all(g(y,x).see_through() for y, x in bresenham(y0, x0, y1, x1))
