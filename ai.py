import random
import const.directions as CD

from pio import io

class AI:
	def __init__(self):
		pass

	def act(self, game, level, creature, loc=None):
		if loc is not None:
			if level.creature_has_sight(creature, loc):
				creature.target_loc = loc
				if level.creature_has_range(creature, loc):
					return self.attack(game, level, creature, loc)
				else:
					return self.move_towards(level, creature, loc)
			elif creature.target_loc is not None:
				if creature.loc == creature.target_loc:
					creature.target_loc = None
				else:
					return self.move_towards(level, creature, creature.target_loc)
			else:
				return
		#return self.move_random(level, creature)

	def move_towards(self, level, creature, target_loc):
		locations = level.get_passable_locations(creature)
		if not len(locations) > 0:
			return
		min_loc = min(locations, key=lambda loc: level.distance_cost(loc, target_loc))
		level.move_creature(creature, min_loc)

	def move_random(self, level, creature):
		for x in range(len(CD.ALL_DIRECTIONS)):
			random_dir = random.choice(CD.ALL_DIRECTIONS)
			loc = level.get_relative_loc(creature.loc, random_dir)
			if level.move_creature(creature, loc):
				break

	def attack(self, game, level, creature, target_loc):
		target = level.get_creature(target_loc)
		game.creature_attack(level, creature, target)
