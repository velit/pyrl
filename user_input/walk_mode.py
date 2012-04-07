import const.game as GAME
import mappings as MAPPING
import const.directions as DIR
from generic_algorithms import add_vector, get_vector, clockwise, anticlockwise, reverse_vector
from generic_algorithms import clockwise_45, anticlockwise_45
from main import io

CORRIDOR = (False, False)
LEFT = (True, False)
RIGHT = (False, True)
OPEN = (True, True)

INTERRUPT_MSG_TIME = 5

def walk_mode_init(game, creature, userinput, direction=None):
	if _any_creatures_visible(game, creature):
		io.msg("Not while there are creatures in the vicinity.")
	if direction is None:
		key_set = MAPPING.DIRECTIONS.viewkeys() | MAPPING.GROUP_CANCEL
		key = io.ask("Specify walking direction, {} to abort".format(MAPPING.CANCEL), key_set)
		if key in MAPPING.DIRECTIONS:
			direction = MAPPING.DIRECTIONS[key]

	if direction is not None:
		walk_mode_data = _walk_mode_init(game, creature, direction)
		if walk_mode_data is not None:
			userinput.walk_mode_data = walk_mode_data

def _walk_mode_init(game, creature, direction):
	if game.creature_move(creature, direction):
		walk_type = _get_walk_type(creature, direction)
		n = _get_neighbor_passables(creature, direction)
		forward, upper_left, upper_right, left, right, lower_left, lower_right = n
		if forward:
			if left and not upper_left and not lower_left \
			or right and not upper_right and not lower_right:
				return
		else:
			if left and lower_left \
			or right and lower_right:
				return
			walk_type = CORRIDOR

		return direction, walk_type, io.get_future_time(GAME.ANIMATION_DELAY), io.get_future_time(INTERRUPT_MSG_TIME)

def walk_mode(game, creature, userinput):
	if not _any_creatures_visible(game, creature):
		direction, old_walk_type, timestamp, msg_time = userinput.walk_mode_data
		if old_walk_type == CORRIDOR:
			result = _corridor_walk_type(game, creature, direction)
		else:
			result = _normal_walk_type(game, creature, direction, old_walk_type)

		if result is not None:
			new_direction, new_walk_type = result
			if msg_time < io.get_current_time():
				message = "Press {} to interrupt walk mode".format(MAPPING.WALK_MODE)
			else:
				message = ""
			key = io.ask_until_timestamp(message, timestamp, MAPPING.GROUP_CANCEL | {MAPPING.WALK_MODE})
			if key not in MAPPING.GROUP_CANCEL | {MAPPING.WALK_MODE}:
				if game.creature_move(creature, new_direction):
					walk_delay = io.get_future_time(GAME.ANIMATION_DELAY)
					userinput.walk_mode_data = new_direction, new_walk_type, walk_delay, msg_time
					return True

	userinput.walk_mode_data = None
	return False

def _corridor_walk_type(game, creature, origin_direction):
	forward_dirs, orthogonal_dirs, ignored_dirs = _get_corridor_candidate_dirs(creature, origin_direction)
	if len(forward_dirs) == 1:
		direction = forward_dirs.pop()
		#if clockwise_45(direction) not in ignored_dirs and anticlockwise_45(direction) not in ignored_dirs:
		return direction, CORRIDOR
	elif len(forward_dirs) > 1 and len(orthogonal_dirs) == 1:
		direction = orthogonal_dirs.pop()
		if all(get_vector(direction, other) in DIR.ALL for other in forward_dirs):
			#if clockwise_45(direction) not in ignored_dirs and anticlockwise_45(direction) not in ignored_dirs:
			return direction, CORRIDOR

def _get_corridor_candidate_dirs(creature, direction):
	reverse = reverse_vector(direction)
	back_sides = {anticlockwise_45(reverse), clockwise_45(reverse)}
	candidate_dirs = set(creature.level.get_tile_passable_neighbors(creature.coord)) - {reverse}
	candidate_forward_dirs = candidate_dirs - back_sides
	candidate_orthogonal_dirs = candidate_dirs & set(DIR.ORTHOGONALS)
	ignored_dirs = candidate_dirs & back_sides
	return candidate_forward_dirs, candidate_orthogonal_dirs, ignored_dirs

def _normal_walk_type(game, creature, direction, old_walk_type):
	forward = _passable(creature, direction)
	new_walk_type = _get_walk_type(creature, direction)
	if forward and old_walk_type == new_walk_type:
		return direction, new_walk_type

def _passable(creature, direction):
	return creature.level.is_passable(add_vector(creature.coord, direction))

def _get_neighbor_passables(creature, direction):
		upper_left_dir = anticlockwise_45(direction)
		upper_right_dir = clockwise_45(direction)
		forward = _passable(creature, direction)
		left = _passable(creature, anticlockwise(direction))
		right = _passable(creature, clockwise(direction))
		upper_left = _passable(creature, upper_left_dir)
		lower_left = _passable(creature, anticlockwise(upper_left_dir))
		upper_right = _passable(creature, upper_right_dir)
		lower_right = _passable(creature, clockwise(upper_right_dir))
		return forward, upper_left, upper_right, left, right, lower_left, lower_right

def _get_walk_type(creature, direction):
	if direction in DIR.ORTHOGONALS:
		left = _passable(creature, anticlockwise(direction))
		right =	_passable(creature, clockwise(direction))
	elif direction in DIR.DIAGONALS:
		left = _passable(creature, anticlockwise_45(direction))
		right =	_passable(creature, clockwise_45(direction))
	else:
		raise Exception("Not a valid direction {0}".format(direction))
	return (left, right)

def _any_creatures_visible(game, creature):
	return any(creature.level.has_creature(coord) for coord in game.current_vision if coord != creature.coord)
