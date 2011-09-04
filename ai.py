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
					return self.move_towards(game, level, creature, loc)
			elif creature.target_loc is not None:
				if creature.loc == creature.target_loc:
					creature.target_loc = None
				else:
					return self.move_towards(game, level, creature, creature.target_loc)
			else:
				return
		return self.move_random(game, level, creature)

	def move_towards(self, game, level, creature, target_loc):
		directions = level.get_passable_directions(creature)
		if not len(directions) > 0:
			return
		min_f = lambda dir_: level.distance_heuristic(level.get_relative_loc(creature.loc, dir_), target_loc)
		min_dir = min(directions, key=min_f)
		game.creature_move(level, creature, min_dir)

	def move_random(self, game, level, creature):
		directions = level.get_passable_directions(creature)
		if not len(directions) > 0:
			return
		dir_ = random.choice(directions)
		game.creature_move(level, creature, dir_)

	def attack(self, game, level, creature, target_loc):
		target = level.get_creature(target_loc)
		game.creature_attack(level, creature, target)
