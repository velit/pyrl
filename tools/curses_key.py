#!/usr/bin/env python3
from __future__ import annotations

import curses
from curses import ascii

_MSG = "Press key to test, Q to quit."

def main(w: curses.window) -> None:
    curses.raw()
    curses.meta(True)
    w.keypad(True)

    key = None
    w.addstr(_MSG)
    while key != 'Q':
        key, alt = get_key(w)
        w.clear()
        print_key(w, key, alt)

    curses.endwin()

def print_key(w: curses.window, key: str | int, alt: bool) -> None:
    if isinstance(key, str):
        nr = ord(key)
        w.addstr(0, 0, _MSG)

        if nr < 128:
            w.addstr(1, 0, str((nr, alt * "!" + curses.keyname(ord(key)).decode(), alt)))
            w.addstr(2, 0, str((nr, alt * "!" + ascii.unctrl(key), alt)))
        else:
            w.addstr(1, 0, str((nr, alt * "!" + key, alt)))
    else:
        w.addstr(0, 0, _MSG)
        w.addstr(1, 0, str((key, alt * "!" + curses.keyname(key).decode(), alt)))

def get_key(w: curses.window) -> tuple[str | int, bool]:
    alt = False
    key = w.get_wch()
    if key == chr(ascii.ESC):
        w.nodelay(True)
        try:
            second_key = w.get_wch()
        except curses.error:
            pass
        else:
            key = second_key
            alt = True
        finally:
            w.nodelay(False)

    return key, alt

if __name__ == '__main__':
    curses.wrapper(main)
