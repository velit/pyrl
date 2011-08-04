import random
from const.directions import ALL_DIRECTIONS

class AI:
	def __init__(self):
		pass

	def act(self, game, level, creature):
		move_random(game, level, creature)

def move_random(game, level, creature):
	for x in range(len(ALL_DIRECTIONS)):
		random_dir = random.choice(ALL_DIRECTIONS)
		loc = level.get_relative_loc(creature.loc, random_dir)
		if level.move_creature(creature, loc):
			break
