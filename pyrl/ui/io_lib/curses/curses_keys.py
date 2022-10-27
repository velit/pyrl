from __future__ import annotations

import sys

from pyrl.engine.types.keys import Key

if sys.platform != "win32":
    import curses.ascii

    from pyrl.ui.io_lib.curses import WideChar

    curses_key_map: dict[WideChar, str] = {
        chr(curses.ascii.CR):  Key.ENTER,
        chr(curses.ascii.ESC): Key.ESC,
        chr(curses.ascii.SP):  Key.SPACE,
        chr(curses.ascii.TAB): Key.TAB,
        curses.ERR:            Key.NO_INPUT,
        curses.KEY_A1:         Key.NUMPAD_7,
        curses.KEY_A3:         Key.NUMPAD_9,
        curses.KEY_B2:         Key.NUMPAD_5,
        curses.KEY_BACKSPACE:  Key.BACKSPACE,
        curses.KEY_BTAB:       Key.SHIFT_TAB,
        curses.KEY_C1:         Key.NUMPAD_1,
        curses.KEY_C3:         Key.NUMPAD_3,
        curses.KEY_DC:         Key.DELETE,
        curses.KEY_DOWN:       Key.DOWN,
        curses.KEY_END:        Key.END,
        curses.KEY_F1:         Key.F1,
        curses.KEY_F2:         Key.F2,
        curses.KEY_F3:         Key.F3,
        curses.KEY_F4:         Key.F4,
        curses.KEY_F5:         Key.F5,
        curses.KEY_F6:         Key.F6,
        curses.KEY_F7:         Key.F7,
        curses.KEY_F8:         Key.F8,
        curses.KEY_F9:         Key.F9,
        curses.KEY_F10:        Key.F10,
        curses.KEY_F11:        Key.F11,
        curses.KEY_F12:        Key.F12,
        curses.KEY_FIND:       Key.NUMPAD_7,
        curses.KEY_HOME:       Key.HOME,
        curses.KEY_IC:         Key.INSERT,
        curses.KEY_LEFT:       Key.LEFT,
        curses.KEY_NPAGE:      Key.PAGE_DOWN,
        curses.KEY_PPAGE:      Key.PAGE_UP,
        curses.KEY_RESIZE:     Key.WINDOW_RESIZE,
        curses.KEY_RIGHT:      Key.RIGHT,
        curses.KEY_SELECT:     Key.NUMPAD_1,
        curses.KEY_UP:         Key.UP,
    }
