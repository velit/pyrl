import path
import rdg
import const.directions as dirs

from random import randrange, choice
from bresenham import bresenham
from monster import Monster
from pio import io
from const.game import PASSAGE_RANDOM
from turn_scheduler import TurnScheduler

class Level:

	def __init__(self, game, world_loc, level_file, creature_spawn_list):
		self.turn_scheduler = TurnScheduler()
		self.creatures = {}
		self.g = game
		self.world_loc = world_loc
		self.rows = level_file.rows
		self.cols = level_file.cols
		self.danger_level = level_file.danger_level
		self.passage_locations = level_file.passage_locations
		if level_file.tilefile is None:
			rdg.add_generated_tilefile(level_file)
		self.tiles = level_file.get_tilemap()
		self.creature_spawn_list = creature_spawn_list #TODO:

		for mons_file in level_file.monster_files:
			self.addcreature(Monster(self.g, mons_file))

		for x in range(100):
			self.spawn_random_creature()

	def get_passage_loc(self, passage):
		if passage == PASSAGE_RANDOM:
			return self.get_free_loc()
		else:
			return self.passage_locations[passage]

	def get_free_loc(self):
		while True:
			loc = self.get_random_loc()
			if self.passable(loc):
				return loc

	def get_random_loc(self):
		return randrange(len(self.tiles))

	def passable(self, loc):
		if loc in self.creatures:
			return False
		else:
			return self.tiles[loc].passable

	def see_through(self, loc):
		return self.tiles[loc].see_through

	def get_loc_iterator(self):
		return range(len(self.tiles))

	def get_visible_char_data(self, loc, color_shift=""):
		if loc in self.creatures:
			symbol, color = self.creatures[loc].char
		else:
			symbol, color = self.tiles[loc].visible_char
		return symbol, color + color_shift

	def get_memory_char_data(self, loc, color_shift=""):
		symbol, color = self.tiles[loc].memory_char
		return symbol, color + color_shift

	def isexit(self, loc):
		return self.tiles[loc].exit_point is not None

	def getexit(self, loc):
		return self.tiles[loc].exit_point

	def legal_loc(self, loc):
		return 0 <= loc < self.rows * self.cols

	def get_loc(self, y, x):
		return y * self.cols + x

	def get_coord(self, loc):
		return loc // self.cols, loc % self.cols

	def get_relative_loc(self, loc, direction):
		return loc + self.get_loc(*dirs.DELTA[direction])

	def draw(self):
		io.drawlevel(self)

	def drawmemory(self):
		io.drawmemory(self)

	def spawn_random_creature(self):
		self.addcreature(Monster(self.g, choice(self.creature_spawn_list)))

	def addcreature(self, creature, loc=None):
		if loc is None:
			loc = self.get_free_loc()
		self.creatures[loc] = creature
		creature.loc = loc
		self.turn_scheduler.add(creature)
		self.g.player.turn_visibility.discard(loc)
		if self.world_loc not in creature.level_memory:
			creature.level_memory[self.world_loc] = set()

	def removecreature(self, creature):
		loc = creature.loc
		del self.creatures[loc]
		self.turn_scheduler.remove(creature)
		self.g.player.turn_visibility.discard(loc)
		creature.loc = None

	def _movecreature(self, creature, new_loc):
		old_loc = creature.loc
		self.g.player.turn_mod.add(old_loc)
		self.g.player.turn_mod.add(new_loc)
		del self.creatures[old_loc]
		self.creatures[new_loc] = creature
		creature.loc = new_loc

	def movecreature(self, creature, loc):
		if self.legal_loc(loc):
			if self.passable(loc):
				self._movecreature(creature, loc)
				return True
		return False

	def move_creature_to_dir(self, creature, direction):
		if direction == dirs.STOP:
			return True
		else:
			loc = self.get_relative_loc(creature.loc, direction)
			return self.movecreature(creature, loc)

	def killall(self):
		creatures = self.turn_scheduler.get_actor_set()
		creatures.remove(self.g.player)
		for c in creatures:
			c.die()

	#def neighbor_nodes(self, y, x):
	#	for j in range(y - 1, y + 2):
	#		for i in range(x - 1, x + 2):
	#			if not ((y == j and x == i) and self.legal_loc(y, x) and
	#					self.getsquare(j, i).tile_passable()):
	#				yield self.getsquare(j, i)

	#def path(self, start, goal):
	#	return path.path(start, goal, self)

	#def get_closest_in_square(self, creature, radius):
	#	y, x = self.square.y, self.square.x
	#	for i in range(radius * 2):
	#		c = self.getsquare(y - radius, x - radius + i).creature
	#		if c:
	#			return c
	#		c = self.getsquare(y - radius + i, x + radius).creature
	#		if c:
	#			return c
	#		c = self.getsquare(y + radius, x + radius - i).creature
	#		if c:
	#			return c
	#		c = self.getsquare(y + radius - i, x - radius).creature
	#		if c:
	#			return c
	#	else:
	#		return False

	#def get_closest_creatureFromArea(self, creature):
	#	y, x = self.square.y, self.square.x
	#	radius = min(self.rows - y, y, self.cols - x, x)
	#	for i in range(1, radius):
	#		c = self.get_closest_in_square(creature, i)
	#		if c:
	#			return c
	#	else:
	#		return False

	#def get_closest_creature(self, target_creature):
	#	tcreature_square = target_creature.square
	#	ty, tx = tcreature_square.y, tcreature_square.x
	#	best, cre = None, None
	#	for creature in self.creatures:
	#		creature_square = creature.square
	#		y, x = creature_square.y, creature_square.x
	#		a = (ty - y) ** 2 + (tx - x) ** 2
	#		if a > 0:
	#			if best is None:
	#				best = a
	#				cre = creature
	#			elif a < best:
	#				best = a
	#				cre = creature
	#	return cre

	#def check_los(self, startSquare, targetsquare):
	#	y0, x0 = startSquare.y, startSquare.x
	#	y1, x1 = targetsquare.y, targetsquare.x
	#	g = self.getsquare
	#	return all(g(y, x).see_through() for y, x in bresenham(y0, x0, y1, x1))
