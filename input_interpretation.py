import curses
import input_functions
import const.directions as dirs

from pio import io
from const.game import PASSAGE_UP, PASSAGE_DOWN

no_kwds = {}
no_args = ()
actions = {
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
	ord('<'): ("ascend", no_args, no_kwds),
	ord('>'): ("descend", no_args, no_kwds),
	ord('H'): ("los_highlight", no_args, no_kwds),
	ord('K'): ("killall", no_args, no_kwds),
	ord('L'): ("loadgame", no_args, no_kwds),
	ord('Q'): ("endgame", no_args, no_kwds),
	ord('S'): ("savegame", no_args, no_kwds),
	ord('d'): ("debug", no_args, no_kwds),
	ord('Z'): ("z_command", no_args, no_kwds),
	ord('\x12'): ("redraw_view", no_args, no_kwds),
}
del no_kwds, no_args

def get_input_and_act(game):
	while True:
		c = io.getch(*game.player.getcoord())
		if c in actions:
			if execute_action(game, actions[c]):
				break
		else:
			if 0 < c < 256:
				io.msg("Undefined command: '{}'".format(chr(c)))
			else:
				io.msg("Undefined command key: {}".format(c))

def execute_action(game, act):
	function, args, keywords = act
	return getattr(input_functions, function)(game, *args, **keywords)
