from collections import namedtuple
from random import randint


Dice = namedtuple("Dice", ["dices", "highest_side", "addition"])


def dice_roll(dices, highest_side, addition):
    return sum(randint(0, highest_side) for _ in range(dices)) + addition


def dice_str(dices, highest_side, addition):
    min_roll = addition
    max_roll = dices * highest_side + addition
    if min_roll < 0:
        min_roll = "({})".format(min_roll)
    if max_roll < 0:
        max_roll = "({}".format(max_roll)
    return "{}-{}".format(min_roll, max_roll)
