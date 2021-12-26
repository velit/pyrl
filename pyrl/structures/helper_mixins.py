from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from pyrl.creature.creature import Creature
    from pyrl.creature.player import Player
    from pyrl.game import Game
    from pyrl.game_actions import GameActions
    from pyrl.structures.dimensions import Dimensions
    from pyrl.types.coord import Coord
    from pyrl.window.window_system import WindowSystem
    from pyrl.world.level import Level
    from pyrl.world.world import World

class HasGame(Protocol):
    game: Game

class GameMixin:

    @property
    def io(self: HasGame) -> WindowSystem:
        return self.game.io

    @property
    def world(self: HasGame) -> World:
        return self.game.world

    @property
    def player(self: HasGame) -> Player:
        return self.game.world.player

class HasCreature(Protocol):
    creature: Creature

class CreatureMixin:

    @property
    def coord(self: HasCreature) -> Coord:
        return self.creature.coord

    @property
    def level(self: HasCreature) -> Level:
        return self.creature.level

class HasDimensions(Protocol):
    dimensions: Dimensions

class DimensionsMixin:
    @property
    def rows(self: HasDimensions) -> int:
        return self.dimensions.rows

    @property
    def cols(self: HasDimensions) -> int:
        return self.dimensions.cols

class HasGameActions(Protocol):
    actions: GameActions

class GameActionsMixin:
    """
    Helper class to access the hierarchy of the game easier in controller classes.

    Remember to set the self.actions variable correctly in classes that use this.
    """

    @property
    def creature(self: HasGameActions) -> Creature:
        return self.actions.creature

    @property
    def coord(self: HasGameActions) -> Coord:
        return self.actions.creature.coord

    @property
    def level(self: HasGameActions) -> Level:
        return self.actions.creature.level

    @property
    def io(self: HasGameActions) -> WindowSystem:
        return self.actions.game.io

    @property
    def world(self: HasGameActions) -> World:
        return self.actions.game.world

    @property
    def player(self: HasGameActions) -> Player:
        return self.actions.game.world.player
