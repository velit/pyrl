from __future__ import absolute_import, division, print_function, unicode_literals

from config.mappings import Mapping


def help_screen(io):
    header = "Help Screen, ^ means ctrl, ! means alt"
    help_lines = [
        "Help           {0}".format(Mapping.Help),
        "Look Mode      {0}".format(Mapping.Look_Mode),
        "Inventory      {0}".format(Mapping.Inventory),
        "Descend        {0}".format(Mapping.Descend),
        "Ascend         {0}".format(Mapping.Ascend),
        "Quit           {0}".format(Mapping.Quit),
        "Save           {0}".format(Mapping.Save),
        "Manual Attack  {0}".format(Mapping.Attack),
        "Redraw Screen  {0}".format(Mapping.Redraw),
        "Print History  {0}".format(Mapping.History),
        "Walk Mode      {0}".format(Mapping.Walk_Mode),
        "",
        "Direction keys used for movement, implicit attacking, walk mode, etc:",
        "  Numpad keys",
        "  So called vi-keys (hjklyubn.)",
        "",
        "Debug keys that start with d",
        "Map hax             dv        Other path                   dp",
        "Kill monsters       dk        Reverse fov                  dh",
        "Path to stairs      do        Interactive console          di",
        "Toggle path debugs  dd        Change level types           dl",
        "Print debug string  dm        Set cross heuristic in path  dr",
        "",
        "Colors available     dc (only on ncurses ie. pyrl.py)",
    ]
    footer = "{0} to close".format(Mapping.Cancel)
    io.menu(header, help_lines, footer, Mapping.Group_Cancel)
