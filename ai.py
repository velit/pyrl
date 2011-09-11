import random
import const.directions as CD
import const.game as CG


def act_towards(game, level, creature, alert_loc):
	if level.creature_has_sight(creature, alert_loc):
		if creature.can_act():
			direction = level.get_dir_if_valid(creature.loc, alert_loc)
			if direction is not None:
				game.creature_attack(level, creature, direction)
			else:
				move_towards(game, level, creature, alert_loc)
		if creature.target_loc is not None and creature.target_loc != alert_loc:
			creature.target_dir = level.get_dir_if_valid(creature.target_loc, alert_loc)
		creature.target_loc = alert_loc
	elif creature.can_act():
		if creature.loc == creature.target_loc:
			creature.target_loc = None
		elif creature.target_loc is not None:
			move_towards(game, level, creature, creature.target_loc)
		elif creature.target_dir is not None:
			target_loc = level.get_relative_loc(creature.loc, creature.target_dir)
			if level.creature_can_move(creature, creature.target_dir):
				game.creature_move(level, creature, creature.target_dir)
			elif level.has_creature(target_loc):
				if level.get_creature(target_loc).is_idle():
					game.creature_swap_places(level, creature, creature.target_dir)
			else:
				creature.target_dir = None
		else:
			move_random(game, level, creature)


def min_f(direction):
	pass


def move_towards(game, level, creature, target_loc):
	for direction in level.get_directions_closest_to_target(creature.loc, target_loc):
		if game.creature_move(level, creature, direction):
			return
	#directions = level.get_passable_directions(creature)
	#min_f = lambda dir_: level.distance_heuristic(level.get_relative_loc(creature.loc, dir_), target_loc)
	#min_dir = min(directions, key=min_f)
	#game.creature_move(level, creature, min_dir)


def move_random(game, level, creature):
	for x in range(len(CD.ALL)):
		direction = random.choice(CD.ALL)
		if game.creature_move(level, creature, direction):
			return
