import random
from const.directions import ALL_DIRECTIONS

class AI:
	def __init__(self):
		pass

	def act(self, game, level, creature):
		locations = level.get_passable_locations(creature)
		#TODO: make hit player also fix min
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
