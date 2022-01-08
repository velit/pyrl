from __future__ import annotations

from typing import NoReturn, Iterable, TypeGuard, Literal, TYPE_CHECKING, TypeVar

from pyrl.creature.action import Action, IllegalMoveException, NoValidTargetException
from pyrl.creature.creature import Creature
from pyrl.creature.item import Item
from pyrl.creature.mixins.hoarder import Hoarder
from pyrl.creature.mixins.visionary import Visionary
from pyrl.functions.combat import get_melee_attack_cr, get_combat_message
from pyrl.functions.coord_algorithms import get_vector, add_vector, vector_is_direction
from pyrl.structures.helper_mixins import GameMixin, CreatureMixin
from pyrl.types.coord import Coord
from pyrl.types.direction import Direction, Dir
from pyrl.types.level_location import LevelLocation
from pyrl.world.tile import Tile

if TYPE_CHECKING:
    from pyrl.game import Game

class GameActions(GameMixin, CreatureMixin):
    """
    GameActions is the interface between creature controllers (user_controller.py, ai.py) and the game.

    All the non-free actions return a GameFeedback namedtuple with .type and .params fields. The
    ActionError Enum is used to find out if the feedback didn't succeed. Action Enum can be used to
    find out which succeeded action was made and .params exists for some actions giving additional
    info about the action.
    """

    creature: Creature

    def __init__(self, game: Game) -> None:
        self.game: Game = game
        self.action_cost: int | None = None

    def associate_creature(self, creature: Creature) -> None:
        self.creature = creature
        self.action_cost = None

    def verify_and_get_cost(self, action: Action) -> int:
        """Verify action cost is defined and return it."""
        assert self.action_cost is not None, \
            f"{self.creature} did {action} but its cost wasn't registered into GameActions"
        assert self.action_cost >= 0, \
            f"A negative {self.action_cost=} is not allowed (yet at least)."
        return self.action_cost

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
        if self.coord not in self.level.locations:
            raise NoValidTargetException("Creature tried to enter a passage in a place without one.",
                                         "This location doesn't have a passage.")

        source_point = self.level.get_world_point(self.coord)
        if not self.game.world.has_destination(source_point):
            raise NoValidTargetException("Creature tried to enter a passage that leads nowhere.",
                                         "This passage doesn't seem to lead anywhere.")

        destination_point = self.game.world.get_destination(source_point)

        if not self.game.move_creature_to_level(self.creature, destination_point):
            raise NoValidTargetException("Creature tried to enter a passage that leads nowhere.",
                                         "This passage doesn't seem to lead anywhere.")

        return self._act(Action.Enter_Passage)

    def move(self, direction: Direction) -> Literal[Action.Move]:
        if not self.can_move(direction):
            raise IllegalMoveException("Creature tried to move illegally.",
                                       "You can't move there.")

        self.level.move_creature_to_dir(self.creature, direction)
        move_multiplier = self.level.movement_multiplier(self.coord, direction)
        return self._act(Action.Move, move_multiplier)

    def teleport(self, target_coord: Coord) -> Literal[Action.Teleport]:
        if not self.level.is_passable(target_coord):
            raise IllegalMoveException("Creature tried to teleport to an illegal location.",
                                       "You can't teleport there.")

        self.level.move_creature(self.creature, target_coord)
        return self._act(Action.Teleport)

    def swap(self, direction: Direction) -> Literal[Action.Swap]:
        target_coord = add_vector(self.coord, direction)
        if target_coord not in self.level.creatures:
            raise NoValidTargetException("Creature tried to swap with a target that doesn't exist.",
                                         "There isn't a creature there to swap with.")

        target_creature = self.level.creatures[target_coord]
        if not self.willing_to_swap(target_creature):
            raise NoValidTargetException("Creature tried to swap with a target that resisted the attempt.",
                                         "There isn't a creature there to swap with.")

        self.level.swap_creature(self.creature, target_creature)
        move_multiplier = self.level.movement_multiplier(self.coord, direction)
        return self._act(Action.Swap, move_multiplier)

    def attack(self, direction: Direction) -> Literal[Action.Attack]:
        target_coord = add_vector(self.coord, direction)
        target: Tile | Creature
        if target_coord in self.level.creatures:
            target = self.level.creatures[target_coord]
        else:
            target = self.level.tiles[target_coord]

        succeeds, damage = get_melee_attack_cr(self.creature, target)
        died = False
        if isinstance(target, Creature):
            if damage:
                target.receive_damage(damage)
                died = target.is_dead()
            if died:
                self.game.creature_death(target)
        self._attack_user_message(succeeds, damage, died, target)
        return self._act(Action.Attack)

    def _attack_user_message(self, succeeds: bool, damage: int, died: bool, target: Creature | Tile) -> None:
        player_attacker: bool = self.creature is self.player
        player_target: bool = target is self.player
        if player_attacker or player_target:
            msg = get_combat_message(succeeds, damage, died, player_attacker, player_target,
                                     self.creature.name, target.name)
            self.game.io.msg(msg)

    def drop_items(self, item_indexes: Iterable[int]) -> tuple[Literal[Action.Drop_Items], str]:
        assert isinstance(self.creature, Hoarder), f"{self.creature} doesn't have an inventory."

        items = self.creature.inventory.unbag_items(item_indexes)
        self.level.add_items(self.coord, items)
        if len(items) == 1:
            message = f"a {items[0].name}"
        else:
            message = f"a collection of items"
        return self._act(Action.Drop_Items), message

    def pickup_items(self, item_indexes: Iterable[int]) -> tuple[Literal[Action.Pick_Items], str]:
        assert isinstance(self.creature, Hoarder), f"{self.creature} doesn't have an inventory."

        items = self.level.pop_items(self.coord, item_indexes)
        self.creature.inventory.bag_items(items)
        if len(items) == 1:
            message = f"a {items[0].name}"
        else:
            message = f"a collection of items"
        return self._act(Action.Pick_Items), message

    def wait(self) -> Literal[Action.Wait]:
        return self._act(Action.Wait)

    def willing_to_swap(self, target_creature: Creature) -> bool:
        return self.creature is not self.player and target_creature not in self.game.ai_state

    def debug_action(self) -> Literal[Action.Debug]:
        return self._player_act(Action.Debug)

    # Player only actions

    def redraw(self) -> Literal[Action.Redraw]:
        self.game.redraw()
        return self._player_act(Action.Redraw)

    def redraw_no_action(self) -> Literal[Action.No_Action]:
        self.game.redraw()
        return Action.No_Action

    def save(self) -> tuple[Literal[Action.Save], str]:
        self._assert_player()
        save_message = self.game.savegame()
        return self._player_act(Action.Save), save_message

    def quit(self) -> NoReturn:
        self._assert_player()
        self.game.endgame()

    # (Free) operations available for creatures

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
        GameActions._assert_inventory(self.creature)
        assert isinstance(self.creature, Hoarder), f"{self.creature} doesn't have an inventory."
        return self.creature.inventory.inspect_items()

    def can_reach(self, target_coord: Coord) -> Direction | None:
        vector = get_vector(self.coord, target_coord)
        if vector_is_direction(vector):
            return vector
        else:
            return None

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

    @staticmethod
    def has_inventory(creature: Creature) -> TypeGuard[Hoarder]:
        return isinstance(creature, Hoarder)

    @staticmethod
    def _assert_inventory(creature: Creature) -> TypeGuard[Hoarder]:
        assert GameActions.has_inventory(creature), f"{creature} doesn't have an inventory."
        return True

    def _assert_player(self) -> None:
        assert self.creature is self.game.player, f"{self.creature} tried to execute a player only action."

    def _assert_not_acted_yet(self) -> None:
        assert self.action_cost is None, f"{self.creature} tried to act multiple times"

    A = TypeVar('A', bound=Action)

    def _act(self, action: A, action_multiplier: float = 1.0) -> A:
        assert action != Action.No_Action, f"Idea behind the {action} is it's not marked into creature actions."
        self._assert_not_acted_yet()
        self.action_cost = self.creature.action_cost(action, action_multiplier)
        return action

    def _player_act(self, action: A) -> A:
        self._assert_player()
        return self._act(action)

    def _clear_action(self, and_associate_creature: Creature | None = None) -> None:
        self.action_cost = None
        if and_associate_creature:
            self.creature = and_associate_creature
