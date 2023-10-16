from __future__ import annotations

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
