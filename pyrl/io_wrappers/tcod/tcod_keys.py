from __future__ import annotations

from tcod.event import KeySym

from pyrl.types.keys import Keys

key_map: dict[int, str] = {
    KeySym.BACKSPACE: Keys.BACKSPACE,
    KeySym.DELETE:    Keys.DELETE,
    KeySym.DOWN:      Keys.DOWN,
    KeySym.END:       Keys.END,
    KeySym.ESCAPE:    Keys.ESC,
    KeySym.F10:       Keys.F10,
    KeySym.F11:       Keys.F11,
    KeySym.F12:       Keys.F12,
    KeySym.F1:        Keys.F1,
    KeySym.F2:        Keys.F2,
    KeySym.F3:        Keys.F3,
    KeySym.F4:        Keys.F4,
    KeySym.F5:        Keys.F5,
    KeySym.F6:        Keys.F6,
    KeySym.F7:        Keys.F7,
    KeySym.F8:        Keys.F8,
    KeySym.F9:        Keys.F9,
    KeySym.HOME:      Keys.HOME,
    KeySym.INSERT:    Keys.INSERT,
    KeySym.LEFT:      Keys.LEFT,
    KeySym.N0:        Keys.NUMPAD_0,
    KeySym.N1:        Keys.NUMPAD_1,
    KeySym.N2:        Keys.NUMPAD_2,
    KeySym.N3:        Keys.NUMPAD_3,
    KeySym.N4:        Keys.NUMPAD_4,
    KeySym.N5:        Keys.NUMPAD_5,
    KeySym.N6:        Keys.NUMPAD_6,
    KeySym.N7:        Keys.NUMPAD_7,
    KeySym.N8:        Keys.NUMPAD_8,
    KeySym.N9:        Keys.NUMPAD_9,
    KeySym.PAGEDOWN:  Keys.PAGE_DOWN,
    KeySym.PAGEUP:    Keys.PAGE_UP,
    KeySym.RETURN2:   Keys.ENTER,
    KeySym.RETURN:    Keys.ENTER,
    KeySym.RIGHT:     Keys.RIGHT,
    KeySym.SPACE:     Keys.SPACE,
    KeySym.TAB:       Keys.TAB,
    KeySym.UNKNOWN:   Keys.NO_INPUT,
    KeySym.UP:        Keys.UP,
}

ignore_keys: set[KeySym] = {
    KeySym.LALT,
    KeySym.LCTRL,
    KeySym.LSHIFT,
    KeySym.LGUI,
    KeySym.RALT,
    KeySym.RCTRL,
    KeySym.RSHIFT,
    KeySym.RGUI,
}
