from pyrl.binds import Binds

def help_view(io):
    header = "Help Screen, ^ means ctrl, ! means alt"
    help_lines = (
        f"Help            {Binds.Help!s:16.16}"      f"Walk Mode       {Binds.Walk_Mode!s:16.16}",
        f"Cancel          {Binds.Cancel!s:16.16}"    f"Look Mode       {Binds.Look_Mode!s:16.16}",
        f"Save            {Binds.Save!s:16.16}"      f"Show vision     {Binds.Show_Vision!s:16.16}",
        f"Quit            {Binds.Quit!s:16.16}"      f"Manual Attack   {Binds.Attack!s:16.16}",
        f"Equipment       {Binds.Equipment!s:16.16}" f"Redraw Screen   {Binds.Redraw!s:16.16}",
        f"Descend         {Binds.Descend!s:16.16}"   f"Print History   {Binds.History!s:16.16}",
        f"Ascend          {Binds.Ascend!s:16.16}",
        f"",
        f"Direction keys used for movement, implicit attacking, walk mode, etc:",
        f"  Numpad keys",
        f"  So called vi-keys (hjklyubn.)",
        f"",
        f"Debug keys that start with d",
        f"Map hax             dv        Other path                   dp",
        f"Kill monsters       dk        Reverse fov                  dh",
        f"Path to stairs      do        Interactive console          di",
        f"Toggle path debugs  dd        Change level types           dl",
        f"Print debug string  dm        Set cross heuristic in path  dr",
        f"",
        f"Colors available     dc (only on ncurses ie. pyrl.py)",
    )
    footer = f"{Binds.Cancel.key} to close"
    io.menu(header, help_lines, footer, Binds.Cancel)
