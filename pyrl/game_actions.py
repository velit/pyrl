from collections import namedtuple
from enum import Enum
from functools import wraps

from pyrl.combat import get_melee_attack_cr, get_combat_message
from pyrl.enums.directions import Dir
from pyrl.generic_algorithms import add_vector, get_vector


GameFeedback = namedtuple("GameFeedback", "type, params")


class ActionError(Enum):
    AlreadyActed        = "Creature tried to act multiple times."
    IllegalMove         = "Creature tried to move illegally."
    IllegalTeleport     = "Creature tried to teleport illegally."
    SwapTargetResists   = "Creature tried to swap with a target that resisted the attempt."
    NoSwapTarget        = "Creature tried to swap with a target that doesn't exist."
    PassageLeadsNoWhere = "Creature tried to enter a passage that leads nowhere."
    NoPassage           = "Creature tried to enter a passage in a place without one."
    NoItemsOnGround     = "Creature tried to pick up items in a place without any."
    PlayerAction        = "Creature tried to execute a player only action."

    def __str__(self):
        return self.value


class Action(Enum):
    Generic        = "Creature did a generic action."
    Move           = "Creature moved."
    Wait           = "Creature waited."
    Attack         = "Creature attacked."
    Swap           = "Creature swapped."
    Exchange_Items = "Creature exchanged items."
    Enter_Passage  = "Creature entered a passage."
    Spawn          = "Creature spawned."
    Teleport       = "Creature teleported."
    Debug          = "Creature did a debug action."

    @property
    def base_cost(self):
        if self in action_cost:
            return action_cost[self]
        else:
            return action_cost[Action.Generic]

    def __str__(self):
        return self.value


action_cost = {
    Action.Generic: 1000,
    Action.Spawn:   500,
}


action_params = {
    Action.Move:          namedtuple("Action", "direction"),
    Action.Attack:        namedtuple("Action", "target, succeeds, damage, died"),
    Action.Swap:          namedtuple("Action", "direction, target"),
    Action.Teleport:      namedtuple("Action", "destination"),
    Action.Enter_Passage: namedtuple("Action", "passage"),
}


def feedback(feedback, *params):
    if params:
        assert feedback in action_params, "No entry found in action_params for {}".format(feedback)
        return GameFeedback(feedback, action_params[feedback](*params))
    else:
        return GameFeedback(feedback, ())


def player_action(func):

    @wraps(func)
    def player_check_wrapper(self, *args, **kwargs):
        if self.creature is not self.game.player:
            return feedback(ActionError.PlayerAction)
        else:
            return func(self, *args, **kwargs)
    return player_check_wrapper


class GameActions(object):

    """
    GameActions is the interface between creature controllers (player, ai) and the game.

    All the non-free actions return a GameFeedback namedtuple with .type and .params fields. The
    ActionError Enum is used to find out if the feedback didn't succeed. Action Enum can be used to
    find out which succeeded action was made and .params exists for some actions giving additional
    info about the action.
    """

    coord  = property(lambda self: self.creature.coord)
    level  = property(lambda self: self.creature.level)
    io     = property(lambda self: self.game.io)
    world  = property(lambda self: self.game.world)
    player = property(lambda self: self.game.world.player)

    def __init__(self, game, creature=None):
        self.game = game
        self.action_cost = None
        if creature:
            self.creature = creature

    def already_acted(self):
        return self.action_cost is not None

    def act_to_dir(self, direction):
        target_coord = add_vector(self.coord, direction)
        if target_coord in self.level.creatures:
            return self.attack(direction)
        elif self.can_move(direction):
            return self.move(direction)
        else:
            return feedback(ActionError.IllegalMove)

    def enter_passage(self):
        if self.already_acted():
            return feedback(ActionError.AlreadyActed)

        if self.coord not in self.level.locations:
            return feedback(ActionError.NoPassage)

        source_point = (self.level.key, self.level.locations[self.coord])

        if not self.game.world.has_destination(source_point):
            return feedback(ActionError.PassageLeadsNoWhere)

        destination_point = self.game.world.get_destination(source_point)

        if not self.game.move_creature_to_level(self.creature, destination_point):
            return feedback(ActionError.PassageLeadsNoWhere)

        self._do_action(self.creature.action_cost(Action.Move))
        return feedback(Action.Enter_Passage)

    def move(self, direction):
        if self.already_acted():
            return feedback(ActionError.AlreadyActed)

        if not self.can_move(direction):
            return feedback(ActionError.IllegalMove)

        self.level.move_creature_to_dir(self.creature, direction)
        move_multiplier = self.level.movement_multiplier(self.coord, direction)
        self._do_action(self.creature.action_cost(Action.Move, move_multiplier))
        return feedback(Action.Move, direction)

    def teleport(self, target_coord):
        if self.already_acted():
            return feedback(ActionError.AlreadyActed)

        if not self.level.is_passable(target_coord):
            return feedback(ActionError.IllegalTeleport)

        self.level.move_creature(self.creature, target_coord)
        self._do_action(self.creature.action_cost(Action.Move))
        return feedback(Action.Teleport, target_coord)

    def swap(self, direction):
        if self.already_acted():
            return feedback(ActionError.AlreadyActed)

        target_coord = add_vector(self.coord, direction)
        if target_coord not in self.level.creatures:
            return feedback(ActionError.NoSwapTarget)

        target_creature = self.level.creatures[target_coord]
        if not self.willing_to_swap(target_creature):
            return feedback(ActionError.SwapTargetResists)

        self.level.swap_creature(self.creature, target_creature)
        move_multiplier = self.level.movement_multiplier(self.coord, direction)
        self._do_action(self.creature.action_cost(Action.Move, move_multiplier))
        return feedback(Action.Swap, direction, target_creature)

    def attack(self, direction):
        if self.already_acted():
            return feedback(ActionError.AlreadyActed)

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
        self._attack_user_message(succeeds, damage, died, target)

        return feedback(Action.Attack, target, succeeds, damage, died)

    def _attack_user_message(self, succeeds, damage, died, target):
        player_attacker = self.creature is self.player
        player_target = target is self.player
        if (player_attacker or player_target):
            msg = get_combat_message(succeeds, damage, died, player_attacker, player_target,
                                    self.creature.name, target.name)
            self.game.io.msg(msg)

    def drop_items(self, item_indexes):
        items = self.creature.equipment.unbag_items(item_indexes)
        self.level.add_items(self.coord, items)
        self._do_action(self.creature.action_cost(Action.Exchange_Items))
        return feedback(Action.Exchange_Items)

    def pickup_items(self, item_indexes):
        items = self.level.pop_items(self.coord, item_indexes)
        self.creature.equipment.bag_items(items)
        self._do_action(self.creature.action_cost(Action.Exchange_Items))
        return feedback(Action.Exchange_Items)

    def wait(self):
        self._do_action(self.creature.action_cost(Action.Wait))
        return feedback(Action.Wait)

    def willing_to_swap(self, target_creature):
        return self.creature is not self.player and target_creature not in self.game.ai.ai_state

    # Free Actions:

    def get_tile(self):
        """Free action."""
        return self.level.tiles[self.creature.coord]

    def get_passage(self):
        """Free action."""
        try:
            return self.level.locations[self.coord]
        except KeyError:
            return None

    def get_coords_of_creatures_in_vision(self, include_player=False):
        """Free action."""
        if include_player:
            return self.creature.vision & self.level.creatures.keys()
        else:
            return self.creature.vision & self.level.creatures.keys() - {self.coord}

    def view_floor_items(self):
        """Free action."""
        return self.level.view_items(self.coord)

    def view_character_items(self):
        """Free action."""
        return self.creature.equipment.view_items()

    def can_reach(self, target_coord):
        """Free action."""
        return (self.coord == target_coord or get_vector(self.coord, target_coord) in Dir.All)

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

    @player_action
    def save(self):
        """Free player action."""
        return self.game.savegame()

    @player_action
    def quit(self):
        """Free player action."""
        self.game.endgame()

    @player_action
    def redraw(self):
        """Free player action."""
        self.game.redraw()

    def _clear_action(self, and_associate_creature=None):
        self.action_cost = None
        if and_associate_creature:
            self.creature = and_associate_creature

    def _do_action(self, cost):
        self.action_cost = cost


class GameActionsProperties(object):

    """
    Helper class to access the hierarchy of the game easier in controller classes.

    Remember to set the self.actions variable correctly in classes that use this.
    """

    creature = property(lambda self: self.actions.creature)
    coord    = property(lambda self: self.actions.creature.coord)
    level    = property(lambda self: self.actions.creature.level)
    io       = property(lambda self: self.actions.game.io)
    world    = property(lambda self: self.actions.game.world)
    player   = property(lambda self: self.actions.game.world.player)
