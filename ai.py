import random

from const.directions import ALL_DIRECTIONS
from pio import io

class AI:
	def __init__(self):
		pass

	def act(self, game, level, creature):
		if level.creature_can_reach(creature, game.player.loc):
			attack_succeeds, name, dies, damage = level.creature_attack(creature, game.player.loc)
			if attack_succeeds:
				if damage > 0:
					io.msg("The {} hits you for {} damage.".format(creature.name, damage))
				else:
					io.msg("The {} fails to hurt you.".format(creature.name))
			else:
				io.msg("The {} misses you.".format(creature.name))
			return

		locations = level.get_passable_locations(creature)
		if not len(locations) > 0:
			return
		min_loc = locations[0]
		min_cost = level.pathing_heuristic(min_loc, game.player.loc)
		for cur_loc in locations:
			cur_cost = level.pathing_heuristic(cur_loc, game.player.loc)
			if cur_cost < min_cost:
				min_loc = cur_loc
				min_cost = cur_cost
		level.move_creature(creature, min_loc)

def move_random(game, level, creature):
	for x in range(len(ALL_DIRECTIONS)):
		random_dir = random.choice(ALL_DIRECTIONS)
		loc = level.get_relative_loc(creature.loc, random_dir)
		if level.move_creature(creature, loc):
			break
