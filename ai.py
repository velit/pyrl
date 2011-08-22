import random
import const.directions as CD

from pio import io

class AI:
	def __init__(self):
		pass

	def act(self, level, creature, loc):
		if level.creature_has_sight(creature, loc):
			creature.last_target_loc = loc
			if level.creature_has_range(creature, loc):
				return self.attack(level, creature, loc)
			else:
				return self.move_towards(level, creature, loc)
		elif creature.last_target_loc is not None:
			if creature.loc == creature.last_target_loc:
				creature.last_target_loc = None
			else:
				return self.move_towards(level, creature, creature.last_target_loc)
		else:
			return
			#return self.move_random(level, creature)

	def move_towards(self, level, creature, target_loc):
		locations = level.get_passable_locations(creature)
		if not len(locations) > 0:
			return
		min_loc = min(locations, key=lambda loc: level.pathing_heuristic(loc, target_loc))
		level.move_creature(creature, min_loc)

	def move_random(self, level, creature):
		for x in range(len(CD.ALL_DIRECTIONS)):
			random_dir = random.choice(CD.ALL_DIRECTIONS)
			loc = level.get_relative_loc(creature.loc, random_dir)
			if level.move_creature(creature, loc):
				break

	def attack(self, level, creature, target_loc):
		attack_succeeds, name, dies, damage = level.creature_attack(creature, target_loc)
		if attack_succeeds:
			if damage > 0:
				io.msg("The {} hits you for {} damage.".format(creature.name, damage))
			else:
				io.msg("The {} fails to hurt you.".format(creature.name))
		else:
			io.msg("The {} misses you.".format(creature.name))
