import random
import const.directions as DIRS
import const.game as GAME
import const.creature_actions as ACTIONS
from generic_algorithms import resize_vector_to_len


def act_alert(game, level, creature, alert_loc):
	# creature seeing actions
	if level.creature_has_sight(creature, alert_loc):
		if creature.target_loc is not None and creature.target_loc != alert_loc:
			creature.chase_vector = level.get_vector(creature.target_loc, alert_loc)
		creature.target_loc = alert_loc

		if creature.can_act():
			if level.creature_can_reach(creature, alert_loc):
				game.creature_attack(level, creature, level.get_vector(creature.loc, creature.target_loc))
			else:
				move_towards(game, level, creature, alert_loc)

	# creature actions
	elif creature.can_act():
		# chasing
		if creature.target_loc == creature.loc:
			creature.target_loc = None
			if creature.chase_vector is not None:
				creature.chase_vector = resize_vector_to_len(creature.chase_vector, creature.sight)
				overarching_target = level.get_relative_loc(creature.loc, creature.chase_vector)
				target_loc = level.get_last_pathable_loc(creature.loc, overarching_target)
				if creature.loc != target_loc:
					creature.target_loc = target_loc
				else:
					creature.chase_vector = None

		if creature.target_loc is not None:
			move_towards(game, level, creature, creature.target_loc)
		else:
			move_random(game, level, creature)


def move_towards(game, level, creature, target_loc):
	best_action = ACTIONS.MOVE
	best_direction = DIRS.STOP
	best_cost = None
	for direction in DIRS.ALL:
		loc = level.get_relative_loc(creature.loc, direction)
		if level.is_passable(loc):
			action = ACTIONS.MOVE
		elif level.creature_is_swappable(loc):
			action = ACTIONS.SWAP
		else:
			continue
		cost = level.distance_heuristic(loc, target_loc)
		if best_cost is None or cost < best_cost:
			best_action = action
			best_direction = direction
			best_cost = cost

	if best_action == ACTIONS.MOVE:
		game.creature_move(level, creature, best_direction)
	elif best_action == ACTIONS.SWAP:
		game.creature_swap(level, creature, best_direction)
	else:
		assert False


def move_random(game, level, creature):
	for x in range(len(DIRS.ALL)):
		direction = random.choice(DIRS.ALL)
		if game.creature_move(level, creature, direction):
			return
