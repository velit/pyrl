from copy import deepcopy

from creature.stats import ensure_stats
from dice import Dice


@ensure_stats
class Creature(object):

    def __init__(self, name, char, speciation_lvl=0, extinction_lvl=0, coord=None):
        self.name = name
        self.char = char
        self.speciation_lvl = speciation_lvl
        self.extinction_lvl = extinction_lvl
        self.coord = coord

        self.level = None

        self.base_strength     = 10
        self.base_dexterity    = 10
        self.base_endurance    = 10
        self.base_intelligence = 10
        self.base_perception   = 10

        self.hp = self.max_hp

    def get_damage_info(self):
        dice = self.unarmed_dices
        highest_side = self.unarmed_sides
        addition = self.damage
        return Dice(dice, highest_side, addition)

    def receive_damage(self, amount):
        if amount > 0:
            self.hp -= amount

    def is_dead(self):
        return self.hp <= 0

    def action_cost(self, action, multiplier=1):
        return round(action.base_cost * multiplier * self.speed_multiplier)

    def __repr__(self):
        return "Creature(name={})".format(self.name, self.level)

    def copy(self):
        return deepcopy(self)

    @property
    def strength(self):
        return self.base_strength

    @property
    def dexterity(self):
        return self.base_dexterity

    @property
    def intelligence(self):
        return self.base_intelligence

    @property
    def endurance(self):
        return self.base_endurance

    @property
    def perception(self):
        return self.base_perception

    @property
    def sight(self):
        return min(self.perception // 2, int((self.perception * 5) ** 0.5))

    @property
    def max_hp(self):
        return self.endurance + self.strength // 2

    @property
    def armor(self):
        return self.endurance // 10

    @property
    def accuracy(self):
        return self.dexterity + self.perception // 2

    @property
    def defense(self):
        return self.dexterity + self.intelligence // 2

    @property
    def unarmed_dices(self):
        return self.strength // 20 + 1

    @property
    def unarmed_sides(self):
        return self.strength // 3 + self.dexterity // 6

    @property
    def damage(self):
        return self.strength // 5 + self.dexterity // 10

    @property
    def speed(self):
        return 93 + self.dexterity // 2 + self.strength // 5

    @property
    def speed_multiplier(self):
        return 100 / self.speed
