from __future__ import absolute_import, division, print_function, unicode_literals

from const.slots import HEAD, BODY, FEET, RIGHT_HAND
from const.stats import *
from creature import Creature


class AdvancedCreature(Creature):

    def __init__(self, creature_file):
        self.equipment_slots = {}
        self.equipment_slots[RIGHT_HAND] = None
        self.equipment_slots[HEAD] = None
        self.equipment_slots[BODY] = None
        self.equipment_slots[FEET] = None
        self.inventory = []
        self.last_action_energy = 0

        super(self.__class__, self).__init__(creature_file)

    def get_damage_info(self):
        if self.equipment_slots[RIGHT_HAND] is not None:
            dice, sides, addition = self.equipment_slots[RIGHT_HAND].get_damage()
            addition += self.dmg_bonus
        else:
            dice = self.unarmed_dice
            sides = self.unarmed_sides
            addition = self.dmg_bonus
        return dice, sides, addition

    def get_item(self, slot):
        return self.equipment_slots[slot]

    def get_item_stats(self, stat):
        return sum(item.get_stat_bonus(stat) for item in self.equipment_slots.values() if item is not None)

    def update_energy(self, amount):
        super(self.__class__, self).update_energy(amount)
        self.last_action_energy = amount

    def update_energy_action(self, action):
        self.last_action_energy = super(self.__class__, self).update_energy_action(action)

    def is_idle(self):
        return False

    def equip(self, item, slot):
        self.equipment_slots[slot] = item

    def unequip(self, slot):
        item = self.equipment_slots[slot]
        self.equipment_slots[slot] = None
        return item

    def bag_item(self, item):
        self.inventory.append(item)

    def unbag_item(self, item):
        self.inventory.remove(item)

    def get_inventory_lines(self):
        f = "{1}. {0.name} {0.stats}"
        for i, item in enumerate(self.inventory):
            yield f.format(item, (i + 1) % 10)

    def get_inventory_items(self, slot=None):
        if slot is not None:
            return (item for item in self.inventory if item.fits_to_slot(slot))
        else:
            return self.inventory

    @property
    def st(self):
        return super(self.__class__, self).st + self.get_item_stats(ST)

    @property
    def dx(self):
        return super(self.__class__, self).dx + self.get_item_stats(DX)

    @property
    def to(self):
        return super(self.__class__, self).to + self.get_item_stats(TO)

    @property
    def le(self):
        return super(self.__class__, self).le + self.get_item_stats(LE)

    @property
    def pe(self):
        return super(self.__class__, self).pe + self.get_item_stats(PE)

    @property
    def sight(self):
        return super(self.__class__, self).sight + self.get_item_stats(SIGHT)

    @property
    def max_hp(self):
        return super(self.__class__, self).max_hp + self.get_item_stats(MAX_HP)

    @property
    def dmg_bonus(self):
        return super(self.__class__, self).dmg_bonus + self.get_item_stats(DMG_BONUS)

    @property
    def pv(self):
        return super(self.__class__, self).pv + self.get_item_stats(PV)

    @property
    def ar(self):
        return super(self.__class__, self).ar + self.get_item_stats(AR)

    @property
    def dr(self):
        return super(self.__class__, self).dr + self.get_item_stats(DR)

    @property
    def unarmed_dice(self):
        return super(self.__class__, self).unarmed_dice + self.get_item_stats(UNARMED_DICE)

    @property
    def unarmed_sides(self):
        return super(self.__class__, self).unarmed_sides + self.get_item_stats(UNARMED_SIDES)

    @property
    def speed(self):
        return super(self.__class__, self).speed + self.get_item_stats(SPEED)
