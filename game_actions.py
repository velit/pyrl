from __future__ import absolute_import, division, print_function, unicode_literals

from enum import Enum
from combat import get_melee_attack_cr, get_combat_message
from creature.actions import Action
from generic_algorithms import add_vector


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
        self.action_cost = -1
        if creature:
            self.creature = creature

    def clear_action(self, and_associate_creature=None):
        self.action_cost = -1
        if and_associate_creature:
            self.creature = and_associate_creature

    def already_acted(self):
        return self.action_cost >= 0

    def do_action(self, cost):
        self.action_cost = cost

    def enter_passage(self):
        game, level, creature = self.game, self.creature.level, self.creature

        if self.already_acted():
            return ActionError.AlreadyActed

        if not level.is_exit(creature.coord):
            return ActionError.NoEntrance

        passage = level.get_exit(creature.coord)
        dest_world_loc, dest_passage = level.get_destination_info(passage)

        if not game.move_creature_to_level(creature, dest_world_loc, dest_passage):
            return ActionError.PassageLeadsNoWhere

        self.do_action(creature.action_cost(Action.Move))

    def move(self, direction):
        level, creature = self.creature.level, self.creature

        if self.already_acted():
            return ActionError.AlreadyActed

        if not level.creature_can_move(creature, direction):
            return ActionError.IllegalMove

        level.move_creature_to_dir(creature, direction)
        move_multiplier = level.movement_multiplier(creature.coord, direction)
        self.do_action(creature.action_cost(Action.Move, move_multiplier))

    def teleport(self, target_coord):
        level, creature = self.creature.level, self.creature
        if self.already_acted():
            return ActionError.AlreadyActed

        if not level.is_passable(target_coord):
            return ActionError.IllegalTeleport

        level.move_creature(creature, target_coord)
        self.do_action(creature.action_cost(Action.Move))

    def swap(self, direction):
        game, level, creature = self.game, self.creature.level, self.creature
        if self.already_acted():
            return ActionError.AlreadyActed

        target_coord = add_vector(creature.coord, direction)
        if not level.has_creature(target_coord):
            return ActionError.NoSwapTarget

        target_creature = level.get_creature(target_coord)
        if not game.ai.willing_to_swap(target_creature, creature, game.player):
            return ActionError.SwapTargetResists

        level.swap_creature(creature, target_creature)
        move_multiplier = level.movement_multiplier(creature.coord, direction)
        self.do_action(creature.action_cost(Action.Move, move_multiplier))

    def attack(self, direction):
        game, level, creature = self.game, self.creature.level, self.creature

        if self.already_acted():
            return ActionError.AlreadyActed

        target_coord = add_vector(creature.coord, direction)

        if level.has_creature(target_coord):
            target = level.get_creature(target_coord)
        else:
            target = level.tiles[target_coord]

        succeeds, damage = get_melee_attack_cr(creature, target)
        died = False
        if damage:
            target.receive_damage(damage)
            died = target.is_dead()
        if died:
            game.creature_death(target)
        self.do_action(creature.action_cost(Action.Attack))
        personity = (creature is game.player, target is game.player)
        msg = get_combat_message(succeeds, damage, died, personity, creature.name, target.name)
        game.io.msg(msg)

    def save(self):
        if self.creature is not self.game.player:
            return ActionError.PlayerAction

        self.game.mark_save()
        self.do_action(0)

    def quit(self):
        if self.creature is not self.game.player:
            return ActionError.PlayerAction

        self.game.endgame(ask=False)

    def redraw(self):
        if self.creature is not self.game.player:
            return ActionError.PlayerAction

        self.game.redraw()