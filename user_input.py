import sys
import const.keys as KEY
import const.directions as DIR
import const.game as GAME
import const.debug as DEBUG
import const.colors as COLOR

from pio import io
from char import Char
from itertools import imap

direction_map = {
		KEY.LEFT: DIR.WE,
		KEY.DOWN: DIR.SO,
		KEY.UP: DIR.NO,
		KEY.RIGHT: DIR.EA,
		u'1': DIR.SW,
		u'2': DIR.SO,
		u'3': DIR.SE,
		u'4': DIR.WE,
		u'5': DIR.STOP,
		u'6': DIR.EA,
		u'7': DIR.NW,
		u'8': DIR.NO,
		u'9': DIR.NE,
		u'h': DIR.WE,
		u'j': DIR.SO,
		u'k': DIR.NO,
		u'l': DIR.EA,
		u'.': DIR.STOP,
		u'u': DIR.NW,
		u'i': DIR.NE,
		u'n': DIR.SW,
		u'm': DIR.SE,
}

class UserInput(object):
	def __init__(self):
		no_args, no_kwds = (), {}
		self.actions = {
			u'<': (u"enter", (GAME.PASSAGE_UP, ), no_kwds),
			u'>': (u"enter", (GAME.PASSAGE_DOWN, ), no_kwds),
			u'Q': (u"endgame", no_args, no_kwds),
			u'S': (u"savegame", no_args, no_kwds),
			u'q': (u"look", no_args, no_kwds),
			u'Z': (u"z_command", no_args, no_kwds),
			u'a': (u"attack", no_args, no_kwds),
			u'd': (u"debug", no_args, no_kwds),
			u'\x12': (u"redraw_view", no_args, no_kwds),
		}
		for key, value in direction_map.items():
			self.actions[key] = (u"act_to_dir", (value, ), no_kwds)

	def get_and_act(self, game, level, creature):
		c = io.getch()
		if c in self.actions:
			return self.execute_action(game, level, creature, self.actions[c])
		else:
			io.msg("Undefined key: {}".format(chr(c) if 0 < c < 128 else c))

	def execute_action(self, game, level, creature, act):
		function, args, keywords = act
		return getattr(sys.modules[__name__], function)(game, level, creature, *args, **keywords)

def act_to_dir(game, level, creature, direction):
	target_coord = level.get_relative_coord(creature.coord, direction)
	if game.creature_move(level, creature, direction):
		return True
	elif level.has_creature(target_coord):
		game.creature_attack(level, creature, direction)
		return True
	else:
		io.msg(u"You can't move there.")
		return False

def z_command(game, level, creature):
	c = io.getch()
	if c == ord(u'Q'):
		game.endgame(ask=False)
	elif c == ord(u'Z'):
		game.savegame(ask=False)

def look(game, level, creature):
	coord = creature.coord
	drawline_flag = False
	direction = DIR.STOP
	while True:
		coord = level.get_relative_coord(coord, direction)
		io.msg(level.look_information(coord))
		if drawline_flag:
			io.drawline(level.get_coord(creature.coord), coord, Char(u"*", COLOR.YELLOW))
			io.msg(u"LoS: {}".format(level.check_los(creature.coord, coord)))
		c = io.getch()
		game.redraw()
		direction = DIR.STOP
		if c in direction_map:
			direction = direction_map[c]
		elif c == u'd':
			drawline_flag = not drawline_flag
		elif c == u'b':
			from generic_algorithms import bresenham
			for coord in bresenham(level.get_coord(creature.coord), coord):
				io.msg(coord)
		elif c == u's':
			if level.has_creature(coord):
				game.register_status_texts(level.get_creature(coord))
		elif c in u"QqzZ ":
			break

def endgame(game, level, creature, *a, **k):
	game.endgame(*a, **k)

def savegame(game, level, creature, *a, **k):
	game.savegame(*a, **k)

def attack(game, level, creature):
	c = io.sel_getch(u"Specify attack direction:", GAME.DEFAULT | set(direction_map.keys()))
	if c in direction_map:
		game.creature_attack(level, creature, direction_map[c])
		return True

def debug(game, level, creature):
	c = io.getch_print(u"Avail cmds: vclbdhkp")
	if c == u'v':
		game.flags.show_map = not game.flags.show_map
		game.redraw()
		io.msg(u"Show map set to {}".format(game.flags.show_map))
	elif c == u'c':
		DEBUG.CROSS = not DEBUG.CROSS
		io.msg(u"Path heuristic cross set to {}".format(DEBUG.CROSS))
	elif c == u'l':
		GAME.LEVEL_TYPE = u"arena" if GAME.LEVEL_TYPE == u"dungeon" else u"dungeon"
		io.msg(u"Level type set to {}".format(GAME.LEVEL_TYPE))
	elif c == u'b':
		io.draw_block((4,4))
	elif c == u'd':
		DEBUG.PATH = not DEBUG.PATH
		io.msg(u"Path debug set to {}".format(DEBUG.PATH))
	elif c == u'h':
		game.flags.reverse = not game.flags.reverse
		game.redraw()
		io.msg(u"Reverse set to {}".format(game.flags.reverse))
	elif c == u'k':
		creature_list = level.creatures.values()
		creature_list.remove(creature)
		for i in creature_list:
			level.remove_creature(i)
		io.msg(u"Abrakadabra.")
	elif c == u'p':
		passage_up = level.get_passage_coord(GAME.PASSAGE_UP)
		passage_down = level.get_passage_coord(GAME.PASSAGE_DOWN)
		io.draw_path(level.path(passage_up, passage_down))
	else:
		io.msg("Undefined debug key: {}".format(chr(c) if 0 < c < 128 else c))

def redraw_view(game, level, creature):
	game.redraw()

def enter(game, level, creature, passage):
	coord = game.player.coord
	if level.is_exit(coord) and level.get_exit(coord) == passage:
		try:
			game.enter_passage(level.world_loc, level.get_exit(coord))
		except GAME.PyrlException:
			io.msg(u"This passage doesn't seem to lead anywhere.")
	else:
		try:
			new_coord = level.get_passage_coord(passage)
		except KeyError:
			io.msg(u"This level doesn't seem to have a corresponding passage.")
		else:
			if not level.is_passable(new_coord):
				level.remove_creature(level.get_creature(new_coord))
			level.move_creature(game.player, new_coord)
	return True
