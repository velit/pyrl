from __future__ import annotations

import sys

from pyrl.types.keys import Keys

if sys.platform != "win32":
    import curses.ascii

    from pyrl.io_wrappers.curses import WideChar

    curses_key_map: dict[WideChar, str] = {
        chr(curses.ascii.CR):  Keys.ENTER,
        chr(curses.ascii.ESC): Keys.ESC,
        chr(curses.ascii.SP):  Keys.SPACE,
        chr(curses.ascii.TAB): Keys.TAB,
        curses.ERR:            Keys.NO_INPUT,
        curses.KEY_A1:         Keys.NUMPAD_7,
        curses.KEY_A3:         Keys.NUMPAD_9,
        curses.KEY_B2:         Keys.NUMPAD_5,
        curses.KEY_BACKSPACE:  Keys.BACKSPACE,
        curses.KEY_BTAB:       Keys.SHIFT_TAB,
        curses.KEY_C1:         Keys.NUMPAD_1,
        curses.KEY_C3:         Keys.NUMPAD_3,
        curses.KEY_DC:         Keys.DELETE,
        curses.KEY_DOWN:       Keys.DOWN,
        curses.KEY_END:        Keys.END,
        curses.KEY_F1:         Keys.F1,
        curses.KEY_F2:         Keys.F2,
        curses.KEY_F3:         Keys.F3,
        curses.KEY_F4:         Keys.F4,
        curses.KEY_F5:         Keys.F5,
        curses.KEY_F6:         Keys.F6,
        curses.KEY_F7:         Keys.F7,
        curses.KEY_F8:         Keys.F8,
        curses.KEY_F9:         Keys.F9,
        curses.KEY_F10:        Keys.F10,
        curses.KEY_F11:        Keys.F11,
        curses.KEY_F12:        Keys.F12,
        curses.KEY_FIND:       Keys.NUMPAD_7,
        curses.KEY_HOME:       Keys.HOME,
        curses.KEY_IC:         Keys.INSERT,
        curses.KEY_LEFT:       Keys.LEFT,
        curses.KEY_NPAGE:      Keys.PAGE_DOWN,
        curses.KEY_PPAGE:      Keys.PAGE_UP,
        curses.KEY_RESIZE:     Keys.WINDOW_RESIZE,
        curses.KEY_RIGHT:      Keys.RIGHT,
        curses.KEY_SELECT:     Keys.NUMPAD_1,
        curses.KEY_UP:         Keys.UP,
    }
