from __future__ import absolute_import, division, print_function, unicode_literals

import const.game as GAME
from .actions import Action
from .stats import ensure_stats


@ensure_stats
class Creature(object):

    def __init__(self, creature_file):
        self.name = creature_file.name
        self.char = creature_file.char

        self.level = None
        self.coord = None
        self.energy = 0

        self.base_strength     = 10
        self.base_dexterity    = 10
        self.base_endurance    = 10
        self.base_intelligence = 10
        self.base_perception   = 10

        self.hp = self.max_hp

    def get_damage_info(self):
        dice = self.unarmed_dices
        sides = self.unarmed_sides
        addition = self.damage
        return dice, sides, addition

    def receive_damage(self, amount):
        if amount > 0:
            self.hp -= amount

    def is_dead(self):
        return self.hp <= 0

    def recover_energy(self):
        self.energy += self.speed
        if self.energy > 0:
            self.energy = 0

    def can_act(self):
        return self.energy >= 0

    def update_energy(self, amount):
        self.energy -= amount

    def update_energy_action(self, action):
        if action == Action.Attack:
            amount = self.attack_energy_cost
        else:
            assert False
        self.energy -= amount
        return amount

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
        return int((2 * self.perception) ** 0.5 + 1)

    @property
    def max_hp(self):
        return self.endurance + self.strength // 2

    @property
    def armor(self):
        return self.endurance // 10

    @property
    def attack_rating(self):
        return self.dexterity + self.perception // 2

    @property
    def defense_rating(self):
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
    def attack_energy_cost(self):
        return GAME.ATTACK_COST
