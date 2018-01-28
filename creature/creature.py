from copy import deepcopy
from decimal import Decimal
from fractions import Fraction

from generic_algorithms import resize_range
from creature.stats import ensure_stats
from dice import Dice


@ensure_stats
class Creature(object):

    def __init__(self, name, char, danger_level=0, spawn_weight_class=1, coord=None):
        self.name = name
        self.char = char
        self.danger_level = danger_level
        self.spawn_weight_class = spawn_weight_class
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
        return f"Creature(name={self.name})"

    def copy(self):
        return deepcopy(self)

    def spawn_weight(self, external_danger_level):
        return round(1000 * self.danger_level_spawn_mult(external_danger_level) *
                     self.spawn_weight_class)

    def danger_level_spawn_mult(self, external_danger_level):
        diff = Decimal(external_danger_level - self.danger_level)

        speciation_range = range(-5, 1)
        extant_range = range(1, 10)
        extinction_range = range(10, 21)
        if diff in speciation_range:
            # 0 0.008 0.064 0.216 0.512 1
            diff_weight = pow(resize_range(diff, speciation_range), 3)
        elif diff in extant_range:
            diff_weight = Decimal(1)
        elif diff in extinction_range:
            # 1, 0.999, 0.992, 0.973, 0.936, 0.875, 0.784, 0.657, 0.488, 0.271, 0
            diff_weight = 1 - pow(resize_range(diff, extinction_range), 3)
        else:
            diff_weight = Decimal(0)
        return diff_weight

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
