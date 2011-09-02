import curses
import sys
import const.directions as DIRS
import const.game as CG
import const.debug as D

from pio import io
from char import Char

direction_keys = {
	curses.KEY_DOWN: DIRS.SO,
	curses.KEY_LEFT: DIRS.WE,
	curses.KEY_RIGHT: DIRS.EA,
	curses.KEY_UP: DIRS.NO,
	ord('.'): DIRS.STOP,
	ord('1'): DIRS.SW,
	ord('2'): DIRS.SO,
	ord('3'): DIRS.SE,
	ord('4'): DIRS.WE,
	ord('5'): DIRS.STOP,
	ord('6'): DIRS.EA,
	ord('7'): DIRS.NW,
	ord('8'): DIRS.NO,
	ord('9'): DIRS.NE,
	ord('h'): DIRS.WE,
	ord('i'): DIRS.NE,
	ord('j'): DIRS.SO,
	ord('k'): DIRS.NO,
	ord('l'): DIRS.EA,
	ord('m'): DIRS.SE,
	ord('n'): DIRS.SW,
	ord('u'): DIRS.NW,
	}

class UserInput:
	def __init__(self):
		no_args, no_kwds = (), {}
		self.actions = {
			ord('<'): ("enter", (CG.PASSAGE_UP, ), no_kwds),
			ord('>'): ("enter", (CG.PASSAGE_DOWN, ), no_kwds),
			ord('Q'): ("endgame", no_args, no_kwds),
			ord('S'): ("savegame", no_args, no_kwds),
			ord('d'): ("debug", no_args, no_kwds),
			ord('L'): ("look", no_args, no_kwds),
			ord('Z'): ("z_command", no_args, no_kwds),
			ord('\x12'): ("redraw_view", no_args, no_kwds),
		}
		for key, value in direction_keys.items():
			self.actions[key] = ("act_to_dir", (value, ), no_kwds)

	def get_and_act(self, game, level, creature):
		c = io.getch(*level.get_coord(creature.loc))
		if c in self.actions:
			return self.execute_action(game, level, creature, self.actions[c])
		else:
			io.msg("Undefined key: {}".format(chr(c) if 0 < c < 256 else c))

	def execute_action(self, game, level, creature, act):
		function, args, keywords = act
		return getattr(sys.modules[__name__], function)(game, level, creature, *args, **keywords)

def act_to_dir(game, level, creature, direction):
	if direction == DIRS.STOP:
		return True
	target_loc = level.get_relative_loc(creature.loc, direction)
	if level.move_creature(creature, target_loc):
		return True
	elif level.has_creature(target_loc):
		target = level.get_creature(target_loc)
		game.creature_attack(level, creature, target)
		return True
	else:
		io.msg("You can't move there.")
		return False

def z_command(game, level, creature):
	c = io.getch()
	if c == ord('Q'):
		game.endgame(ask=False)
	elif c == ord('Z'):
		game.savegame(ask=False)

def look(game, level, creature):
	loc = creature.loc
	drawline_flag = False
	direction = DIRS.STOP
	while True:
		loc = level.get_relative_loc(loc, direction)
		io.msg(level.look_information(loc))
		if drawline_flag:
			io.drawline(level.get_coord(creature.loc), level.get_coord(loc), Char("*", "yellow"))
			io.msg("LoS: {}".format(level.check_los(creature.loc, loc)))
		c = io.getch(*level.get_coord(loc))
		game.redraw()
		direction = DIRS.STOP
		if c in direction_keys:
			direction = direction_keys[c]
		elif c == ord('d'):
			drawline_flag = not drawline_flag
		elif c in map(ord, "QqzZ "):
			break

def endgame(game, level, creature, *a, **k):
	game.endgame(*a, **k)

def savegame(game, level, creature, *a, **k):
	game.savegame(*a, **k)

def debug(game, level, creature):
	c = io.getch_print("Avail cmds: vclbdhkp")
	if c == ord('v'):
		game.flags.show_map = not game.flags.show_map
		game.redraw()
		io.msg("Show map set to {}".format(game.flags.show_map))
	elif c == ord('c'):
		D.CROSS = not D.CROSS
		io.msg("Path heuristic cross set to {}".format(D.CROSS))
	elif c == ord('l'):
		CG.LEVEL_TYPE = "arena" if CG.LEVEL_TYPE == "dungeon" else "dungeon"
		io.msg("Level type set to {}".format(CG.LEVEL_TYPE))
	elif c == ord('b'):
		io.draw_block((4,4))
	elif c == ord('d'):
		D.PATH = not D.PATH
		io.msg("Path debug set to {}".format(D.PATH))
	elif c == ord('h'):
		game.flags.reverse = not game.flags.reverse
		game.redraw()
		io.msg("Reverse set to {}".format(game.flags.reverse))
	elif c == ord('k'):
		creature_list = list(level.creatures.values())
		creature_list.remove(creature)
		for i in creature_list:
			level.remove_creature(i)
		io.msg("Abrakadabra.")
	elif c == ord('p'):
		passage_up = level.get_passage_loc(CG.PASSAGE_UP)
		passage_down = level.get_passage_loc(CG.PASSAGE_DOWN)
		io.draw_path((loc // level.cols, loc % level.cols) for loc in level.path(passage_up, passage_down))
	else:
		io.msg("Undefined debug key: {}".format(chr(c) if 0 < c < 256 else c))

def redraw_view(game, level, creature):
	game.redraw()

def enter(game, level, creature, passage):
	loc = game.player.loc
	if level.is_exit(loc) and level.get_exit(loc) == passage:
		try:
			game.enter_passage(level.world_loc, level.get_exit(loc))
		except CG.PyrlException:
			io.msg("This passage doesn't seem to lead anywhere.")
	else:
		try:
			new_loc = level.get_passage_loc(passage)
		except KeyError:
			io.msg("This level doesn't seem to have a corresponding passage.")
		else:
			if not level.is_passable(new_loc):
				level.remove_creature(level.get_creature(new_loc))
			level.move_creature(game.player, new_loc)
	return True
