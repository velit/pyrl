from __future__ import annotations

from pyrl.config.binds import Binds
from pyrl.engine.enums.glyphs import Colors
from pyrl.ui.views.line import from_multiline_str
from pyrl.ui.window.window_system import WindowSystem

raw_help_lines = f"""
Help            {Binds.Help!s:16.16}"      f"Walk Mode       {Binds.Walk_Mode!s:16.16}
Cancel          {Binds.Cancel!s:16.16}"    f"Look Mode       {Binds.Look_Mode!s:16.16}
Save            {Binds.Save!s:16.16}"      f"Show vision     {Binds.Show_Vision!s:16.16}
Quit            {Binds.Quit!s:16.16}"      f"Manual Attack   {Binds.Attack!s:16.16}
Equipment       {Binds.Equipment!s:16.16}" f"Redraw Screen   {Binds.Redraw!s:16.16}
Descend         {Binds.Descend!s:16.16}"   f"Print History   {Binds.History!s:16.16}
Ascend          {Binds.Ascend!s:16.16}

Direction keys used for movement, implicit attacking, walk mode, etc:
  Numpad keys
  So called vi-keys (hjklyubn.)

Debug keys that start with d
Map hax             dv        Other path                   dp
Kill monsters       dk        Reverse fov                  dh
Path to stairs      do        Interactive console          di
Toggle path debugs  dd        Change level types           dl
Print debug string  dm        Set cross heuristic in path  dr

Colors available     dc (only on ncurses ie. pyrl.py)
"""[1:-1]
help_lines = from_multiline_str(raw_help_lines, color=Colors.Normal)

def help_view(io: WindowSystem) -> None:
    header = "Help Screen, ^ means ctrl, ! means alt"
    footer = f"{Binds.Cancel.key} to close"
    io.menu(header, help_lines, footer, Binds.Cancel)
