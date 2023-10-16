from __future__ import annotations

from enum import Enum
from typing import NamedTuple

from pyrl.config.binds import Binds
from pyrl.config.config import Config
from pyrl.engine.actions.action_exceptions import IllegalContextException
from pyrl.engine.actions.action_feedback import ActionFeedback, NoActionFeedback
from pyrl.engine.actions.action_interface import ActionInterface
from pyrl.engine.behaviour.coordinates import get_vector, anticlockwise_45, reverse, clockwise_45
from pyrl.engine.structures.helper_mixins import CreatureActionsMixin
from pyrl.engine.enums.directions import Direction, Dir

class Type(Enum):
    Wait          = (None, None)
    Corridor      = (False, False)
    Left          = (True, False)
    Right         = (False, True)
    Open          = (True, True)

class WalkModeState(NamedTuple):
    direction: Direction
    walk_type: Type
    next_walk_time: float
    show_msg_time: float

INTERRUPT_MSG_TIME = 1

class WalkMode(CreatureActionsMixin):

    state: WalkModeState

    def __init__(self, actions: ActionInterface):
        self.actions = actions
        self.active = False

    def init_walk_mode(self, direction: Direction | None = None) -> ActionFeedback:
        if self._any_creatures_visible():
            raise IllegalContextException("Not while there are creatures in the vicinity.")

        if direction is None:
            query = f"Specify walking direction, {Binds.Cancel.key} to cancel."
            key_seq = Binds.Directions + Binds.Cancel
            key = self.io.get_key(query, keys=key_seq)
            if key in Binds.Cancel:
                return NoActionFeedback
            direction = Binds.get_direction(key)

        feedback = self.actions.move(direction)
        walk_type = self._get_initial_walk_type(direction)
        if not walk_type:
            return feedback

        self.active = True
        self.state = WalkModeState(direction, walk_type,
                                   next_walk_time=self.io.get_future_time(Config.animation_period),
                                   show_msg_time=self.io.get_future_time(INTERRUPT_MSG_TIME))
        return feedback

    def continue_walk(self) -> ActionFeedback:
        next_direction = self._next_direction()

        if next_direction is not None:
            feedback = self.actions.move(next_direction)
            next_walk_time = self.io.get_future_time(Config.animation_period)
            self.state = WalkModeState(next_direction, self.state.walk_type, next_walk_time, self.state.show_msg_time)
            return feedback

        self.active = False
        return NoActionFeedback

    def _next_direction(self) -> Direction | None:
        if self._any_creatures_visible():
            return None

        next_direction = self._calculate_next_direction(self.state.direction, self.state.walk_type)

        if next_direction is None:
            return None

        msg = ""
        if self.state.show_msg_time < self.io.get_time():
            msg = f"Press {Binds.Walk_Mode.key} or {Binds.Cancel.key} to interrupt walk mode."
        key_seq = Binds.Walk_Mode + Binds.Cancel
        key = self.io.check_key(msg, keys=key_seq, until=self.state.next_walk_time)

        if key in Binds.Walk_Mode + Binds.Cancel:
            return None

        return next_direction

    def _calculate_next_direction(self, old_direction: Direction, walk_type: Type) -> Direction | None:
        if walk_type == Type.Wait:
            return old_direction
        elif walk_type == Type.Corridor:
            forward_dirs, orthogonal_dirs, ignored_dirs = self._get_corridor_candidate_dirs(old_direction)
            if len(forward_dirs) == 1:
                new_direction = forward_dirs.pop()
                return new_direction
            elif len(forward_dirs) > 1 and len(orthogonal_dirs) == 1:
                new_direction = orthogonal_dirs.pop()
                if all(get_vector(new_direction, other) in Dir.AllPlusStay for other in forward_dirs):
                    return new_direction
        else:
            forward = self._passable(old_direction)
            sides = self._get_type_from_sides(old_direction)
            if forward and sides == walk_type:
                return old_direction
        return None

    def _get_corridor_candidate_dirs(self, direction: Direction) \
            -> tuple[set[Direction], set[Direction], set[Direction]]:
        back = reverse(direction)
        back_sides = {anticlockwise_45(back), clockwise_45(back)}
        candidate_dirs = set(self.level.get_passable_neighbors(self.creature.coord)) - {back}
        candidate_forward_dirs = candidate_dirs - back_sides
        candidate_orthogonal_dirs = candidate_dirs & set(Dir.Orthogonals)
        ignored_dirs = candidate_dirs & back_sides
        return candidate_forward_dirs, candidate_orthogonal_dirs, ignored_dirs

    def _passable(self, direction: Direction) -> bool:
        return self.actions.can_move(direction)

    def _get_neighbor_passables(self, direction: Direction) -> tuple[bool, bool, bool, bool, bool, bool, bool]:
        forward    = self._passable(direction)
        up_right   = self._passable(Dir.clockwise(direction, 1))
        right      = self._passable(Dir.clockwise(direction, 2))
        down_right = self._passable(Dir.clockwise(direction, 3))
        # down     = self._passable(Dir.clockwise(direction, 4))
        down_left  = self._passable(Dir.clockwise(direction, 5))
        left       = self._passable(Dir.clockwise(direction, 6))
        up_left    = self._passable(Dir.clockwise(direction, 7))
        return forward, up_left, up_right, left, right, down_left, down_right

    def _get_initial_walk_type(self, direction: Direction) -> Type | None:
        if direction == Dir.Stay:
            return Type.Wait

        walk_type = self._get_type_from_sides(direction)
        forward, up_left, up_right, left, right, down_left, down_right = \
            self._get_neighbor_passables(direction)
        if (forward and left and not up_left and not down_left
                or forward and right and not up_right and not down_right
                or not forward and left and down_left
                or not forward and right and down_right):
            return None
        if not forward:
            walk_type = Type.Corridor
        return walk_type

    def _get_type_from_sides(self, direction: Direction) -> Type:
        if direction in Dir.Orthogonals:
            turns = 2
        elif direction in Dir.Diagonals:
            turns = 1
        else:
            raise Exception(f"Not a valid {direction=} for side viewing")
        left = self._passable(Dir.counter_clockwise(direction, turns))
        right = self._passable(Dir.clockwise(direction, turns))
        return Type((left, right))

    def _any_creatures_visible(self) -> int:
        return len(self.actions.get_coords_of_creatures_in_vision())
