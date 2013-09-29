import code
from pyrl import debug

import const.keys as KEY
import const.directions as DIR
import const.game as GAME
import const.colors as COLOR
import const.generated_level_types as LEVEL_TYPE
from pyrl import mappings as MAPPING

from pyrl.main import io
from pyrl.world_file import LevelNotFound
from pyrl.generic_algorithms import add_vector

from inventory import equipment
from walk_mode import walk_mode, walk_mode_init

class UserInput(object):
    def __init__(self):
        self.walk_mode_data = None
        no_args, no_kwds = (), {}
        self.actions = {
            KEY.CLOSE_WINDOW:   (endgame, no_args, no_kwds),
            MAPPING.ASCEND:     (enter, (GAME.PASSAGE_UP, ), no_kwds),
            MAPPING.DESCEND:    (enter, (GAME.PASSAGE_DOWN, ), no_kwds),
            MAPPING.QUIT:       (endgame, no_args, no_kwds),
            MAPPING.SAVE:       (savegame, no_args, no_kwds),
            MAPPING.ATTACK:     (attack, no_args, no_kwds),
            MAPPING.REDRAW:     (redraw, no_args, no_kwds),
            MAPPING.HISTORY:    (print_history, no_args, no_kwds),
            MAPPING.WALK_MODE:  (walk_mode_init, (self, ), no_kwds),
            MAPPING.LOOK_MODE:  (look, no_args, no_kwds),
            MAPPING.INVENTORY:  (equipment, no_args, no_kwds),
            MAPPING.HELP:       (help_screen, no_args, no_kwds),

            'd':  (debug_action, (self, ), no_kwds),
            '+':  (sight_change, (1, ), no_kwds),
            '-':  (sight_change, (-1, ), no_kwds),
        }
        for key, value in MAPPING.DIRECTIONS.viewitems():
            self.actions[key] = (act_to_dir, (value, ), no_kwds)
        for key, value in MAPPING.INSTANT_WALK_MODE.viewitems():
            self.actions[key] = (walk_mode_init, (self, value), no_kwds)

    def get_user_input_and_act(self, game, creature):
        while creature.can_act():
            if self.walk_mode_data is not None:
                walk_mode(game, creature, self)
            else:
                key = io.get_key()
                if key in self.actions:
                    function, args, keywords = self.actions[key]
                    if function(game, creature, *args, **keywords):
                        return
                else:
                    io.msg("Undefined key: {}".format(key))

def act_to_dir(game, creature, direction):
    target_coord = add_vector(creature.coord, direction)
    level = creature.level
    if level.creature_can_move(creature, direction):
        game.creature_move(creature, direction)
    elif level.has_creature(target_coord):
        game.creature_attack(creature, direction)
    elif not creature.can_act():
        io.msg("You're out of energy.")
    else:
        io.msg("You can't move there.")

def look(game, creature):
    coord = creature.coord
    level = creature.level
    drawline_flag = False
    direction = DIR.STOP
    while True:
        new_coord = add_vector(coord, direction)
        if level.legal_coord(new_coord):
            coord = new_coord
        io.msg(level.look_information(coord))
        if drawline_flag:
            io.draw_line(creature.coord, coord, ("*", COLOR.YELLOW))
            io.draw_line(coord, creature.coord, ("*", COLOR.YELLOW))
            io.msg("LoS: {}".format(level.check_los(creature.coord, coord)))
        if coord != creature.coord:
            char = level._get_visible_char(coord)
            char = char[0], (COLOR.BASE_BLACK, COLOR.BASE_GREEN)
            io.draw_char(coord, char)
            io.draw_char(creature.coord, level._get_visible_char(creature.coord), reverse=True)
        c = io.get_key()
        game.redraw()
        direction = DIR.STOP
        if c in MAPPING.DIRECTIONS:
            direction = MAPPING.DIRECTIONS[c]
        elif c == 'd':
            drawline_flag = not drawline_flag
        elif c == 'b':
            from generic_algorithms import bresenham
            for coord in bresenham(level.get_coord(creature.coord), coord):
                io.msg(coord)
        elif c == 's':
            if level.has_creature(coord):
                game.register_status_texts(level.get_creature(coord))
        elif c in MAPPING.GROUP_CANCEL or c == MAPPING.LOOK_MODE:
            break

def endgame(game, creature, *a, **k):
    game.endgame(*a, **k)

def savegame(game, creature, *a, **k):
    game.savegame(*a, **k)

def attack(game, creature):
    key = io.ask("Specify attack direction, {} to abort".format(MAPPING.CANCEL), MAPPING.DIRECTIONS.viewkeys() | MAPPING.GROUP_CANCEL)
    if key in MAPPING.DIRECTIONS:
        game.creature_attack(creature, MAPPING.DIRECTIONS[key])

def redraw(game, creature):
    game.redraw()

def enter(game, creature, passage):
    coord = game.player.coord
    level = creature.level
    if level.is_exit(coord) and level.get_exit(coord) == passage:
        try:
            game.creature_enter_passage(creature, level.world_loc, level.get_exit(coord))
        except LevelNotFound:
            io.msg("This passage doesn't seem to lead anywhere.")
    else:
        try:
            new_coord = level.get_passage_coord(passage)
        except KeyError:
            io.msg("This level doesn't seem to have a corresponding passage.")
        else:
            if not level.is_passable(new_coord):
                level.remove_creature(level.get_creature(new_coord))
            if not game.creature_teleport(creature, new_coord):
                io.msg("Teleport failed.")

def sight_change(game, creature, amount):
    from const.slots import BODY
    from const.stats import SIGHT
    creature.get_item(BODY).stats[SIGHT] += amount
    return True

def print_history(game, creature):
    io.m.print_history()

def debug_action(game, creature, userinput):
    level = creature.level
    c = io.get_key("Avail cmds: vclbdhkpors+-")
    if c == 'v':
        debug.show_map = not debug.show_map
        game.redraw()
        io.msg("Show map set to {}".format(debug.show_map))
    elif c == 'r':
        debug.cross = not debug.cross
        io.msg("Path heuristic cross set to {}".format(debug.cross))
    elif c == 'l':
        GAME.LEVEL_TYPE = LEVEL_TYPE.ARENA if GAME.LEVEL_TYPE == LEVEL_TYPE.DUNGEON else LEVEL_TYPE.DUNGEON
        io.msg("Level type set to {}".format(GAME.LEVEL_TYPE))
    elif c == 'd':
        if not debug.path:
            debug.path = True
            io.msg("Path debug set")
        elif not debug.path_step:
            debug.path_step = True
            io.msg("Path debug and stepping set")
        else:
            debug.path = False
            debug.path_step = False
            io.msg("Path debug unset")
    elif c == 'h':
        debug.reverse = not debug.reverse
        game.redraw()
        io.msg("Reverse set to {}".format(debug.reverse))
    elif c == 'k':
        creature_list = level.creatures.values()
        creature_list.remove(creature)
        for i in creature_list:
            level.remove_creature(i)
        io.msg("Abrakadabra.")
        return True
    elif c == 'o':
        passage_down = level.get_passage_coord(GAME.PASSAGE_DOWN)
        io.draw_path(level.path(creature.coord, passage_down))
        game.redraw()
    elif c == 'p':
        passage_up = level.get_passage_coord(GAME.PASSAGE_UP)
        passage_down = level.get_passage_coord(GAME.PASSAGE_DOWN)
        io.draw_path(level.path(passage_up, passage_down))
        game.redraw()
    elif c == 'i':
        io.suspend()
        code.interact(local=locals())
        io.resume()
    elif c == 'c':
        import curses
        io.msg(curses.COLORS, curses.COLOR_PAIRS, curses.can_change_color())
        io.msg(curses.A_ALTCHARSET, curses.A_BLINK, curses.A_BOLD, curses.A_DIM, curses.A_NORMAL,
                curses.A_REVERSE, curses.A_STANDOUT, curses.A_UNDERLINE)
    elif c == 'm':
        io.msg(debug.debug_string)
    else:
        io.msg("Undefined debug key: {}".format(chr(c) if 0 < c < 128 else c))

def help_screen(game, creature):
    header = "Help Screen, ^ means ctrl, ! means alt"
    help_lines = [
        "Help           {0}".format(MAPPING.HELP),
        "Look Mode      {0}".format(MAPPING.LOOK_MODE),
        "Inventory      {0}".format(MAPPING.INVENTORY),
        "Descend        {0}".format(MAPPING.DESCEND),
        "Ascend         {0}".format(MAPPING.ASCEND),
        "Quit           {0}".format(MAPPING.QUIT),
        "Save           {0}".format(MAPPING.SAVE),
        "Manual Attack  {0}".format(MAPPING.ATTACK),
        "Redraw Screen  {0}".format(MAPPING.REDRAW),
        "Print History  {0}".format(MAPPING.HISTORY),
        "Walk Mode      {0}".format(MAPPING.WALK_MODE),
        "",
        "Direction keys used for movement, implicit attacking, walk mode, et cetera:",
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
    footer = "{0} to close".format(MAPPING.CANCEL)
    io.menu(header, help_lines, footer, MAPPING.GROUP_CANCEL)
    game.redraw()
