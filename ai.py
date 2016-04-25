from __future__ import absolute_import, division, print_function, unicode_literals

import random

from game_actions import Action, ActionError, GameActionsProperties
from enums.directions import Dir
from generic_algorithms import resize_vector_to_len, get_vector, add_vector


class AI(GameActionsProperties, object):

    def __init__(self):
        self.ai_state = {}

    def act(self, game_actions, alert_coord):
        self.actions = game_actions

        if self.creature in self.ai_state:
            chase_coord, chase_vector = self.ai_state[self.creature]
        else:
            chase_coord, chase_vector = None, None

        if self.actions.target_in_sight(alert_coord):
            # passive actions
            if chase_coord is not None and chase_coord != alert_coord:
                chase_vector = get_vector(chase_coord, alert_coord)
            chase_coord = alert_coord

            # actions
            if self.actions.can_reach(alert_coord):
                feedback = self.actions.attack(get_vector(self.coord, alert_coord))
            else:
                feedback = self._move_towards(alert_coord)

        else:
            # chasing and already at the target square and has a chase vector to pursue
            if chase_coord == self.coord:
                if chase_vector is not None:
                    # resize the chase vector to the creatures sight so the self.creature can just go there
                    chase_vector = resize_vector_to_len(chase_vector, self.creature.sight)

                    # calculate a new target square
                    overarching_target = add_vector(self.coord, chase_vector)
                    chase_coord = self.level.get_last_pathable_coord(self.coord, overarching_target)

                    # if an obstacle is hit end chase
                    if self.coord == chase_coord:
                        chase_coord, chase_vector = None, None
                else:
                    chase_coord = None

            # actions
            if chase_coord is not None:
                feedback = self._move_towards(chase_coord)
            else:
                feedback = self._move_random()

        if chase_coord is not None or chase_vector is not None:
            self.ai_state[self.creature] = chase_coord, chase_vector
        else:
            self.remove_creature_state(self.creature)

        assert feedback.type not in ActionError, \
            "AI state bug. Got error from game: {} {}".format(feedback.type, feedback.params)

    def _move_towards(self, target_coord):
        best_action = Action.Move
        best_direction = Dir.Stay
        best_cost = None
        for direction in Dir.AllPlusStay:
            coord = add_vector(self.coord, direction)
            if self.level.is_passable(coord):
                action = Action.Move
            elif coord in self.level.creatures and self.actions.willing_to_swap(self.level.creatures[coord]):
                action = Action.Swap
            else:
                continue

            cost = self.level.distance_heuristic(coord, target_coord)
            if best_cost is None or cost < best_cost:
                best_action = action
                best_direction = direction
                best_cost = cost

        if best_action == Action.Move:
            return self.actions.move(best_direction)
        elif best_action == Action.Swap:
            return self.actions.swap(best_direction)
        else:
            assert False, "AI state bug. Best action was: {}".format(best_action)

    def _move_random(self):
        valid_dirs = [direction for direction in Dir.All if self.actions.can_move(direction)]
        if random.random() < 0.8 and len(valid_dirs) > 0:
            return self.actions.move(random.choice(valid_dirs))
        else:
            return self.actions.move(Dir.Stay)

    def remove_creature_state(self, creature):
        if creature in self.ai_state:
            del self.ai_state[creature]
