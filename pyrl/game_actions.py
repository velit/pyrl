from __future__ import annotations

from typing import NoReturn, Iterable, TypeGuard, Literal, TYPE_CHECKING

from pyrl.combat import get_melee_attack_cr, get_combat_message
from pyrl.constants.coord import Coord
from pyrl.constants.direction import Direction, Dir
from pyrl.constants.level_location import LevelLocation
from pyrl.creature.actions import Action, IllegalMoveException, NoValidTargetException
from pyrl.creature.item import Item
from pyrl.creature.mixins.hoarder import Hoarder, has_inventory
from pyrl.creature.mixins.visionary import Visionary
from pyrl.generic_algorithms import add_vector, get_vector
from pyrl.world.level import Level
from pyrl.world.tile import Tile
from pyrl.world.world import World

if TYPE_CHECKING:
    from pyrl.creature.creature import Creature
    from pyrl.game import Game

class GameActions:

    """
    GameActions is the interface between creature controllers (player, ai) and the game.

    All the non-free actions return a GameFeedback namedtuple with .type and .params fields. The
    ActionError Enum is used to find out if the feedback didn't succeed. Action Enum can be used to
    find out which succeeded action was made and .params exists for some actions giving additional
    info about the action.
    """
    coord: Coord     = property(lambda self: self.creature.coord)
    level: Level     = property(lambda self: self.creature.level)
    io               = property(lambda self: self.game.io)
    world: World     = property(lambda self: self.game.world)
    player: Creature = property(lambda self: self.game.world.player)

    def __init__(self, game: Game, creature: Creature | None = None) -> None:
        self.game: Game = game
        self.action_cost: int | None = None
        if creature:
            self.creature = creature

    def already_acted(self) -> bool:
        return self.action_cost is not None

    def assert_not_acted_yet(self) -> None:
        assert not self.already_acted(), f"{self.creature} tried to act multiple times"

    def act_to_dir(self, direction: Direction) -> Literal[Action.Move] | Literal[Action.Attack]:
        target_coord = add_vector(self.coord, direction)
        if target_coord in self.level.creatures:
            return self.attack(direction)
        elif self.can_move(direction):
            return self.move(direction)
        else:
            raise IllegalMoveException("Creature tried to move illegally.",
                                       "You can't move there.")

    def enter_passage(self) -> Literal[Action.Enter_Passage]:
        self.assert_not_acted_yet()

        if self.coord not in self.level.locations:
            raise NoValidTargetException("Creature tried to enter a passage in a place without one.",
                                         "This location doesn't have a passage.")

        source_point = (self.level.level_key, self.level.locations[self.coord])

        if not self.game.world.has_destination(source_point):
            raise NoValidTargetException("Creature tried to enter a passage that leads nowhere.",
                                         "This passage doesn't seem to lead anywhere.")

        destination_point = self.game.world.get_destination(source_point)

        if not self.game.move_creature_to_level(self.creature, destination_point):
            raise NoValidTargetException("Creature tried to enter a passage that leads nowhere.",
                                         "This passage doesn't seem to lead anywhere.")

        self._apply_action_cost(self.creature.action_cost(Action.Move))
        return Action.Enter_Passage

    def move(self, direction: Direction) -> Literal[Action.Move]:
        self.assert_not_acted_yet()

        if not self.can_move(direction):
            raise IllegalMoveException("Creature tried to move illegally.",
                                       "You can't move there.")

        self.level.move_creature_to_dir(self.creature, direction)
        move_multiplier = self.level.movement_multiplier(self.coord, direction)
        self._apply_action_cost(self.creature.action_cost(Action.Move, move_multiplier))
        return Action.Move

    def teleport(self, target_coord: Coord) -> Literal[Action.Teleport]:
        self.assert_not_acted_yet()

        if not self.level.is_passable(target_coord):
            raise IllegalMoveException("Creature tried to teleport to an illegal location.",
                                       "You can't teleport there.")

        self.level.move_creature(self.creature, target_coord)
        self._apply_action_cost(self.creature.action_cost(Action.Move))
        return Action.Teleport

    def swap(self, direction: Direction) -> Literal[Action.Swap]:
        self.assert_not_acted_yet()

        target_coord = add_vector(self.coord, direction)
        if target_coord not in self.level.creatures:
            raise NoValidTargetException("Creature tried to swap with a target that doesn't exist.",
                                         "There isn't a creature there to swap with.")

        target_creature = self.level.creatures[target_coord]
        if not self.willing_to_swap(target_creature):
            raise NoValidTargetException("Creature tried to swap with a target that resisted the attempt.",
                                         "There isn't a creature there to swap with.")

        self.level.swap_creature(self.creature, target_creature)
        move_multiplier = self.level.move_multiplier(self.coord, direction)
        self._apply_action_cost(self.creature.action_cost(Action.Move, move_multiplier))
        return Action.Swap

    def attack(self, direction: Direction) -> Literal[Action.Attack]:
        self.assert_not_acted_yet()

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
        self._apply_action_cost(self.creature.action_cost(Action.Attack))
        self._attack_user_message(succeeds, damage, died, target)
        return Action.Attack

    def _attack_user_message(self, succeeds: bool, damage: int, died: bool, target: Creature) -> None:
        player_attacker: bool = self.creature is self.player
        player_target: bool = target is self.player
        if player_attacker or player_target:
            msg = get_combat_message(succeeds, damage, died, player_attacker, player_target,
                                     self.creature.name, target.name)
            self.game.io.msg(msg)

    def drop_items(self, item_indexes: Iterable[int]) -> tuple[Literal[Action.Drop_Items], str]:
        self.assert_not_acted_yet()
        assert isinstance(self.creature, Hoarder), f"{self.creature} doesn't have an inventory."

        items = self.creature.inventory.unbag_items(item_indexes)
        self.level.add_items(self.coord, items)
        self._apply_action_cost(self.creature.action_cost(Action.Drop_Items))
        if len(items) == 1:
            return Action.Drop_Items, f"a {items[0].name}"
        else:
            return Action.Drop_Items, f"a collection of items"

    def pickup_items(self, item_indexes: Iterable[int]) -> tuple[Literal[Action.Pick_Items], str]:
        self.assert_not_acted_yet()
        assert isinstance(self.creature, Hoarder), f"{self.creature} doesn't have an inventory."

        items = self.level.pop_items(self.coord, item_indexes)
        self.creature.inventory.bag_items(items)
        self._apply_action_cost(self.creature.action_cost(Action.Pick_Items))
        if len(items) == 1:
            return Action.Pick_Items, f"a {items[0].name}"
        else:
            return Action.Pick_Items, f"a collection of items"

    def wait(self) -> Literal[Action.Wait]:
        self.assert_not_acted_yet()
        self._apply_action_cost(self.creature.action_cost(Action.Wait))
        return Action.Wait

    def willing_to_swap(self, target_creature: Creature) -> bool:
        return self.creature is not self.player and target_creature not in self.game.ai.ai_state

    def no_action(self) -> Literal[Action.No_Action]:
        self._assert_player()
        self._apply_action_cost(self.creature.action_cost(Action.No_Action))
        return Action.No_Action

    # Player only actions

    def redraw(self) -> Literal[Action.Redraw]:
        self._assert_player()
        self.game.redraw()
        return Action.Redraw

    def save(self) -> tuple[Literal[Action.Save], str]:
        self._assert_player()
        save_message = self.game.savegame()
        return Action.Save, save_message

    def quit(self) -> NoReturn:
        self._assert_player()
        self.game.endgame()

    # Operations available for creatures

    def get_tile(self) -> Tile:
        return self.level.tiles[self.creature.coord]

    def get_passage(self) -> LevelLocation | None:
        try:
            return self.level.locations[self.coord]
        except KeyError:
            return None

    def get_coords_of_creatures_in_vision(self, include_player: bool = False) -> set[Coord]:
        assert isinstance(self.creature, Visionary), f"{self.creature} doesn't remember vision."
        if include_player:
            return self.creature.vision & self.level.creatures.keys()
        else:
            return self.creature.vision & self.level.creatures.keys() - {self.coord}

    def inspect_floor_items(self) -> tuple[Item, ...]:
        return self.level.inspect_items(self.coord)

    def inspect_character_items(self) -> tuple[Item, ...]:
        assert isinstance(self.creature, Hoarder), f"{self.creature} doesn't have an inventory."
        return self.creature.inventory.inspect_items()

    def can_reach(self, target_coord: Coord) -> bool:
        return self.coord == target_coord or get_vector(self.coord, target_coord) in Dir.All

    def can_move(self, direction: Direction) -> bool:
        if direction not in Dir.AllPlusStay:
            raise ValueError(f"Illegal movement direction: {direction}")
        elif direction == Dir.Stay:
            return True
        else:
            coord = add_vector(self.coord, direction)
            return self.level.is_legal(coord) and self.level.is_passable(coord)

    def target_within_sight_distance(self, target_coord: Coord) -> bool:
        cy, cx = self.coord
        ty, tx = target_coord
        return (cy - ty) ** 2 + (cx - tx) ** 2 <= self.creature.sight ** 2

    def target_in_sight(self, target_coord: Coord) -> bool:
        return (self.target_within_sight_distance(target_coord) and
                self.level.check_los(self.coord, target_coord))

    def _has_inventory(self, creature: Creature) -> TypeGuard[Hoarder]:
        assert has_inventory(creature), f"{creature} doesn't have an inventory."
        return True

    def _assert_player(self) -> None:
        assert self.creature is self.game.player, f"{self.creature} tried to execute a player only action."

    def _assert_inventory(self, creature: Creature) -> TypeGuard[Hoarder]:
        assert isinstance(creature, Hoarder), f"{self.creature} doesn't have an inventory."
        return True

    def _clear_action(self, and_associate_creature: Creature | None = None) -> None:
        self.action_cost = None
        if and_associate_creature:
            self.creature = and_associate_creature

    def _apply_action_cost(self, cost: int) -> None:
        self.action_cost = cost

class GameActionProperties:

    """
    Helper class to access the hierarchy of the game easier in controller classes.

    Remember to set the self.actions variable correctly in classes that use this.
    """

    creature: Creature       = property(lambda self: self.actions.creature)
    coord: Coord             = property(lambda self: self.actions.creature.coord)
    level: Level             = property(lambda self: self.actions.creature.level)
    io                       = property(lambda self: self.actions.game.io)
    world: World             = property(lambda self: self.actions.game.world)
    player: Creature         = property(lambda self: self.actions.game.world.player)
