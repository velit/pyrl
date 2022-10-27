from __future__ import annotations

from tcod.event import KeySym

from pyrl.types.keys import Key

key_map: dict[int, str] = {
    KeySym.BACKSPACE: Key.BACKSPACE,
    KeySym.DELETE:    Key.DELETE,
    KeySym.DOWN:      Key.DOWN,
    KeySym.END:       Key.END,
    KeySym.ESCAPE:    Key.ESC,
    KeySym.F10:       Key.F10,
    KeySym.F11:       Key.F11,
    KeySym.F12:       Key.F12,
    KeySym.F1:        Key.F1,
    KeySym.F2:        Key.F2,
    KeySym.F3:        Key.F3,
    KeySym.F4:        Key.F4,
    KeySym.F5:        Key.F5,
    KeySym.F6:        Key.F6,
    KeySym.F7:        Key.F7,
    KeySym.F8:        Key.F8,
    KeySym.F9:        Key.F9,
    KeySym.HOME:      Key.HOME,
    KeySym.INSERT:    Key.INSERT,
    KeySym.LEFT:      Key.LEFT,
    KeySym.N0:        Key.NUMPAD_0,
    KeySym.N1:        Key.NUMPAD_1,
    KeySym.N2:        Key.NUMPAD_2,
    KeySym.N3:        Key.NUMPAD_3,
    KeySym.N4:        Key.NUMPAD_4,
    KeySym.N5:        Key.NUMPAD_5,
    KeySym.N6:        Key.NUMPAD_6,
    KeySym.N7:        Key.NUMPAD_7,
    KeySym.N8:        Key.NUMPAD_8,
    KeySym.N9:        Key.NUMPAD_9,
    KeySym.PAGEDOWN:  Key.PAGE_DOWN,
    KeySym.PAGEUP:    Key.PAGE_UP,
    KeySym.RETURN2:   Key.ENTER,
    KeySym.RETURN:    Key.ENTER,
    KeySym.RIGHT:     Key.RIGHT,
    KeySym.SPACE:     Key.SPACE,
    KeySym.TAB:       Key.TAB,
    KeySym.UNKNOWN:   Key.NO_INPUT,
    KeySym.UP:        Key.UP,
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
