from __future__ import annotations

try:
    import curses
except ImportError:
    import sys
    print("Couldn't import curses. Try running sdlpyrl.py")
    sys.exit(1)

IMPLEMENTATION = "curses"
WideChar = int | str

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
