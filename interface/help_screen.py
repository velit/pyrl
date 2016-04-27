from __future__ import absolute_import, division, print_function, unicode_literals

from bindings import Bind


def help_screen(io):
    header = "Help Screen, ^ means ctrl, ! means alt"
    section = "{!s:16.16}"*2
    help_lines = (
        ("{:32}"*2).format("Main View:", "General"),
        "",
        (section * 3).format("Help",           Bind.Help,        "Show vision",  Bind.Show_Vision,  "Cancel",  Bind.Cancel),
        (section * 1).format("Look Mode",      Bind.Look_Mode),
        (section * 1).format("Inventory",      Bind.Equipment),
        (section * 1).format("Descend",        Bind.Descend),
        (section * 1).format("Ascend",         Bind.Ascend),
        (section * 1).format("Quit",           Bind.Quit),
        (section * 1).format("Save",           Bind.Save),
        (section * 1).format("Manual Attack",  Bind.Attack),
        (section * 1).format("Redraw Screen",  Bind.Redraw),
        (section * 1).format("Print History",  Bind.History),
        (section * 1).format("Walk Mode",      Bind.Walk_Mode),
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
    )
    footer = "{0} to close".format(Bind.Cancel.key)
    io.menu(header, help_lines, footer, Bind.Cancel)


def scroll_views_help_screen(io):
    header = "Help Screen, ^ means ctrl, ! means alt"
    section = "{!s:16.16}"*2
    help_lines = (
        ("{:32}"*2).format("Main View:", "General"),
        "",
        (section * 3).format("Help",           Bind.Help,        "Show vision",  Bind.Show_Vision,  "Cancel",  Bind.Cancel),
        (section * 1).format("Look Mode",      Bind.Look_Mode),
        (section * 1).format("Inventory",      Bind.Equipment),
        (section * 1).format("Descend",        Bind.Descend),
        (section * 1).format("Ascend",         Bind.Ascend),
        (section * 1).format("Quit",           Bind.Quit),
        (section * 1).format("Save",           Bind.Save),
        (section * 1).format("Manual Attack",  Bind.Attack),
        (section * 1).format("Redraw Screen",  Bind.Redraw),
        (section * 1).format("Print History",  Bind.History),
        (section * 1).format("Walk Mode",      Bind.Walk_Mode),
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
    )
    footer = "{0} to close".format(Bind.Cancel.key)
    io.menu(header, help_lines, footer, Bind.Cancel)
