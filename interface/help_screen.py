from __future__ import absolute_import, division, print_function, unicode_literals

from config.bindings import Bind


def help_screen(io):
    header = "Help Screen, ^ means ctrl, ! means alt"
    columns = \
    (
        (
            "{:32}".format("Main View:"),
            "",
            "Help            {0!s:16.16}".format(Bind.Help),
            "Look Mode       {0!s:16.16}".format(Bind.Look_Mode),
            "Inventory       {0!s:16.16}".format(Bind.Inventory),
            "Descend         {0!s:16.16}".format(Bind.Descend),
            "Ascend          {0!s:16.16}".format(Bind.Ascend),
            "Quit            {0!s:16.16}".format(Bind.Quit),
            "Save            {0!s:16.16}".format(Bind.Save),
            "Manual Attack   {0!s:16.16}".format(Bind.Attack),
            "Redraw Screen   {0!s:16.16}".format(Bind.Redraw),
            "Print History   {0!s:16.16}".format(Bind.History),
            "Walk Mode       {0!s:16.16}".format(Bind.Walk_Mode),
        ),
        (
            "",
            "",
            "Show vision     {0!s:16.16}".format(Bind.Show_Vision),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
        ),
        (
            "General:",
            "",
            "Cancel          {0!s:16.16}".format(Bind.Cancel),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
            "                {0!s:16.16}".format(""),
        ),
    )
    top = tuple("".join(row) for row in zip(*columns))
    bottom = (
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
    help_lines = top + bottom
    footer = "{0} to close".format(Bind.Cancel.key)
    io.menu(header, help_lines, footer, Bind.Cancel)
