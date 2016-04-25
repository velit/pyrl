from __future__ import absolute_import, division, print_function, unicode_literals

from collections import namedtuple
from config.bindings import Bind
from config.game import GameConf
from enums.directions import Dir
from enums.keys import Key
from game_actions import Action, ActionError, GameActionsProperties
from generic_algorithms import (get_vector, clockwise, anticlockwise, reverse_vector,
                                clockwise_45, anticlockwise_45)


WalkType = namedtuple("WalkType", "left_passable, right_passable")
WalkModeState = namedtuple("WalkModeState", "direction, walk_type, next_walk_time, show_msg_time")


WALK_IN_PLACE = WalkType(None,  None)
CORRIDOR      = WalkType(False, False)
LEFT          = WalkType(True,  False)
RIGHT         = WalkType(False, True)
OPEN          = WalkType(True,  True)

INTERRUPT_MSG_TIME = 1


class WalkMode(GameActionsProperties, object):

    def __init__(self, game_actions):
        self.actions = game_actions
        self.state = None

    def is_walk_mode_active(self):
        return self.state is not None

    def init_walk_mode(self, direction=None):
        if self._any_creatures_visible():
            self.io.msg("Not while there are creatures in the vicinity.")
            return

        if direction is None:
            user_query = "Specify walking direction, {} to cancel.".format(Bind.Cancel.key)
            key_seq = tuple(Bind.action_direction) + Bind.Cancel
            key = self.io.ask(user_query, key_seq)
            if key in Bind.Cancel:
                return
            direction = Bind.action_direction[key]

        feedback = self.actions.move(direction)
        if feedback.type in ActionError:
            return feedback

        walk_type = self._get_initial_walk_type(direction)
        if not walk_type:
            return feedback

        self.state = WalkModeState(direction, walk_type,
                                   self.io.get_future_time(GameConf.animation_period),
                                   self.io.get_future_time(INTERRUPT_MSG_TIME))
        return feedback

    def continue_walk(self):
        if self._any_creatures_visible():
            self.state = None
            return

        if self.state.walk_type == WALK_IN_PLACE:
            result = self.state.direction, self.state.walk_type
        elif self.state.walk_type == CORRIDOR:
            result = self._corridor_walk_type(self.state.direction)
        else:
            result = self._normal_walk_type(self.state.direction, self.state.walk_type)

        if result is None:
            self.state = None
            return

        new_direction, new_walk_type = result

        msg = ""
        if self.state.show_msg_time < self.io.get_current_time():
            msg = "Press {} or {} to interrupt walk mode.".format(Bind.Walk_Mode.key, Bind.Cancel.key)
        key_seq = Bind.Walk_Mode + Bind.Cancel
        key = self.io.selective_ask_until_timestamp(msg, self.state.next_walk_time, key_seq)
        if key != Key.NO_INPUT:
            self.state = None
            return

        feedback = self.actions.move(new_direction)
        assert feedback.type == Action.Move, \
            "Bug in walk_mode. Move failed: {} {}".format(feedback.type, feedback.params)

        next_walk_time = self.io.get_future_time(GameConf.animation_period)
        self.state = WalkModeState(new_direction, new_walk_type, next_walk_time,
                                    self.state.show_msg_time)
        return feedback

    def _corridor_walk_type(self, origin_direction):
        forward_dirs, orthogonal_dirs, ignored_dirs = self._get_corridor_candidate_dirs(origin_direction)
        if len(forward_dirs) == 1:
            direction = forward_dirs.pop()
            return direction, CORRIDOR
        elif len(forward_dirs) > 1 and len(orthogonal_dirs) == 1:
            direction = orthogonal_dirs.pop()
            if all(get_vector(direction, other) in Dir.AllPlusStay for other in forward_dirs):
                return direction, CORRIDOR

    def _get_corridor_candidate_dirs(self, direction):
        reverse = reverse_vector(direction)
        back_sides = {anticlockwise_45(reverse), clockwise_45(reverse)}
        candidate_dirs = set(self.level.get_passable_neighbors(self.creature.coord)) - {reverse}
        candidate_forward_dirs = candidate_dirs - back_sides
        candidate_orthogonal_dirs = candidate_dirs & set(Dir.Orthogonals)
        ignored_dirs = candidate_dirs & back_sides
        return candidate_forward_dirs, candidate_orthogonal_dirs, ignored_dirs

    def _normal_walk_type(self, direction, old_walk_type):
        forward = self._passable(direction)
        new_walk_type = self._get_walk_type(direction)
        if forward and old_walk_type == new_walk_type:
            return direction, new_walk_type
        else:
            return None

    def _passable(self, direction):
        return self.actions.can_move(direction)

    def _get_neighbor_passables(self, direction):
            upper_left_dir = anticlockwise_45(direction)
            upper_right_dir = clockwise_45(direction)

            forward = self._passable(direction)
            left = self._passable(anticlockwise(direction))
            right = self._passable(clockwise(direction))
            up_left = self._passable(upper_left_dir)
            down_left = self._passable(anticlockwise(upper_left_dir))
            up_right = self._passable(upper_right_dir)
            down_right = self._passable(clockwise(upper_right_dir))
            return forward, up_left, up_right, left, right, down_left, down_right

    def _get_initial_walk_type(self, direction):
        walk_type = self._get_walk_type(direction)
        if walk_type != WALK_IN_PLACE:
            forward, up_left, up_right, left, right, down_left, down_right = \
                self._get_neighbor_passables(direction)
            if forward and left and not up_left and not down_left:
                return None
            if forward and right and not up_right and not down_right:
                return None
            if not forward and left and down_left:
                return None
            if not forward and right and down_right:
                return None
            if not forward:
                walk_type = CORRIDOR
        return walk_type

    def _get_walk_type(self, direction):
        if direction in Dir.Orthogonals:
            left = self._passable(anticlockwise(direction))
            right = self._passable(clockwise(direction))
        elif direction in Dir.Diagonals:
            left = self._passable(anticlockwise_45(direction))
            right = self._passable(clockwise_45(direction))
        elif direction == Dir.Stay:
            left, right = WALK_IN_PLACE
        else:
            raise Exception("Not a valid direction: {0}".format(direction))
        return WalkType(left, right)

    def _any_creatures_visible(self):
        return len(self.actions.get_coords_of_creatures_in_vision())
