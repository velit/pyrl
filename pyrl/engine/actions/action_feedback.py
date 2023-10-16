from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from pyrl.engine.actions.action import Action
from pyrl.engine.creature.creature import Creature
from pyrl.engine.world.item import Item
from pyrl.engine.enums.directions import Direction, Coord
from pyrl.engine.world.tile import Tile

@dataclass
class ActionFeedback:
    action: Action

NoActionFeedback = ActionFeedback(Action.No_Action)

@dataclass
class DisplacementFeedback(ActionFeedback):
    action: Action
    coord: Coord
    items: Sequence[Item]

@dataclass
class MoveFeedback(DisplacementFeedback):
    direction: Direction
    move_multiplier: float

    action: Action = field(init=False, default=Action.Move)

@dataclass
class SwapFeedback(MoveFeedback):
    target: Creature

    action: Action = field(init=False, default=Action.Swap)

@dataclass
class AttackFeedback(ActionFeedback):
    attacker: Creature
    target: Tile | Creature
    succeeds: bool
    target_died: bool
    damage: int
    experience: int
    levelups: Sequence[int]

    action: Action = field(init=False, default=Action.Attack)

@dataclass
class DropItemsFeedback(ActionFeedback):
    items: Sequence[Item]

    action: Action = field(init=False, default=Action.Drop_Items)

@dataclass
class PickItemsFeedback(ActionFeedback):
    items: Sequence[Item]

    action: Action = field(init=False, default=Action.Pick_Items)
