import path
import rdg
import const.directions as dirs

from random import randrange, choice
from bresenham import bresenham
from creature import Creature
from const.game import PASSAGE_RANDOM, MONSTERS_PER_LEVEL
from turn_scheduler import TurnScheduler
from combat import get_melee_attack

class Level:

	def __init__(self, world_loc, level_file, creature_spawn_list):
		self.modified_locations = set()
		self.visited_locations = set()
		self.turn_scheduler = TurnScheduler()
		self.creatures = {}
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
			self.add_creature(Creature(mons_file))

		for x in range(MONSTERS_PER_LEVEL):
			self._spawn_random_creature()

	def _get_free_loc(self):
		while True:
			loc = self._get_random_loc()
			if self.is_passable(loc):
				return loc

	def _get_random_loc(self):
		return randrange(len(self.tiles))

	def _get_visible_char(self, loc):
		if loc in self.creatures:
			return self.creatures[loc].char
		else:
			return self.tiles[loc].visible_char

	def _get_loc(self, y, x):
		return y * self.cols + x

	def _legal_loc(self, loc):
		return 0 <= loc < self.rows * self.cols

	def _make_coord_to_legal_loc(self, y, x):
		if y < 0: y = 0
		elif y >= self.rows: y = self.rows - 1
		if x < 0: x = 0
		elif x >= self.cols: x = self.cols - 1
		return self._get_loc(y, x)

	def _spawn_random_creature(self):
		self.add_creature(Creature(choice(self.creature_spawn_list)))

	def get_exit(self, loc):
		return self.tiles[loc].exit_point

	def get_coord(self, loc):
		return loc // self.cols, loc % self.cols

	def get_relative_loc(self, loc, direction):
		y, x = self.get_coord(loc)
		dy, dx = dirs.DELTA[direction]
		ny, nx = y + dy, x + dx
		return self._make_coord_to_legal_loc(ny, nx)

	def get_loc_iter(self):
		return range(len(self.tiles))

	def get_visible_data(self, location_set):
		for loc in location_set:
			yield loc // self.cols, loc % self.cols, self._get_visible_char(loc)

	def get_memory_data(self, location_set):
		for loc in location_set:
			yield loc // self.cols, loc % self.cols, self.tiles[loc].memory_char

	def get_passage_loc(self, passage):
		if passage == PASSAGE_RANDOM:
			return self.get_free_loc()
		else:
			return self.passage_locations[passage]

	def has_creature(self, loc):
		return loc in self.creatures

	def is_passable(self, loc):
		if loc in self.creatures:
			return False
		else:
			return self.tiles[loc].is_passable

	def is_see_through(self, loc):
		return self.tiles[loc].is_see_through

	def is_exit(self, loc):
		return self.tiles[loc].exit_point is not None

	def add_creature(self, creature, loc=None):
		if loc is None:
			loc = self._get_free_loc()
		self.creatures[loc] = creature
		self.turn_scheduler.add(creature)
		self.modified_locations.add(loc)
		creature.loc = loc

	def remove_creature(self, loc):
		creature = self.creatures[loc]
		del self.creatures[loc]
		self.turn_scheduler.remove(creature)
		self.modified_locations.add(loc)
		creature.loc = None

	def _move_creature(self, creature, new_loc):
		self.modified_locations.add(creature.loc)
		self.modified_locations.add(new_loc)
		del self.creatures[creature.loc]
		self.creatures[new_loc] = creature
		creature.loc = new_loc

	def move_creature(self, creature, loc):
		if self._legal_loc(loc):
			if self.is_passable(loc):
				self._move_creature(creature, loc)
				return True
		return False

	def creature_attack(self, creature, target_loc):
		target = self.creatures[target_loc]
		attack_succeeds, damage = get_melee_attack(creature.ar, creature.get_damage_info(), target.dr, target.pv)
		if attack_succeeds:
			dies = target.lose_hp(damage)
			if dies:
				self.remove_creature(target_loc)
			return attack_succeeds, target.name, dies, damage
		else:
			return attack_succeeds, target.name, False, 0

	def pop_modified_locs(self):
		mod_locs = self.modified_locations
		self.modified_locations = set()
		return mod_locs

	def update_visited_locs(self, locations):
		self.visited_locations |= locations

	def check_los(self, loc1, loc2):
		y0, x0 = self.get_coord(loc1)
		y1, x1 = self.get_coord(loc2)
		return all(self.is_see_through(self._get_loc(y, x)) for y, x in bresenham(y0, x0, y1, x1))

	def get_information(self, loc):
		if loc in self.visited_locations:
			if self.has_creature(loc):
				return self.creatures[loc].name
			else:
				return self.tiles[loc].name
		else:
			return "You don't know anything about this place."

	def get_legal_neighbor_locs(self, loc):
		pass

	def get_pathable_neighbor_locs(self, loc):
		for direction in dirs.ALL_DIRECTIONS:
			neighbor_loc = self.get_relative_loc(loc, direction)
			if self.is_passable(
			yield 
				if not ((y == j and x == i) and self.legal_loc(y, x) and self.getsquare(j, i).tile_passable()):

	def get_passable_neighbor_locs(self, loc):
		pass

	#def path(self, start, goal):
	#	return path.path(start, goal, self)
