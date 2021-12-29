from __future__ import annotations

try:
    import curses
except ImportError:
    import sys
    print("Couldn't import curses. Try running with sdl output.")
    sys.exit(1)

WideChar = int | str
IMPLEMENTATION = "curses"

def clean_curses() -> None:
    """Resume normal shell state. Does nothing if curses wasn't initialized."""
    try:
        curses.reset_shell_mode()
    except curses.error:
        pass
    try:
        curses.endwin()
    except curses.error:
        pass
