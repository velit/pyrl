from __future__ import division
import random
import path
import rdg
import const.directions as dirs
import const.game as GAME
import const.debug as DEBUG

from creature import Creature
from turn_scheduler import TurnScheduler
from generic_algorithms import bresenham, cross_product, get_vector


class TileStructure(list):
	def __init__(self, level_file):
		list.__init__(self, level_file.tilemap())
		self.rows = level_file.rows
		self.cols = level_file.cols

	def __getitem__(self, coord):
		return list.__getitem__(self, coord[0] * self.cols + coord[1])

	def __setitem__(self, coord, value):
		return list.__setitem__(self, coord[0] * self.cols + coord[1], value)

	def __delitem__(self, coord):
		return list.__delitem__(self, coord[0] * self.cols + coord[1])


class Level(object):

	def __init__(self, world_loc, level_file, creature_spawn_list):
		self.modified_locations = set()
		self.visited_locations = set()
		self.turn_scheduler = TurnScheduler()
		self.creatures = {}
		self.world_loc = world_loc
		self.danger_level = level_file.danger_level
		self.passage_locations = level_file.passage_locations
		if level_file.use_map_generator():
			rdg.add_generated_tilefile(level_file, GAME.LEVEL_TYPE)
		self.tiles = TileStructure(level_file)
		self.creature_spawn_list = creature_spawn_list #TODO:

		for mons_file in level_file.monster_files:
			self._spawn_predefined_creature(mons_file)

		for x in xrange(GAME.MONSTERS_PER_LEVEL):
			self._spawn_random_creature()

	# nudge_coord nudges towards a line between this and start_coord
	def _a_star_heuristic(self, start_coord, end_coord, nudge_coord):
		cost = self.distance_heuristic(start_coord, end_coord)
		if DEBUG.CROSS:
			cost += cross_product(start_coord, end_coord, nudge_coord) / DEBUG.CROSS_MOD
		return cost

	def _a_star_neighbors(self, coord):
		for direction in dirs.ALL:
			neighbor_coord = self.get_relative_coord(coord, direction)
			if self.tiles[neighbor_coord].is_passable:
				if direction in dirs.DIAGONAL:
					yield neighbor_coord, round(self.tiles[coord].movement_cost * GAME.DIAGONAL_MODIFIER)
				else:
					yield neighbor_coord, self.tiles[coord].movement_cost

	def _get_free_coord(self):
		while True:
			coord = self._get_random_coord()
			if self.is_passable(coord):
				return coord

	def _get_random_coord(self):
		return random.randrange(self.tiles.rows), random.randrange(self.tiles.cols)

	def _get_visible_char(self, coord):
		if coord in self.creatures:
			return self.get_creature(coord).char
		else:
			return self.tiles[coord].visible_char

	def _spawn_random_creature(self):
		creature = Creature(random.choice(self.creature_spawn_list))
		self.add_creature(creature)

	def _spawn_predefined_creature(self, mons_file):
		creature = Creature(mons_file)
		self.add_creature(creature)

	def legal_coord(self, coord, direction=(0,0)):
		y, x = coord
		return (0 <= (y + direction[0]) < self.tiles.rows) and (0 <= (x + direction[1]) < self.tiles.cols)

	def get_exit(self, coord):
		return self.tiles[coord].exit_point

	def get_creature(self, coord):
		return self.creatures[coord]

	def get_relative_coord(self, coord, direction):
		return coord[0] + direction[0], coord[1] + direction[1]

	def get_coord_iter(self):
		for y in xrange(self.tiles.rows):
			for x in xrange(self.tiles.cols):
				yield y, x

	def get_visible_data(self, location_set):
		for (y, x) in location_set:
			yield y, x, self._get_visible_char((y, x))

	def get_memory_data(self, location_set):
		for (y, x) in location_set:
			yield y, x, self.tiles[y, x].memory_char

	def get_passage_coord(self, passage):
		if passage == GAME.PASSAGE_RANDOM:
			return self.get_free_coord()
		else:
			return self.passage_locations[passage]

	def has_creature(self, coord):
		return coord in self.creatures

	def is_passable(self, coord):
		if coord in self.creatures:
			return False
		else:
			return self.tiles[coord].is_passable

	def is_pathable(self, coord):
		return self.tiles[coord].is_passable

	def is_see_through(self, coord):
		return self.tiles[coord].is_see_through

	def is_exit(self, coord):
		return self.tiles[coord].exit_point is not None

	def pop_modified_locations(self):
		mod_locs = self.modified_locations
		self.modified_locations = set()
		return mod_locs

	def update_visited_locations(self, locations):
		self.visited_locations |= locations

	def check_los(self, coordA, coordB):
		return not (any(not self.is_see_through(coord) for coord in bresenham(coordA, coordB)) and
				any(not self.is_see_through(coord) for coord in bresenham(coordB, coordA)))

	def get_last_pathable_coord(self, coord_start, coord_end):
		last = coord_start
		for coord in bresenham(coord_start, coord_end):
			if self.is_pathable(coord):
				last = coord
			else:
				break
		return last

	def distance_heuristic(self, coordA, coordB):
		return round(path.heuristic(coordA, coordB, GAME.MOVEMENT_COST, GAME.DIAGONAL_MODIFIER))

	def movement_cost(self, direction, end_coord):
		if direction in dirs.ORTHOGONAL:
			value = self.tiles[end_coord].movement_cost
		elif direction in dirs.DIAGONAL:
			value = round(self.tiles[end_coord].movement_cost * GAME.DIAGONAL_MODIFIER)
		elif direction == dirs.STOP:
			value = GAME.MOVEMENT_COST
		else:
			raise GAME.PyrlException("Invalid direction: {}".format(direction))
		return value

	def path(self, start_coord, goal_coord):
		return path.path(start_coord, goal_coord, self._a_star_neighbors, self._a_star_heuristic)

	def look_information(self, coord):
		#if coord in self.visited_locations:
		information = "{}x{} ".format(*coord)
		if self.has_creature(coord):
			c = self.get_creature(coord)
			creature_stats = "{} hp:{}/{} sight:{} pv:{} dr:{} ar:{} attack:{}D{}+{}"
			information += creature_stats.format(c.name, c.hp, c.max_hp, c.sight, c.pv, c.dr, c.ar, *c.get_damage_info())
			information += " target:{}".format(coord)
			information += " direction:{}".format(c.chase_vector)
		else:
			information += self.tiles[coord].name
		return information
		#else:
		#	return "You don't know anything about this place."

	def add_creature(self, creature, coord=None):
		if coord is None:
			coord = self._get_free_coord()
		self.creatures[coord] = creature
		self.modified_locations.add(coord)
		creature.coord = coord
		self.turn_scheduler.add(creature)

	def remove_creature(self, creature):
		coord = creature.coord
		del self.creatures[coord]
		self.modified_locations.add(coord)
		creature.coord = None
		self.turn_scheduler.remove(creature)

	def move_creature(self, creature, new_coord):
		self.modified_locations.add(creature.coord)
		self.modified_locations.add(new_coord)
		del self.creatures[creature.coord]
		self.creatures[new_coord] = creature
		creature.coord = new_coord

	def swap_creature(self, creatureA, creatureB):
		self.modified_locations.add(creatureA.coord)
		self.modified_locations.add(creatureB.coord)
		self.creatures[creatureA.coord] = creatureB
		self.creatures[creatureB.coord] = creatureA
		creatureA.coord, creatureB.coord = creatureB.coord, creatureA.coord

	def creature_is_swappable(self, coord):
		try:
			return self.get_creature(coord).is_idle()
		except KeyError:
			return False

	def creature_can_reach(self, creature, target_coord):
		if creature.coord == target_coord:
			return True
		else:
			vector = get_vector(creature.coord, target_coord)
			if vector in dirs.ALL:
				return True
			else:
				return False

	def creature_can_move(self, creature, direction):
		if direction == dirs.STOP:
			return True
		elif self.legal_coord(creature.coord, direction):
			coord = self.get_relative_coord(creature.coord, direction)
			return self.is_passable(coord)
		else:
			return False

	def creature_has_sight(self, creature, target_coord):
		cy, cx = creature.coord
		ty, tx = target_coord
		if (cy - ty) ** 2 + (cx - tx) ** 2 <= creature.sight ** 2:
			return self.check_los(creature.coord, target_coord)
		else:
			return False
