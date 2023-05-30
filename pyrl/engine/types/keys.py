from __future__ import annotations

from enum import StrEnum

AnyKey = str
KeyTuple = tuple[AnyKey, ...]

class KeySequence(tuple[AnyKey, ...]):

    @property
    def key(self) -> AnyKey:
        if len(self):
            return self[0]
        else:
            return "Unbound"

    def __str__(self) -> str:
        return "/".join(f"{key}" for key in self)

class Key(StrEnum):
    LEFT           = "Left"
    RIGHT          = "Right"
    UP             = "Up"
    DOWN           = "Down"
    F1             = "F1"
    F2             = "F2"
    F3             = "F3"
    F4             = "F4"
    F5             = "F5"
    F6             = "F6"
    F7             = "F7"
    F8             = "F8"
    F9             = "F9"
    F10            = "F10"
    F11            = "F11"
    F12            = "F12"
    ESC            = "Esc"
    TAB            = "Tab"
    SHIFT_TAB      = "Shift+Tab"
    BACKSPACE      = "Backspace"
    SPACE          = "Space"
    ENTER          = "Enter"
    INSERT         = "Insert"
    DELETE         = "Delete"
    HOME           = "Home"
    END            = "End"
    PAGE_UP        = "Page Up"
    PAGE_DOWN      = "Page Down"
    NUMPAD_0       = "Numpad 0"
    NUMPAD_1       = "Numpad 1"
    NUMPAD_2       = "Numpad 2"
    NUMPAD_3       = "Numpad 3"
    NUMPAD_4       = "Numpad 4"
    NUMPAD_5       = "Numpad 5"
    NUMPAD_6       = "Numpad 6"
    NUMPAD_7       = "Numpad 7"
    NUMPAD_8       = "Numpad 8"
    NUMPAD_9       = "Numpad 9"
    WINDOW_RESIZE  = "Window Resize"
    CLOSE_WINDOW   = "Close Window"

    # The IO system will never return this value
    UNDEFINED      = "Undefined"
    # Do not bind. Returned by the IO system when something has to be returned and there is no input
    NO_INPUT       = "No Input"

KeyOrSequence = AnyKey | KeySequence
