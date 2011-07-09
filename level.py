import path
import const.directions as dirs

from random import choice
from bresenham import bresenham
from monster import Monster
from map import Map
from pio import io
from rdg import generateMap

from const.game import SET_LEVEL, PREVIOUS_LEVEL, NEXT_LEVEL
from const.game import PASSAGE_DOWN, PASSAGE_UP


class Level:

	def __init__(self, game, world_loc, level_template=None):
		self.g = game
		self.world_loc = world_loc

		self.creatures = []
		self.creature_squares = {}
		self.creature_spawn_list = self.g.templs.get_level_monster_list(world_loc[1])

		self.passages = level_template.passages

		if level_template.map_not_rdg:
			template = level_template.template
		else:
			rows, cols = level_template.template
			template = generateMap(rows, cols, level_template.passages)

		self.map = Map(template)

		#for mons_templ in level_template.monsters:
		#	self.addcreature(Monster(self.g, self, mons_templ))
		#for x in range(100):
		#	self.spawn_random_creature()

	def getsquare(self, *a, **k):
		return self.map.getsquare(*a, **k)

	def get_creature_square(self, creature):
		return self.creature_squares[creature]

	def get_relative_loc(self, square, direction):
		y, x = square.getloc()
		dy, dx = dirs.DY[direction], dirs.DX[direction]
		return y+dy, x+dx

	def get_free_square(self, *a, **k):
		return self.map.get_free_square(*a, **k)

	def get_random_square(self, *a, **k):
		return self.map.get_random_square(*a, **k)

	def enter_passage(self, exit_point):
		passage_info = self.passages[exit_point]
		d, i = self.world_loc
		if passage_info[0] == SET_LEVEL:
			self.g.change_level(*passage_info[1])
		elif passage_info[0] == PREVIOUS_LEVEL:
			self.g.change_level(d, i - 1, PASSAGE_DOWN)
		elif passage_info[0] == NEXT_LEVEL:
			self.g.change_level(d, i + 1, PASSAGE_UP)

	def visit_square(self, y, x):
		if self.legal_coord(y, x):
			s = self.getsquare(y, x)
			s.visit()
			self.g.p.visibility.add((s.y, s.x))

	def see_through(self, y, x):
		return self.legal_coord(y, x) and self.getsquare(y, x).see_through()

	def legal_loc(self, *a, **k):
		return self.map.legal_loc(*a, **k)

	def legal_coord(self, *a, **k):
		return self.map.legal_coord(*a, **k)

	def drawmap(self):
		io.drawmap(self.map)

	def drawmemory(self):
		io.drawmemory(self.map)

	def spawn_random_creature(self):
		self.addcreature(Monster(self.g, self, choice(self.creature_spawn_list)))

	def addcreature(self, creature, square=None):
		if square is None:
			square = self.get_free_square()
		self.creatures.append(creature)
		self.creature_squares[creature] = square
		square.creature = creature

	def removecreature(self, creature):
		square = self.get_creature_square(creature)
		self.g.p.visi_mod.add(square.getloc())
		square.creature = None
		self.creatures.remove(creature)

	def _movecreature(self, creature, new_square):
		old_square = self.get_creature_square(creature)
		self.g.p.visi_mod.add(old_square.getloc())
		self.g.p.visi_mod.add(new_square.getloc())
		old_square.creature = None
		new_square.creature = creature
		self.creature_squares[creature] = new_square

	def movecreature(self, creature, y, x):
		if self.legal_coord(y, x):
			targetsquare = self.getsquare(y, x)
			if targetsquare.passable():
				self._movecreature(creature, targetsquare)
				return True
		return False

	def move_creature_to_dir(self, creature, direction):
		if direction == dirs.STOP:
			return True
		else:
			y, x = self.get_relative_loc(creature, direction)
			return self.movecreature(creature, y, x)

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
