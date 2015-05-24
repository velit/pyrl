from __future__ import absolute_import, division, print_function, unicode_literals

from enum import Enum


class Action(Enum):
    Move = 1
    Attack = 2
    Swap = 3

    @property
    def cost(self):
        return action_cost[self]


action_cost = {
    Action.Move: 1000,
    Action.Attack: 1000,
    Action.Swap: 1000,
}
