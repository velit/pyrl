from __future__ import absolute_import, division, print_function, unicode_literals

from enum import Enum
from combat import get_melee_attack_cr, get_combat_message
from creature.actions import Action
from generic_algorithms import add_vector, get_vector
from enums.directions import Dir


class ActionError(Enum):
    AlreadyActed        = "Creature already acted."
    IllegalMove         = "Creature can't move there."
    IllegalTeleport     = "Creature can't teleport there."
    SwapTargetResists   = "Creature resists the swap attempt."
    NoSwapTarget        = "There isn't a creature there to swap with."
    PassageLeadsNoWhere = "This passage doesn't seem to lead anywhere."
    NoPassage           = "This location doesn't have a passage."
    PlayerAction        = "Only the player can do this action."


class GameActions(object):

    def __init__(self, game, creature=None):
        self.game = game
        self.action_cost = None
        if creature:
            self.creature = creature

    @property
    def world(self):
        return self.game.world

    @property
    def level(self):
        return self.creature.level

    @property
    def player(self):
        return self.game.world.player

    @property
    def coord(self):
        return self.creature.coord

    @property
    def equipment(self):
        return self.creature.equipment

    @property
    def io(self):
        return self.game.io

    def _clear_action(self, and_associate_creature=None):
        self.action_cost = None
        if and_associate_creature:
            self.creature = and_associate_creature

    def _do_action(self, cost):
        self.action_cost = cost

    def already_acted(self):
        return self.action_cost is not None

    def enter_passage(self):
        if self.already_acted():
            return ActionError.AlreadyActed

        if self.coord not in self.level.locations:
            return ActionError.NoEntrance

        source_point = (self.level.key, self.level.locations[self.coord])

        if not self.world.has_destination(source_point):
            return ActionError.PassageLeadsNoWhere

        destination_point = self.world.get_destination(source_point)

        if not self.game.move_creature_to_level(self.creature, destination_point):
            return ActionError.PassageLeadsNoWhere

        self._do_action(self.creature.action_cost(Action.Move))

    def move(self, direction):
        if self.already_acted():
            return ActionError.AlreadyActed

        if not self.can_move(direction):
            return ActionError.IllegalMove

        self.level.move_creature_to_dir(self.creature, direction)
        move_multiplier = self.level.movement_multiplier(self.coord, direction)
        self._do_action(self.creature.action_cost(Action.Move, move_multiplier))

    def teleport(self, target_coord):
        if self.already_acted():
            return ActionError.AlreadyActed

        if not self.level.is_passable(target_coord):
            return ActionError.IllegalTeleport

        self.level.move_creature(self.creature, target_coord)
        self._do_action(self.creature.action_cost(Action.Move))

    def swap(self, direction):
        if self.already_acted():
            return ActionError.AlreadyActed

        target_coord = add_vector(self.coord, direction)
        if target_coord not in self.level.creatures:
            return ActionError.NoSwapTarget

        target_creature = self.level.creatures[target_coord]
        if not self.game.ai.willing_to_swap(target_creature, self.creature, self.player):
            return ActionError.SwapTargetResists

        self.level.swap_creature(self.creature, target_creature)
        move_multiplier = self.level.movement_multiplier(self.coord, direction)
        self._do_action(self.creature.action_cost(Action.Move, move_multiplier))

    def attack(self, direction):
        if self.already_acted():
            return ActionError.AlreadyActed

        target_coord = add_vector(self.coord, direction)

        if target_coord in self.level.creatures:
            target = self.level.creatures[target_coord]
        else:
            target = self.level.tiles[target_coord]

        succeeds, damage = get_melee_attack_cr(self.creature, target)
        died = False
        if damage:
            target.receive_damage(damage)
            died = target.is_dead()
        if died:
            self.game.creature_death(target)
        self._do_action(self.creature.action_cost(Action.Attack))
        personity = (self.creature is self.player, target is self.player)
        msg = get_combat_message(succeeds, damage, died, personity, self.creature.name, target.name)
        self.game.io.msg(msg)

    def drop_items(self, item_indexes):
        items = self.creature.equipment.unbag_items(item_indexes)
        self.level.deposit_items(self.coord, items)
        self._do_action(self.creature.action_cost(Action.Exchange_Items))

    def save(self):
        """Zero cost player action. Will exit out to the event loop for the saving to happen."""
        if self.creature is not self.game.player:
            return ActionError.PlayerAction

        self.game.save_mark = True
        self._do_action(0)

    def quit(self):
        """Free player action."""
        if self.creature is not self.game.player:
            return ActionError.PlayerAction

        self.game.endgame(ask=False)

    def redraw(self):
        """Free player action."""
        if self.creature is not self.game.player:
            return ActionError.PlayerAction

        self.game.redraw()

    def can_reach(self, target_coord):
        """Free action."""
        return (self.coord == target_coord or
            get_vector(self.coord, target_coord) in Dir.All)

    def can_move(self, direction):
        """Free action."""
        if direction not in Dir.AllPlusStay:
            raise ValueError("Illegal movement direction: {}".format(direction))
        elif direction == Dir.Stay:
            return True
        else:
            coord = add_vector(self.coord, direction)
            return self.level.is_legal(coord) and self.level.is_passable(coord)

    def target_within_sight_distance(self, target_coord):
        """Free action."""
        cy, cx = self.coord
        ty, tx = target_coord
        return (cy - ty) ** 2 + (cx - tx) ** 2 <= self.creature.sight ** 2

    def target_in_sight(self, target_coord):
        """Free action."""
        return (self.target_within_sight_distance(target_coord) and
                self.level.check_los(self.coord, target_coord))
