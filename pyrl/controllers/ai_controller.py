from __future__ import annotations

import random

from pyrl.engine.actions.action import Action
from pyrl.engine.actions.action_feedback import ActionFeedback
from pyrl.engine.actions.action_interface import ActionInterface
from pyrl.engine.behaviour.coordinates import resize_vector_to_len, add_vector, get_vector
from pyrl.engine.creature.creature import Creature
from pyrl.engine.creature.stats import Stat
from pyrl.engine.structures.helper_mixins import CreatureActionsMixin
from pyrl.engine.types.directions import Dir, Coord

AiState = dict[Creature, tuple[Coord | None, Coord | None]]

class AIController(CreatureActionsMixin):

    def __init__(self, ai_state: AiState, actions: ActionInterface) -> None:
        self.ai_state = ai_state
        self.actions = actions

    def act(self, alert_coord: Coord) -> Action:
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
            direction = self.actions.can_reach(alert_coord)
            if direction:
                feedback = self.actions.attack(direction)
            else:
                feedback = self._move_towards(alert_coord)
        else:
            # chasing and already at the target square and has a chase vector to pursue
            if chase_coord == self.coord:
                if chase_vector is not None:
                    # resize the chase vector to the creatures sight so the self.creature can just go there
                    chase_vector = resize_vector_to_len(chase_vector, self.creature[Stat.SIGHT])

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

        return feedback.action

    def _move_towards(self, target_coord: Coord) -> ActionFeedback:
        best_action = Action.Move
        best_direction = Dir.Stay
        best_cost: int | None = None
        for direction in Dir.AllPlusStay:
            coord = add_vector(self.coord, direction)
            if self.level.is_passable(coord):
                action = Action.Move
            elif coord in self.level.creatures and self.actions.willing_to_swap(self.level.creatures[coord]):
                action = Action.Swap
            else:
                continue

            cost = self.level.distance(coord, target_coord)
            if best_cost is None or cost < best_cost:
                best_action = action
                best_direction = direction
                best_cost = cost

        if best_action == Action.Move:
            return self.actions.move(best_direction)
        elif best_action == Action.Swap:
            return self.actions.swap(best_direction)
        else:
            assert False, f"AI state bug. Best action was: {best_action}"

    def _move_random(self) -> ActionFeedback:
        valid_dirs = [direction for direction in Dir.All if self.actions.can_move(direction)]
        if random.random() < 0.8 and len(valid_dirs) > 0:
            return self.actions.move(random.choice(valid_dirs))
        else:
            return self.actions.move(Dir.Stay)

    def remove_creature_state(self, creature: Creature) -> None:
        if creature in self.ai_state:
            del self.ai_state[creature]
