from __future__ import absolute_import, division, print_function, unicode_literals

import code
from config.debug import Debug
from level_template import LevelTemplate
from rdg import GenLevelType
from enums.level_locations import LevelLocation


def debug_action(io, game_actions):
    creature = game_actions.creature
    level = creature.level

    def show_map():
        Debug.show_map = not Debug.show_map
        game_actions.redraw()
        io.msg("Show map set to {}".format(Debug.show_map))

    def toggle_path_heuristic_cross():
        Debug.cross = not Debug.cross
        io.msg("Path heuristic cross set to {}".format(Debug.cross))

    def cycle_level_type():
        if LevelTemplate.default_level_type == GenLevelType.Dungeon:
            LevelTemplate.default_level_type = GenLevelType.Arena
        else:
            LevelTemplate.default_level_type = GenLevelType.Dungeon
        io.msg("Level type set to {}".format(LevelTemplate.default_level_type))

    def show_path_debug():
        if not Debug.path:
            Debug.path = True
            io.msg("Path debug set")
        elif not Debug.path_step:
            Debug.path_step = True
            io.msg("Path debug and stepping set")
        else:
            Debug.path = False
            Debug.path_step = False
            io.msg("Path debug unset")

    def show_fov_debug():
        Debug.reverse = not Debug.reverse
        game_actions.redraw()
        io.msg("Reverse set to {}".format(Debug.reverse))

    def kill_creatures_in_level():
        creature_list = list(level.creatures.values())
        creature_list.remove(creature)
        for i in creature_list:
            level.remove_creature(i)
        io.msg("Abrakadabra.")

    def draw_path_to_passage_down():
        passage_down = level.get_passage_coord(LevelLocation.Passage_Down)
        io.draw_path(level.path(creature.coord, passage_down))
        game_actions.redraw()

    def draw_path_from_up_to_down():
        passage_up = level.get_passage_coord(LevelLocation.Passage_Up)
        passage_down = level.get_passage_coord(LevelLocation.Passage_Down)
        io.draw_path(level.path(passage_up, passage_down))
        game_actions.redraw()

    def interactive_console():
        io.suspend()
        code.interact(local=locals())
        io.resume()

    def toggle_log_keycodes():
        Debug.show_keycodes = not Debug.show_keycodes
        io.msg("Input code debug set to {}".format(Debug.show_keycodes))

    def display_curses_color_info():
        import curses
        io.msg(curses.COLORS, curses.COLOR_PAIRS, curses.can_change_color())
        io.msg(curses.A_ALTCHARSET, curses.A_BLINK, curses.A_BOLD, curses.A_DIM, curses.A_NORMAL,
            curses.A_REVERSE, curses.A_STANDOUT, curses.A_UNDERLINE)

    def print_message_debug_string():
        io.msg(Debug.debug_string)

    debug_actions = {
        'v': show_map,
        'r': toggle_path_heuristic_cross,
        'l': cycle_level_type,
        'd': show_path_debug,
        'h': show_fov_debug,
        'k': kill_creatures_in_level,
        'o': draw_path_to_passage_down,
        'p': draw_path_from_up_to_down,
        'i': interactive_console,
        'y': toggle_log_keycodes,
        'c': display_curses_color_info,
        'm': print_message_debug_string,
    }
    c = io.get_key("Avail cmds: " + "".join(sorted(debug_actions.keys())))

    if c in debug_actions:
        debug_actions[c]()
    else:
        io.msg("Undefined debug key: {}".format(c))
