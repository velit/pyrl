import random
import const.directions as DIRS
import const.creature_actions as ACTIONS
from generic_algorithms import resize_vector_to_len, get_vector, add_vector


def act_alert(game, creature, alert_coord):
	level = creature.level
	# creature seeing actions
	if level.creature_has_sight(creature, alert_coord):
		if creature.target_coord is not None and creature.target_coord != alert_coord:
			creature.chase_vector = get_vector(creature.target_coord, alert_coord)
		creature.target_coord = alert_coord

		if creature.can_act():
			if level.creature_can_reach(creature, alert_coord):
				game.creature_attack(creature, get_vector(creature.coord, creature.target_coord))
			else:
				move_towards(game, creature, alert_coord)

	# creature actions
	elif creature.can_act():
		# chasing
		if creature.target_coord == creature.coord:
			creature.target_coord = None
			if creature.chase_vector is not None:
				creature.chase_vector = resize_vector_to_len(creature.chase_vector, creature.sight)
				overarching_target = add_vector(creature.coord, creature.chase_vector)
				target_coord = level.get_last_pathable_coord(creature.coord, overarching_target)
				if creature.coord != target_coord:
					creature.target_coord = target_coord
				else:
					creature.chase_vector = None

		if creature.target_coord is not None:
			move_towards(game, creature, creature.target_coord)
		else:
			move_random(game, creature)


def move_towards(game, creature, target_coord):
	level = creature.level
	best_action = ACTIONS.MOVE
	best_direction = DIRS.STOP
	best_cost = None
	for direction in DIRS.ALL:
		coord = add_vector(creature.coord, direction)
		if level.is_passable(coord):
			action = ACTIONS.MOVE
		elif level.creature_is_swappable(coord):
			action = ACTIONS.SWAP
		else:
			continue
		cost = level.distance_heuristic(coord, target_coord)
		if best_cost is None or cost < best_cost:
			best_action = action
			best_direction = direction
			best_cost = cost

	if best_action == ACTIONS.MOVE:
		game.creature_move(creature, best_direction)
	elif best_action == ACTIONS.SWAP:
		game.creature_swap(creature, best_direction)
	else:
		assert False


def move_random(game, creature):
	for x in xrange(len(DIRS.ALL)):
		direction = random.choice(DIRS.ALL)
		if game.creature_move(creature, direction):
			return
