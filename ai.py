import random
import const.directions as CD
import const.game as CG

from pio import io

class AI:
	def __init__(self):
		pass

	def act(self, game, level, creature, loc=None):
		if loc is not None:
			if level.creature_has_sight(creature, loc):
				creature.target_loc = loc
				direction = level.get_dir_if_valid(creature.loc, loc)
				if direction is not None:
					game.creature_attack(level, creature, direction)
				else:
					self.move_towards(game, level, creature, loc)
			elif creature.target_loc is not None:
				if creature.loc == creature.target_loc:
					creature.target_loc = None
				else:
					self.move_towards(game, level, creature, creature.target_loc)
			else:
				self.move_random(game, level, creature)
		else:
			self.move_random(game, level, creature)

	def move_towards(self, game, level, creature, target_loc):
		directions = level.get_passable_directions(creature)
		min_f = lambda dir_: level.distance_heuristic(level.get_relative_loc(creature.loc, dir_), target_loc)
		min_dir = min(directions, key=min_f)
		game.creature_move(level, creature, min_dir)

	def move_random(self, game, level, creature):
		for x in range(len(CD.ALL)):
			direction = random.choice(CD.ALL)
			if game.creature_move(level, creature, direction):
				return
