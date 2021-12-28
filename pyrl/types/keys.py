from __future__ import annotations

from typing import Final

Key = str
KeyTuple = tuple[Key, ...]
class Keys:
    LEFT:           Final = "Left"
    RIGHT:          Final = "Right"
    UP:             Final = "Up"
    DOWN:           Final = "Down"
    F1:             Final = "F1"
    F2:             Final = "F2"
    F3:             Final = "F3"
    F4:             Final = "F4"
    F5:             Final = "F5"
    F6:             Final = "F6"
    F7:             Final = "F7"
    F8:             Final = "F8"
    F9:             Final = "F9"
    F10:            Final = "F10"
    F11:            Final = "F11"
    F12:            Final = "F12"
    ESC:            Final = "Esc"
    TAB:            Final = "Tab"
    SHIFT_TAB:      Final = "Shift+Tab"
    BACKSPACE:      Final = "Backspace"
    SPACE:          Final = "Space"
    ENTER:          Final = "Enter"
    INSERT:         Final = "Insert"
    DELETE:         Final = "Delete"
    HOME:           Final = "Home"
    END:            Final = "End"
    PAGE_UP:        Final = "Page Up"
    PAGE_DOWN:      Final = "Page Down"
    NUMPAD_0:       Final = "Numpad 0"
    NUMPAD_1:       Final = "Numpad 1"
    NUMPAD_2:       Final = "Numpad 2"
    NUMPAD_3:       Final = "Numpad 3"
    NUMPAD_4:       Final = "Numpad 4"
    NUMPAD_5:       Final = "Numpad 5"
    NUMPAD_6:       Final = "Numpad 6"
    NUMPAD_7:       Final = "Numpad 7"
    NUMPAD_8:       Final = "Numpad 8"
    NUMPAD_9:       Final = "Numpad 9"
    WINDOW_RESIZE:  Final = "Window Resize"
    CLOSE_WINDOW:   Final = "Close Window"

    # The IO system will never return this value
    UNDEFINED:      Final = "Undefined"
    # Do not bind. Returned by the IO system when something has to be returned and there is no input
    NO_INPUT:       Final = "No Input"
