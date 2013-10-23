from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from random import randrange


class Dice(object):
    def __init__(self, dices=1, sides=6, addition=0):
        self.dices = dices
        self.sides = sides
        self.addition = addition

    def roll(self):
        return sum(randrange(self.sides) + 1 for die in range(self.dices)) + self.addition

    def get_values(self):
        return self.dices, self.sides, self.addition

    def __str__(self):
        if self.addition != 0:
            return "{0.dices}D{0.sides}{0.addition:+}".format(self)
        else:
            return "{0.dices}D{0.sides}".format(self)


def dice_roll(dices=1, sides=6, addition=0):
    return sum(randrange(sides) + 1 for die in range(dices)) + addition
