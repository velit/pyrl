import const.game as GAME
import mappings as MAPPING
import const.directions as DIR
from generic_algorithms import add_vector, get_vector, clockwise, anticlockwise, reverse_vector
from generic_algorithms import clockwise_45, anticlockwise_45
from main import io

CORRIDOR = (False, False)
LEFT = (False, True)
RIGHT = (True, False)
OPEN = (True, True)

INTERRUPT_MSG_TIME = 5

def walk_mode_init(game, creature, userinput):
	if _any_creatures_visible(game, creature):
		io.msg("Not while there are creatures in the vicinity.")
	else:
		key_set = MAPPING.DIRECTIONS.viewkeys() | MAPPING.GROUP_CANCEL
		key = io.ask("Specify walking direction, {} to abort".format(MAPPING.CANCEL), key_set)
		if key in MAPPING.DIRECTIONS:
			walk_mode_data = _walk_mode_init(game, creature, MAPPING.DIRECTIONS[key])
			if walk_mode_data is not None:
				userinput.walk_mode_data = walk_mode_data
				return True
	return False

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

def _walk_mode_init(game, creature, direction):
	if game.creature_move(creature, direction):
		forward, walk_type = _get_walk_type_data(creature, direction)
		if not forward:
			walk_type = CORRIDOR
		return (direction, walk_type, io.get_future_time(GAME.ANIMATION_DELAY), io.get_future_time(INTERRUPT_MSG_TIME))

def _corridor_walk_type(game, creature, direction):
	valid_forward_dirs = _valid_forward_dirs(creature, direction)
	if len(valid_forward_dirs) == 1:
		return valid_forward_dirs[0], CORRIDOR
	elif len(valid_forward_dirs) == 2:
		d1, d2 = valid_forward_dirs
		if get_vector(d1, d2) in DIR.ALL:
			if d1 in DIR.ORTHOGONAL and d2 in DIR.DIAGONAL:
				return d1, CORRIDOR
			elif d2 in DIR.ORTHOGONAL and d1 in DIR.DIAGONAL:
				return d2, CORRIDOR

def _normal_walk_type(game, creature, direction, old_walk_type):
	forward, new_walk_type = _get_walk_type_data(creature, direction)
	if forward and old_walk_type == new_walk_type:
		return direction, new_walk_type

def _passable(creature, direction):
	return creature.level.is_passable(add_vector(creature.coord, direction))

def _get_walk_type_data(creature, direction):
	forward = _passable(creature, direction)
	if direction in DIR.ORTHOGONAL:
		left = _passable(creature, anticlockwise(direction))
		right =	_passable(creature, clockwise(direction))
	elif direction in DIR.DIAGONAL:
		left = _passable(creature, anticlockwise_45(direction))
		right =	_passable(creature, clockwise_45(direction))
	else:
		raise Exception("Not a valid direction {0}".format(direction))
	return forward, (left, right)

def _any_creatures_visible(game, creature):
	return any(creature.level.has_creature(coord) for coord in game.current_vision if coord != creature.coord)

def _valid_forward_dirs(creature, direction):
	reverse = reverse_vector(direction)
	return tuple(set(creature.level.get_tile_passable_neighbors(creature.coord)) -
			{DIR.STOP, reverse, anticlockwise_45(reverse), clockwise_45(reverse)})
