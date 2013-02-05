import random
import const.directions as DIRS
import const.creature_actions as ACTIONS
from generic_algorithms import resize_vector_to_len, get_vector, add_vector


def act_alert(game, creature, alert_coord):
    level = creature.level
    if level.creature_has_sight(creature, alert_coord):
        # passive actions
        if hasattr(creature, "target_coord") and creature.target_coord != alert_coord:
            creature.chase_vector = get_vector(creature.target_coord, alert_coord)
        creature.target_coord = alert_coord

        # actions
        if creature.can_act():
            if level.creature_can_reach(creature, alert_coord):
                game.creature_attack(creature, get_vector(creature.coord, alert_coord))
            else:
                move_towards(game, creature, alert_coord)

    elif creature.can_act():
        # chasing and already at the target square
        if hasattr(creature, "target_coord") and creature.target_coord == creature.coord:
            # and has a chase vector to pursue
            if hasattr(creature, "chase_vector"):
                # resize the chase vector to the creatures sight so the creature can just go there
                chase_vector = resize_vector_to_len(creature.chase_vector, creature.sight)
                # calculate a new target square
                overarching_target = add_vector(creature.coord, chase_vector)
                target_coord = level.get_last_pathable_coord(creature.coord, overarching_target)
                if creature.coord != target_coord:
                    creature.target_coord = target_coord
                    creature.chase_vector = chase_vector
                # hit a wall, end chase
                else:
                    del creature.target_coord
                    del creature.chase_vector
        # actions
        if hasattr(creature, "target_coord"):
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
