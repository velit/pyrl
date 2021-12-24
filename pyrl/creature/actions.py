from __future__ import annotations

from enum import Enum

class Action(Enum):
    No_Action      = "Creature didn't do an action.",  0
    Free_Action    = "Creature did a free action.",    0
    Save           = "Player saved.",                  0
    Redraw         = "Player redrew the screen.",      0
    Generic        = "Creature did a generic action.", 1000
    Attack         = "Creature attacked.",             1000
    Debug          = "Creature did a debug action.",   0
    Drop_Items     = "Creature dropped items.",        1000
    Enter_Passage  = "Creature entered a passage.",    1000
    Move           = "Creature moved.",                1000
    Pick_Items     = "Creature picked up items.",      1000
    Spawn          = "Creature spawned.",              500
    Swap           = "Creature swapped.",              1000
    Teleport       = "Creature teleported.",           1000
    Wait           = "Creature waited.",               1000

    def __init__(self, description: str, base_cost: int) -> None:
        self.description = description
        self.base_cost = base_cost

class ActionException(Exception):
    def __init__(self, message: str, player_message: str | None = None):
        self.message = message
        if player_message is not None:
            self.player_message = player_message
        else:
            self.player_message = message

class IllegalMoveException(ActionException): pass

class NoValidTargetException(ActionException): pass

class IllegalContextException(ActionException): pass
