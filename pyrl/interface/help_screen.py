from pyrl.binds import Binds


def help_screen(io):
    header = "Help Screen, ^ means ctrl, ! means alt"
    section = "{!s:16.16}"*2
    help_lines = (
        ("{:32}"*2).format("Main View:", "General"),
        "",
        (section * 3).format("Help", Binds.Help, "Show vision", Binds.Show_Vision, "Cancel", Binds.Cancel),
        (section * 1).format("Look Mode", Binds.Look_Mode),
        (section * 1).format("Inventory", Binds.Equipment),
        (section * 1).format("Descend", Binds.Descend),
        (section * 1).format("Ascend", Binds.Ascend),
        (section * 1).format("Quit", Binds.Quit),
        (section * 1).format("Save", Binds.Save),
        (section * 1).format("Manual Attack", Binds.Attack),
        (section * 1).format("Redraw Screen", Binds.Redraw),
        (section * 1).format("Print History", Binds.History),
        (section * 1).format("Walk Mode", Binds.Walk_Mode),
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
    footer = "{0} to close".format(Binds.Cancel.key)
    io.menu(header, help_lines, footer, Binds.Cancel)


def scroll_views_help_screen(io):
    header = "Help Screen, ^ means ctrl, ! means alt"
    section = "{!s:16.16}"*2
    help_lines = (
        ("{:32}"*2).format("Main View:", "General"),
        "",
        (section * 3).format("Help", Binds.Help, "Show vision", Binds.Show_Vision, "Cancel", Binds.Cancel),
        (section * 1).format("Look Mode", Binds.Look_Mode),
        (section * 1).format("Inventory", Binds.Equipment),
        (section * 1).format("Descend", Binds.Descend),
        (section * 1).format("Ascend", Binds.Ascend),
        (section * 1).format("Quit", Binds.Quit),
        (section * 1).format("Save", Binds.Save),
        (section * 1).format("Manual Attack", Binds.Attack),
        (section * 1).format("Redraw Screen", Binds.Redraw),
        (section * 1).format("Print History", Binds.History),
        (section * 1).format("Walk Mode", Binds.Walk_Mode),
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
    footer = "{0} to close".format(Binds.Cancel.key)
    io.menu(header, help_lines, footer, Binds.Cancel)
