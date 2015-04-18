from __future__ import absolute_import, division, print_function, unicode_literals

from enum import Enum


class Action(Enum):
    Move = 1
    Attack = 2
    Swap = 3


class Multiplier(object):
    Orthogonal = 1
    Diagonal = 2 ** 0.5
    Stay = 1


class Cost(object):
    Move = 1000
    Attack = 1000
    Swap = 1000
