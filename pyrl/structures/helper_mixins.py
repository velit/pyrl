"""Bunch of property getter mixins to flatten the hierarchy of the game a bit in certain places"""
from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from pyrl.creature.creature import Creature
    from pyrl.creature.player import Player
    from pyrl.game import Game
    from pyrl.creature.game_actions import GameActions
    from pyrl.structures.dimensions import Dimensions
    from pyrl.types.coord import Coord
    from pyrl.window.window_system import WindowSystem
    from pyrl.world.level import Level
    from pyrl.world.world import World

class HasGame(Protocol):
    @property
    def game(self) -> Game:
        raise NotImplementedError

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
    @property
    def creature(self) -> Creature:
        raise NotImplementedError

class CreatureMixin:

    @property
    def coord(self: HasCreature) -> Coord:
        return self.creature.coord

    @property
    def level(self: HasCreature) -> Level:
        return self.creature.level

class HasDimensions(Protocol):
    @property
    def dimensions(self) -> Dimensions:
        raise NotImplementedError

class DimensionsMixin:
    @property
    def rows(self: HasDimensions) -> int:
        return self.dimensions.rows

    @property
    def cols(self: HasDimensions) -> int:
        return self.dimensions.cols

class HasCreatureActions(Protocol):
    @property
    def actions(self) -> GameActions:
        raise NotImplementedError

class CreatureActionsMixin:

    @property
    def creature(self: HasCreatureActions) -> Creature:
        return self.actions.creature

    @property
    def coord(self: HasCreatureActions) -> Coord:
        return self.actions.creature.coord

    @property
    def level(self: HasCreatureActions) -> Level:
        return self.actions.creature.level

    @property
    def io(self: HasCreatureActions) -> WindowSystem:
        return self.actions.game.io

    @property
    def world(self: HasCreatureActions) -> World:
        return self.actions.game.world

    @property
    def player(self: HasCreatureActions) -> Player:
        return self.actions.game.world.player
