from __future__ import absolute_import, division, print_function, unicode_literals

import random

from creature.actions import Action
from enums.directions import Dir
from generic_algorithms import resize_vector_to_len, get_vector, add_vector


class AI(object):

    def __init__(self):
        self.ai_state = {}

    def act_alert(self, game, creature, alert_coord):
        level = creature.level
        if creature in self.ai_state:
            chase_coord, chase_vector = self.ai_state[creature]
        else:
            chase_coord, chase_vector = None, None

        if level.creature_has_sight(creature, alert_coord):
            # passive actions
            if chase_coord is not None and chase_coord != alert_coord:
                chase_vector = get_vector(chase_coord, alert_coord)
            chase_coord = alert_coord

            # actions
            if creature.can_act():
                if level.creature_can_reach(creature, alert_coord):
                    game.creature_attack(creature, get_vector(creature.coord, alert_coord))
                else:
                    self.move_towards(game, creature, alert_coord)

        elif creature.can_act():
            # chasing and already at the target square and has a chase vector to pursue
            if chase_coord == creature.coord:
                if chase_vector is not None:
                    # resize the chase vector to the creatures sight so the creature can just go there
                    chase_vector = resize_vector_to_len(chase_vector, creature.sight)

                    # calculate a new target square
                    overarching_target = add_vector(creature.coord, chase_vector)
                    chase_coord = level.get_last_pathable_coord(creature.coord, overarching_target)

                    # if an obstacle is hit end chase
                    if creature.coord == chase_coord:
                        chase_coord, chase_vector = None, None
                else:
                    chase_coord = None

            # actions
            if chase_coord is not None:
                self.move_towards(game, creature, chase_coord)
            else:
                self.move_random(game, creature)

        if chase_coord is not None or chase_vector is not None:
            self.ai_state[creature] = chase_coord, chase_vector
        else:
            self.remove_creature_state(creature)

    def move_towards(self, game, creature, target_coord):
        level = creature.level
        best_action = Action.Move
        best_direction = Dir.Stay
        best_cost = None
        for direction in Dir.AllPlusStay:
            coord = add_vector(creature.coord, direction)
            if level.is_passable(coord):
                action = Action.Move
            elif level.has_creature(coord) and self.willing_to_swap(level.get_creature(coord), creature):
                action = Action.Swap
            else:
                continue

            cost = level.distance_heuristic(coord, target_coord)
            if best_cost is None or cost < best_cost:
                best_action = action
                best_direction = direction
                best_cost = cost

        if best_action == Action.Move:
            game.creature_move(creature, best_direction)
        elif best_action == Action.Swap:
            game.creature_swap(creature, best_direction)
        else:
            assert False

    def move_random(self, game, creature):
        valid_dirs = [direction for direction in Dir.All if creature.level.creature_can_move(creature, direction)]
        if random.random() < 0.8 and len(valid_dirs) > 0:
            game.creature_move(creature, random.choice(valid_dirs))
        else:
            game.creature_move(creature, Dir.Stay)

    def willing_to_swap(self, creature, target_creature, player=None):
        return target_creature is not player and creature not in self.ai_state

    def remove_creature_state(self, creature):
        if creature in self.ai_state:
            del self.ai_state[creature]
