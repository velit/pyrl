import path
import rdg
import const.directions as DIRS
import const.game as CG
import const.debug as D

from pio import io
from char import Char
from random import randrange, choice
from generic_algorithms import bresenham, chebyshev_distance
from creature import Creature
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
			rdg.add_generated_tilefile(level_file, CG.LEVEL_TYPE)
		self.tiles = level_file.get_tilemap()
		self.creature_spawn_list = creature_spawn_list #TODO:

		for mons_file in level_file.monster_files:
			self._spawn_predefined_creature(mons_file)

		for x in range(CG.MONSTERS_PER_LEVEL):
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

	def _legal_loc(self, loc, dy=0, dx=0):
		return 0 <= loc // self.cols + dy < self.rows and 0 <= loc % self.cols + dx < self.cols

	def _spawn_random_creature(self):
		creature = Creature(choice(self.creature_spawn_list))
		self.add_creature(creature)

	def _spawn_predefined_creature(self, mons_file):
		creature = Creature(mons_file)
		self.add_creature(creature)

	def get_exit(self, loc):
		return self.tiles[loc].exit_point

	def get_coord(self, loc):
		return loc // self.cols, loc % self.cols

	def get_relative_loc(self, loc, direction):
		dy, dx = DIRS.DELTA[direction]
		if not self._legal_loc(loc, dy, dx):
			msg = "Location {} of {},{} is out of bounds."
			raise IndexError(msg.format(direction, *self.get_coord(loc)))
		else:
			return loc + self._get_loc(dy, dx)

	def get_loc_iter(self):
		return range(len(self.tiles))

	def get_visible_data(self, location_set):
		for loc in location_set:
			yield loc // self.cols, loc % self.cols, self._get_visible_char(loc)

	def get_memory_data(self, location_set):
		for loc in location_set:
			yield loc // self.cols, loc % self.cols, self.tiles[loc].memory_char

	def get_passage_loc(self, passage):
		if passage == CG.PASSAGE_RANDOM:
			return self.get_free_loc()
		else:
			return self.passage_locations[passage]

	def has_creature(self, loc):
		return loc in self.creatures

	def is_tile_passable(self, loc):
		return self.tiles[loc].is_passable

	def is_passable(self, loc):
		if loc in self.creatures:
			return False
		else:
			return self.tiles[loc].is_passable

	def is_see_through(self, loc):
		return self.tiles[loc].is_see_through

	def is_exit(self, loc):
		return self.tiles[loc].exit_point is not None

	def pop_modified_locs(self):
		mod_locs = self.modified_locations
		self.modified_locations = set()
		return mod_locs

	def update_visited_locs(self, locations):
		self.visited_locations |= locations

	def check_los(self, loc1, loc2):
		coordA = self.get_coord(loc1)
		coordB = self.get_coord(loc2)
		return all(self.is_see_through(self._get_loc(y, x)) for y, x in bresenham(coordA, coordB))

	def look_information(self, loc):

		if loc in self.visited_locations:
			information = "{}x{} ".format(*self.get_coord(loc))
			if self.has_creature(loc):
				c = self.creatures[loc]
				creature_stats = "{} hp:{}/{} sight:{} pv:{} dr:{} ar:{} dmg_bonus:{} dice:{} sides:{} "
				information += creature_stats.format(c.name, c.hp, c.max_hp, c.sight, c.pv, c.dr, c.ar, c.dmg_bonus,
						c.unarmed_dice, c.unarmed_sides)
				information += "target:{}".format(c.last_target_loc if c.last_target_loc is None else self.get_coord(c.last_target_loc))
			else:
				information += self.tiles[loc].name
			return information
		else:
			return "You don't know anything about this place."

	def pathing_neighbors(self, loc):
		for direction in DIRS.ALL_DIRECTIONS:
			neighbor_loc = self.get_relative_loc(loc, direction)
			if self.is_tile_passable(neighbor_loc):
				if direction in DIRS.DIAGONAL:
					yield neighbor_loc, int(round(self.tiles[loc].movement_cost * DIRS.DIAGONAL_MODIFIER))
				else:
					yield neighbor_loc, self.tiles[loc].movement_cost

	def pathing_heuristic(self, locA, locB, cross_product_loc=None):
		"""A* pathing heuristic."""
		ay, ax = self.get_coord(locA)
		by, bx = self.get_coord(locB)

		orthogonal_steps, diagonal_steps = chebyshev_distance((ay, ax), (by, bx))
		cost = CG.MOVEMENT_COST * (orthogonal_steps + diagonal_steps * DIRS.DIAGONAL_MODIFIER)

		if cross_product_loc is not None:
			cross_y, cross_x = self.get_coord(cross_product_loc)
			cross_product = abs((ax - bx) * (cross_y - by) - (cross_x - bx) * (ay - by)) / 100
			return cost + cross_product
		else:
			return cost

	def path(self, start_loc, goal_loc):
		return path.path(start_loc, goal_loc, self.pathing_neighbors, self.pathing_heuristic, self.cols)

	def add_creature(self, creature, loc=None):
		if loc is None:
			loc = self._get_free_loc()
		self.creatures[loc] = creature
		self.modified_locations.add(loc)
		creature.loc = loc
		self.turn_scheduler.add(creature)

	def remove_creature(self, loc):
		creature = self.creatures[loc]
		del self.creatures[loc]
		self.modified_locations.add(loc)
		creature.loc = None
		self.turn_scheduler.remove(creature)

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

	def creature_has_range(self, creature, target_loc):
		orth, dia = chebyshev_distance(self.get_coord(creature.loc), self.get_coord(target_loc))
		return orth + dia in (0, 1)

	def creature_has_sight(self, creature, target_loc):
		cy, cx = self.get_coord(creature.loc)
		ty, tx = self.get_coord(target_loc)
		#dy, dx = self.get_coord(max(creature.loc, target_loc) - min(creature.loc, target_loc))
		if (cy - ty) ** 2 + (cx - tx) ** 2 <= creature.sight ** 2:
		#if dy ** 2 + dx ** 2 <= creature.sight:
			return self.check_los(creature.loc, target_loc)
		else:
			return False

	def creature_attack(self, creature, target_loc):
		target = self.creatures[target_loc]
		attack_succeeds, damage = get_melee_attack(creature.ar, creature.get_damage_info(), target.dr, target.pv)
		if attack_succeeds:
			dies = target.lose_hp(damage)
			if dies:
				self.creature_death(target)
			return attack_succeeds, target.name, dies, damage
		else:
			return attack_succeeds, target.name, False, 0

	def creature_death(self, creature):
		self.remove_creature(creature.loc)

	def get_passable_locations(self, creature):
		locations = []
		for direction in DIRS.ALL_DIRECTIONS:
			loc = self.get_relative_loc(creature.loc, direction)
			if self.is_passable(loc):
				locations.append(loc)
		return locations
