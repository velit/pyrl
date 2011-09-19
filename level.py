import random
import path
import rdg
import const.directions as dirs
import const.game as GAME
import const.debug as DEBUG

from char import Char
from creature import Creature
from turn_scheduler import TurnScheduler
from generic_algorithms import bresenham, chebyshev, cross_product

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
			rdg.add_generated_tilefile(level_file, GAME.LEVEL_TYPE)
		self.tiles = level_file.get_tilemap()
		self.creature_spawn_list = creature_spawn_list #TODO:

		for mons_file in level_file.monster_files:
			self._spawn_predefined_creature(mons_file)

		for x in range(GAME.MONSTERS_PER_LEVEL):
			self._spawn_random_creature()

	def _a_star_heuristic(self, start_loc, end_loc, nudge_towards_from_start_loc):
		cost = self.distance_heuristic(start_loc, end_loc)
		if DEBUG.CROSS:
			coord_start = self.get_coord(start_loc)
			coord_end = self.get_coord(end_loc)
			coord_nudge = self.get_coord(nudge_towards_from_start_loc)
			cost += cross_product(coord_start, coord_end, coord_nudge) / DEBUG.CROSS_MOD
		return cost

	def _a_star_neighbors(self, loc):
		for direction in dirs.ALL:
			neighbor_loc = self.get_relative_loc(loc, direction)
			if self.get_tile(neighbor_loc).is_passable:
				if direction in dirs.DIAGONAL:
					yield neighbor_loc, round(self.get_tile(loc).movement_cost * GAME.DIAGONAL_MODIFIER)
				else:
					yield neighbor_loc, self.get_tile(loc).movement_cost

	def _get_free_loc(self):
		while True:
			loc = self._get_random_loc()
			if self.is_passable(loc):
				return loc

	def _get_random_loc(self):
		return random.randrange(len(self.tiles))

	def _get_visible_char(self, loc):
		if loc in self.creatures:
			return self.get_creature(loc).char
		else:
			return self.get_tile(loc).visible_char

	def _get_loc(self, y, x):
		return y * self.cols + x

	def _spawn_random_creature(self):
		creature = Creature(random.choice(self.creature_spawn_list))
		self.add_creature(creature)

	def _spawn_predefined_creature(self, mons_file):
		creature = Creature(mons_file)
		self.add_creature(creature)

	def legal_loc(self, loc, direction=(0,0)):
		return 0 <= loc // self.cols + direction[0] < self.rows and 0 <= loc % self.cols + direction[1] < self.cols

	def get_exit(self, loc):
		return self.get_tile(loc).exit_point

	def get_coord(self, loc):
		return loc // self.cols, loc % self.cols

	def get_creature(self, loc):
		return self.creatures[loc]

	def get_tile(self, loc):
		return self.tiles[loc]

	def get_relative_loc(self, loc, direction):
		return loc + self._get_loc(direction[0], direction[1])

	def get_loc_iter(self):
		return range(len(self.tiles))

	def get_visible_data(self, location_set):
		for loc in location_set:
			yield loc // self.cols, loc % self.cols, self._get_visible_char(loc)

	def get_memory_data(self, location_set):
		for loc in location_set:
			yield loc // self.cols, loc % self.cols, self.get_tile(loc).memory_char

	def get_passage_loc(self, passage):
		if passage == GAME.PASSAGE_RANDOM:
			return self.get_free_loc()
		else:
			return self.passage_locations[passage]

	def has_creature(self, loc):
		return loc in self.creatures

	def is_passable(self, loc):
		if loc in self.creatures:
			return False
		else:
			return self.get_tile(loc).is_passable

	def is_pathable(self, loc):
		return self.get_tile(loc).is_passable

	def is_see_through(self, loc):
		return self.get_tile(loc).is_see_through

	def is_exit(self, loc):
		return self.get_tile(loc).exit_point is not None

	def pop_modified_locs(self):
		mod_locs = self.modified_locations
		self.modified_locations = set()
		return mod_locs

	def update_visited_locs(self, locations):
		self.visited_locations |= locations

	def check_los(self, loc1, loc2):
		coordA = self.get_coord(loc1)
		coordB = self.get_coord(loc2)
		return not (any(not self.is_see_through(self._get_loc(y, x)) for y, x in bresenham(coordA, coordB)) and
				any(not self.is_see_through(self._get_loc(y, x)) for y, x in bresenham(coordB, coordA)))

	def get_last_pathable_loc(self, loc_start, loc_end):
		last = loc_start
		to_coord = self.get_coord
		for loc in (self._get_loc(*coord) for coord in bresenham(to_coord(loc_start), to_coord(loc_end))):
			if self.is_pathable(loc):
				last = loc
			else:
				break
		return last

	def distance_heuristic(self, locA, locB):
		coordA, coordB = self.get_coord(locA), self.get_coord(locB)
		return round(path.heuristic(coordA, coordB, GAME.MOVEMENT_COST, GAME.DIAGONAL_MODIFIER))

	def movement_cost(self, direction, end_loc):
		if direction in dirs.ORTHOGONAL:
			value = self.get_tile(end_loc).movement_cost
		elif direction in dirs.DIAGONAL:
			value = round(self.get_tile(end_loc).movement_cost * GAME.DIAGONAL_MODIFIER)
		elif direction == dirs.STOP:
			value = GAME.MOVEMENT_COST
		else:
			raise Exception(direction)
		return value

	def path(self, start_loc, goal_loc):
		return path.path(start_loc, goal_loc, self._a_star_neighbors, self._a_star_heuristic, self.cols)

	def look_information(self, loc):
		#if loc in self.visited_locations:
		information = "{}x{} ".format(*self.get_coord(loc))
		if self.has_creature(loc):
			c = self.get_creature(loc)
			creature_stats = "{} hp:{}/{} sight:{} pv:{} dr:{} ar:{} attack:{}D{}+{}"
			information += creature_stats.format(c.name, c.hp, c.max_hp, c.sight, c.pv, c.dr, c.ar, *c.get_damage_info())
			information += " target:{}".format(c.target_loc if c.target_loc is None else self.get_coord(c.target_loc))
			information += " direction:{}".format(c.chase_vector)
		else:
			information += self.get_tile(loc).name
		return information
		#else:
		#	return "You don't know anything about this place."

	def add_creature(self, creature, loc=None):
		if loc is None:
			loc = self._get_free_loc()
		self.creatures[loc] = creature
		self.modified_locations.add(loc)
		creature.loc = loc
		self.turn_scheduler.add(creature)

	def remove_creature(self, creature):
		loc = creature.loc
		del self.creatures[loc]
		self.modified_locations.add(loc)
		creature.loc = None
		self.turn_scheduler.remove(creature)

	def move_creature(self, creature, new_loc):
		self.modified_locations.add(creature.loc)
		self.modified_locations.add(new_loc)
		del self.creatures[creature.loc]
		self.creatures[new_loc] = creature
		creature.loc = new_loc

	def swap_creature(self, creatureA, creatureB):
		self.modified_locations.add(creatureA.loc)
		self.modified_locations.add(creatureB.loc)
		self.creatures[creatureA.loc] = creatureB
		self.creatures[creatureB.loc] = creatureA
		creatureA.loc, creatureB.loc = creatureB.loc, creatureA.loc

	def get_vector(self, loc_origin, loc_target):
		oy, ox = self.get_coord(loc_origin)
		ty, tx = self.get_coord(loc_target)
		return (ty - oy, tx - ox)

	def creature_is_swappable(self, loc):
		try:
			return self.get_creature(loc).is_idle()
		except KeyError:
			return False

	def creature_can_reach(self, creature, target_loc):
		if creature.loc == target_loc:
			return True
		else:
			cy, cx = self.get_coord(creature.loc)
			ty, tx = self.get_coord(target_loc)
			vector = (cy - ty, cx - tx)
			if vector in dirs.ALL:
				return True
			else:
				return False

	def creature_can_move(self, creature, direction):
		if direction == dirs.STOP:
			return True
		elif self.legal_loc(creature.loc, direction):
			loc = self.get_relative_loc(creature.loc, direction)
			return self.is_passable(loc)
		else:
			return False

	def creature_has_sight(self, creature, target_loc):
		cy, cx = self.get_coord(creature.loc)
		ty, tx = self.get_coord(target_loc)
		if (cy - ty) ** 2 + (cx - tx) ** 2 <= creature.sight ** 2:
			return self.check_los(creature.loc, target_loc)
		else:
			return False
