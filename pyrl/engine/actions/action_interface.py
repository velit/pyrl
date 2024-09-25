from __future__ import annotations

from collections.abc import Iterable, Callable
from dataclasses import dataclass, field
from typing import NoReturn, TYPE_CHECKING, ParamSpec, Concatenate

from pyrl.engine.actions.action import Action
from pyrl.engine.actions.action_exceptions import IllegalMoveException, NoValidTargetException
from pyrl.engine.actions.action_feedback import AttackFeedback, ActionFeedback, MoveFeedback, DropItemsFeedback, \
    PickItemsFeedback, DisplacementFeedback, SwapFeedback
from pyrl.engine.behaviour.coordinates import get_vector, vector_is_direction, add_vector
from pyrl.engine.creature.advanced.mixins.hoarder import Hoarder
from pyrl.engine.creature.advanced.mixins.visionary import Visionary
from pyrl.engine.creature.creature import Creature
from pyrl.engine.world.item import Item
from pyrl.engine.structures.helper_mixins import GameMixin, CreatureMixin
from pyrl.engine.enums.directions import Direction, Dir, Coord
from pyrl.engine.world.tile import Tile
from pyrl.engine.world.enums.level_location import LevelLocation

if TYPE_CHECKING:
    from pyrl.engine.game import Game

P = ParamSpec("P")
def creature_action(action_method: ActionInterfaceMethod[P]) -> ActionInterfaceMethod[P]:
    def creature_wrapper(self: ActionInterface, /, *args: P.args, **kwargs: P.kwargs) -> ActionFeedback:
        self._assert_not_acted_yet()
        feedback: ActionFeedback = action_method(self, *args, **kwargs)
        if isinstance(feedback, MoveFeedback):
            self._act(feedback.action, feedback.move_multiplier)
        else:
            self._act(feedback.action, 1.0)
        return feedback
    return creature_wrapper

def player_action(action_method: ActionInterfaceMethod[P]) -> ActionInterfaceMethod[P]:
    def player_wrapper(self: ActionInterface, /, *args: P.args, **kwargs: P.kwargs) -> ActionFeedback:
        self._assert_player()
        self._assert_not_acted_yet()
        feedback: ActionFeedback = action_method(self, *args, **kwargs)
        self._act(feedback.action, 1.0)
        return feedback
    return player_wrapper

@dataclass
class ActionInterface(GameMixin, CreatureMixin):
    """ActionInterface is the bridge between controllers (user_controller.py, ai_controller.py) and the game."""

    game: Game
    creature: Creature = field(init=False)
    action_cost: int | None = field(init=False, default=None)

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

    @creature_action
    def act_to_dir(self, direction: Direction) -> ActionFeedback:
        target_coord = add_vector(self.coord, direction)
        if target_coord in self.level.creatures:
            return self.attack(direction)
        elif self.can_move(direction):
            return self.move(direction)
        else:
            raise IllegalMoveException("Creature tried to move illegally.",
                                       "You can't move there.")

    @creature_action
    def enter_passage(self) -> ActionFeedback:
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
        return DisplacementFeedback(Action.Enter_Passage, self.creature.coord, self.inspect_floor_items())

    @creature_action
    def move(self, direction: Direction) -> ActionFeedback:
        if not self.can_move(direction):
            raise IllegalMoveException("Creature tried to move illegally.",
                                       "You can't move there.")

        self.level.move_creature_to_dir(self.creature, direction)
        move_multiplier = self.level.movement_multiplier(self.coord, direction)
        return MoveFeedback(self.creature.coord, self.inspect_floor_items(), direction, move_multiplier)

    @creature_action
    def teleport(self, target_coord: Coord) -> ActionFeedback:
        if not self.level.is_passable(target_coord):
            raise IllegalMoveException("Creature tried to teleport to an illegal location.",
                                       "You can't teleport there.")

        self.level.move_creature(self.creature, target_coord)
        return DisplacementFeedback(Action.Teleport, self.creature.coord, self.inspect_floor_items())

    @creature_action
    def swap(self, direction: Direction) -> ActionFeedback:
        target_coord = add_vector(self.coord, direction)
        if target_coord not in self.level.creatures:
            raise NoValidTargetException("Creature tried to swap with a target that doesn't exist.",
                                         "There isn't a creature there to swap with.")

        target = self.level.creatures[target_coord]
        if not self.willing_to_swap(target):
            raise NoValidTargetException("Creature tried to swap with a target that resisted the attempt.",
                                         "There isn't a creature there to swap with.")

        self.level.swap_creature(self.creature, target)
        move_multiplier = self.level.movement_multiplier(self.coord, direction)
        return SwapFeedback(self.creature.coord, self.inspect_floor_items(), direction, move_multiplier, target)

    @creature_action
    def attack(self, direction: Direction) -> ActionFeedback:
        target_coord = add_vector(self.coord, direction)
        target: Tile | Creature
        if target_coord in self.level.creatures:
            target = self.level.creatures[target_coord]
        else:
            target = self.level.tiles[target_coord]
        succeeds, died, damage, experience, levelups = self.game.creature_attack(self.creature, target)
        feedback = AttackFeedback(self.creature, target, succeeds, died, damage, experience, levelups)
        if self.creature is not self.player and self.player.can_see(self.coord):
            self.game.user_controller.process_feedback(feedback)
        return feedback

    @creature_action
    def drop_items(self, item_indexes: Iterable[int]) -> ActionFeedback:
        assert isinstance(self.creature, Hoarder), f"{self.creature} doesn't have an inventory."
        items = self.creature.inventory.unbag_items(item_indexes)
        self.level.add_items(self.coord, items)
        return DropItemsFeedback(items)

    @creature_action
    def pickup_items(self, item_indexes: Iterable[int]) -> ActionFeedback:
        assert isinstance(self.creature, Hoarder), f"{self.creature} doesn't have an inventory."
        items = self.level.pop_items(self.coord, item_indexes)
        self.creature.inventory.bag_items(items)
        return PickItemsFeedback(items)

    @creature_action
    def wait(self) -> ActionFeedback:
        return ActionFeedback(Action.Wait)

    # Player only actions

    @player_action
    def debug_action(self) -> ActionFeedback:
        return ActionFeedback(Action.Debug)

    @player_action
    def redraw_action(self) -> ActionFeedback:
        self.game.redraw()
        return ActionFeedback(Action.Redraw)

    @player_action
    def save(self) -> ActionFeedback:
        return ActionFeedback(Action.Save)

    def quit(self) -> NoReturn:
        self._assert_player()
        self.game.end_game()

    # (Free) operations available for creatures

    def can_move(self, direction: Direction) -> bool:
        if direction not in Dir.AllPlusStay:
            raise ValueError(f"Illegal movement direction: {direction}")
        elif direction == Dir.Stay:
            return True
        else:
            coord = add_vector(self.coord, direction)
            return self.level.is_legal(coord) and self.level.is_passable(coord)

    def can_reach(self, target_coord: Coord) -> Direction | None:
        vector = get_vector(self.coord, target_coord)
        if vector_is_direction(vector):
            return vector
        else:
            return None

    def get_coords_of_creatures_in_vision(self, include_player: bool = False) -> set[Coord]:
        assert isinstance(self.creature, Visionary), f"{self.creature} doesn't remember vision."
        if include_player:
            return self.creature.vision & self.level.creatures.keys()
        else:
            return self.creature.vision & self.level.creatures.keys() - {self.coord}

    def get_passage(self) -> LevelLocation | None:
        try:
            return self.level.locations[self.coord]
        except KeyError:
            return None

    def get_tile(self) -> Tile:
        return self.level.tiles[self.creature.coord]

    def inspect_character_items(self) -> tuple[Item, ...]:
        assert isinstance(self.creature, Hoarder), f"{self.creature} doesn't have an inventory."
        return self.creature.inventory.inspect_items()

    def inspect_floor_items(self) -> tuple[Item, ...]:
        return self.level.inspect_items(self.coord)

    def redraw(self) -> None:
        self.game.redraw()

    def target_in_sight(self, target_coord: Coord) -> bool:
        return self.creature.can_see(target_coord)

    def willing_to_swap(self, target_creature: Creature) -> bool:
        return self.creature is not self.player and target_creature not in self.game.ai_state

    def _act(self, action: Action, action_multiplier: float = 1.0) -> None:
        assert action != Action.No_Action, f"Idea behind the {action} is it's not marked into creature actions."
        self.action_cost = self.creature.action_cost(action, action_multiplier)

    def _assert_player(self) -> None:
        assert self.creature is self.game.player, f"{self.creature} tried to execute a player only action."

    def _assert_not_acted_yet(self) -> None:
        assert self.action_cost is None, f"{self.creature} tried to act multiple times"

ActionInterfaceMethod = Callable[Concatenate[ActionInterface, P], ActionFeedback]
