from __future__ import absolute_import, division, print_function, unicode_literals

from enum import Enum


class Action(Enum):
    Generic = 1
    Move = 2
    Attack = 3
    Swap = 4
    Exchange_Items = 4
    Spawn = 5

    @property
    def cost(self):
        return action_cost[self]


action_cost = {
    Action.Generic: 1000,
    Action.Move: 1000,
    Action.Attack: 1000,
    Action.Swap: 1000,
    Action.Exchange_Items: 1000,
    Action.Spawn: 1000,
}
