from __future__ import annotations

from collections import namedtuple
from typing import Literal

from pyrl.binds import Binds
from pyrl.config.config import Config
from pyrl.constants.coord import Coord
from pyrl.constants.direction import Direction, Dir
from pyrl.creature.actions import Action, IllegalContextException
from pyrl.game_actions import GameActionProperties, GameActions
from pyrl.generic_algorithms import (get_vector, clockwise, anticlockwise, reverse_vector,
                                     clockwise_45, anticlockwise_45)

WalkType = namedtuple("WalkType", "left_passable, right_passable")
WalkModeState = namedtuple("WalkModeState", "direction, walk_type, next_walk_time, show_msg_time")

WALK_IN_PLACE = WalkType(None,  None)
CORRIDOR      = WalkType(False, False)
LEFT          = WalkType(True,  False)
RIGHT         = WalkType(False, True)
OPEN          = WalkType(True,  True)

INTERRUPT_MSG_TIME = 1

class WalkMode(GameActionProperties, object):

    def __init__(self, game_actions: GameActions):
        self.actions = game_actions
        self.state: WalkModeState = None

    def is_walk_mode_active(self) -> bool:
        return self.state is not None

    def init_walk_mode(self, direction: Direction | None = None) -> Literal[Action.Move, Action.No_Action]:
        if self._any_creatures_visible():
            raise IllegalContextException("Not while there are creatures in the vicinity.")

        if direction is None:
            query = f"Specify walking direction, {Binds.Cancel.key} to cancel."
            key_seq = Binds.Directions + Binds.Cancel
            key = self.io.get_key(query, keys=key_seq)
            if key in Binds.Cancel:
                return Action.No_Action
            direction = Binds.get_direction(key)

        feedback = self.actions.move(direction)
        walk_type = self._get_initial_walk_type(direction)
        if not walk_type:
            return feedback

        self.state = WalkModeState(direction, walk_type,
                                   self.io.get_future_time(Config.animation_period),
                                   self.io.get_future_time(INTERRUPT_MSG_TIME))
        return feedback

    def continue_walk(self) -> Literal[Action.Move, Action.No_Action]:
        next_direction = self._next_direction()

        if next_direction is not None:
            feedback = self.actions.move(next_direction)
            next_walk_time = self.io.get_future_time(Config.animation_period)
            self.state = WalkModeState(next_direction, self.state.walk_type, next_walk_time, self.state.show_msg_time)
            return feedback

        self.state = None
        return Action.No_Action

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

    def _calculate_next_direction(self, old_direction: Direction, walk_type: WalkType) -> Direction | None:
        if walk_type == WALK_IN_PLACE:
            return old_direction
        elif walk_type == CORRIDOR:
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
            sides = self._get_side_passables(old_direction)
            if forward and sides == walk_type:
                return old_direction
        return None

    def _get_corridor_candidate_dirs(self, direction: Direction) \
            -> tuple[set[Direction], set[Direction], set[Direction]]:
        reverse = reverse_vector(direction)
        back_sides = {anticlockwise_45(reverse), clockwise_45(reverse)}
        candidate_dirs = set(self.level.get_passable_neighbors(self.creature.coord)) - {reverse}
        candidate_forward_dirs = candidate_dirs - back_sides
        candidate_orthogonal_dirs = candidate_dirs & set(Dir.Orthogonals)
        ignored_dirs = candidate_dirs & back_sides
        return candidate_forward_dirs, candidate_orthogonal_dirs, ignored_dirs

    def _passable(self, direction: Direction) -> bool:
        return self.actions.can_move(direction)

    def _get_neighbor_passables(self, direction: Direction) -> tuple[bool, bool, bool, bool, bool, bool, bool]:
        upper_left_dir = anticlockwise_45(direction)
        upper_right_dir = clockwise_45(direction)

        forward = self._passable(direction)
        up_left = self._passable(upper_left_dir)
        up_right = self._passable(upper_right_dir)
        left = self._passable(anticlockwise(direction))
        right = self._passable(clockwise(direction))
        down_left = self._passable(anticlockwise(upper_left_dir))
        down_right = self._passable(clockwise(upper_right_dir))
        return forward, up_left, up_right, left, right, down_left, down_right

    def _get_initial_walk_type(self, direction: Direction) -> WalkType | None:
        if direction == Dir.Stay:
            return WALK_IN_PLACE

        walk_type = self._get_side_passables(direction)
        forward, up_left, up_right, left, right, down_left, down_right = \
            self._get_neighbor_passables(direction)
        if (forward and left and not up_left and not down_left
                or forward and right and not up_right and not down_right
                or not forward and left and down_left
                or not forward and right and down_right):
            return None
        if not forward:
            walk_type = CORRIDOR
        return walk_type

    def _get_side_passables(self, direction: Coord) -> WalkType:
        if direction in Dir.Orthogonals:
            left = self._passable(anticlockwise(direction))
            right = self._passable(clockwise(direction))
        elif direction in Dir.Diagonals:
            left = self._passable(anticlockwise_45(direction))
            right = self._passable(clockwise_45(direction))
        else:
            raise Exception(f"Not a valid {direction=}")
        return WalkType(left, right)

    def _any_creatures_visible(self) -> int:
        return len(self.actions.get_coords_of_creatures_in_vision())
