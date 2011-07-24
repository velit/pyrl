import curses
import sys
import const.directions as dirs

from pio import io
from const.game import PASSAGE_UP, PASSAGE_DOWN, PyrlException

class UserInput:
	def __init__(self):
		no_args, no_kwds = (), {}
		self.actions = {
			curses.KEY_DOWN: ("act_to_dir", (dirs.SO, ), no_kwds),
			curses.KEY_LEFT: ("act_to_dir", (dirs.WE, ), no_kwds),
			curses.KEY_RIGHT: ("act_to_dir", (dirs.EA, ), no_kwds),
			curses.KEY_UP: ("act_to_dir", (dirs.NO, ), no_kwds),
			ord('.'): ("act_to_dir", (dirs.STOP, ), no_kwds),
			ord('1'): ("act_to_dir", (dirs.SW, ), no_kwds),
			ord('2'): ("act_to_dir", (dirs.SO, ), no_kwds),
			ord('3'): ("act_to_dir", (dirs.SE, ), no_kwds),
			ord('4'): ("act_to_dir", (dirs.WE, ), no_kwds),
			ord('5'): ("act_to_dir", (dirs.STOP, ), no_kwds),
			ord('6'): ("act_to_dir", (dirs.EA, ), no_kwds),
			ord('7'): ("act_to_dir", (dirs.NW, ), no_kwds),
			ord('8'): ("act_to_dir", (dirs.NO, ), no_kwds),
			ord('9'): ("act_to_dir", (dirs.NE, ), no_kwds),
			ord('h'): ("act_to_dir", (dirs.WE, ), no_kwds),
			ord('i'): ("act_to_dir", (dirs.NE, ), no_kwds),
			ord('j'): ("act_to_dir", (dirs.SO, ), no_kwds),
			ord('k'): ("act_to_dir", (dirs.NO, ), no_kwds),
			ord('l'): ("act_to_dir", (dirs.EA, ), no_kwds),
			ord('m'): ("act_to_dir", (dirs.SE, ), no_kwds),
			ord('n'): ("act_to_dir", (dirs.SW, ), no_kwds),
			ord('u'): ("act_to_dir", (dirs.NW, ), no_kwds),
			ord('p'): ("path", no_args, no_kwds),
			ord('<'): ("enter", (PASSAGE_UP, ), no_kwds),
			ord('>'): ("enter", (PASSAGE_DOWN, ), no_kwds),
			ord('H'): ("los_highlight", no_args, no_kwds),
			ord('K'): ("killall", no_args, no_kwds),
			ord('L'): ("loadgame", no_args, no_kwds),
			ord('Q'): ("endgame", no_args, no_kwds),
			ord('S'): ("savegame", no_args, no_kwds),
			ord('d'): ("debug", no_args, no_kwds),
			ord('Z'): ("z_command", no_args, no_kwds),
			ord('\x12'): ("redraw_view", no_args, no_kwds),
		}

	def get_and_act(self, game, level, creature):
		while True:
			c = io.getch(*level.get_coord(creature.loc))
			if c in self.actions:
				if self.execute_action(game, level, creature, self.actions[c]):
					break
			else:
				if 0 < c < 256:
					io.msg("Undefined command: '{}'".format(chr(c)))
				else:
					io.msg("Undefined command key: {}".format(c))

	def execute_action(self, game, level, creature, act):
		function, args, keywords = act
		return getattr(sys.modules[__name__], function)(game, level, creature, *args, **keywords)

def act_to_dir(game, level, creature, direction):
	if level.move_creature_to_dir(game.player, direction):
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

def killall(game, level, creature):
	io.msg("Abrakadabra.")
	level.killall()
	return True

def endgame(game, level, creature, *a, **k):
	game.endgame(*a, **k)

def savegame(game, level, creature, *a, **k):
	game.savegame(*a, **k)

def loadgame(game, level, creature, *a, **k):
	game.loadgame(*a, **k)

def debug(game, level, creature):
	io.clear_level_buffer()

def path(game, level, creature):
	io.msg("Shhhhhhh. Everything will be all right.")

def redraw_view(game, level, creature):
	game.redraw()

def los_highlight(game, level, creature):
	if game.reverse == "":
		game.reverse = "r"
	elif game.reverse == "r":
		game.reverse = ""
	game.draw()

def enter(game, level, creature, passage):
	loc = game.player.loc
	if level.isexit(loc) and level.getexit(loc) == passage:
		try:
			game.enter_passage(level.world_loc, level.getexit(loc))
		except PyrlException:
			io.msg("This passage doesn't seem to lead anywhere.")
	else:
		try:
			new_loc = level.get_passage_loc(passage)
		except KeyError:
			io.msg("This level doesn't seem to have a corresponding passage.")
		else:
			level.movecreature(game.player, new_loc)
	return True