import sys
import const.keys as KEY
import const.directions as DIR
import const.game as GAME
import const.debug as DEBUG
import const.colors as COLOR
import const.generated_level_types as LEVEL_TYPE

from generic_algorithms import add_vector
from input_output import io
from char import Char

direction_map = {
		KEY.LEFT: DIR.WE,
		KEY.DOWN: DIR.SO,
		KEY.UP: DIR.NO,
		KEY.RIGHT: DIR.EA,
		'1': DIR.SW,
		'2': DIR.SO,
		'3': DIR.SE,
		'4': DIR.WE,
		'5': DIR.STOP,
		'6': DIR.EA,
		'7': DIR.NW,
		'8': DIR.NO,
		'9': DIR.NE,
		'h': DIR.WE,
		'j': DIR.SO,
		'k': DIR.NO,
		'l': DIR.EA,
		'.': DIR.STOP,
		'u': DIR.NW,
		'i': DIR.NE,
		'n': DIR.SW,
		'm': DIR.SE,
}

class UserInput(object):
	def __init__(self):
		no_args, no_kwds = (), {}
		self.actions = {
			'<': ("enter", (GAME.PASSAGE_UP, ), no_kwds),
			'>': ("enter", (GAME.PASSAGE_DOWN, ), no_kwds),
			'Q': ("endgame", no_args, no_kwds),
			'S': ("savegame", no_args, no_kwds),
			'q': ("look", no_args, no_kwds),
			'Z': ("z_command", no_args, no_kwds),
			'a': ("attack", no_args, no_kwds),
			'd': ("debug", no_args, no_kwds),
			'+': ("sight_change", (1, ), no_kwds),
			'-': ("sight_change", (-1, ), no_kwds),
			'\x12': ("redraw_view", no_args, no_kwds),
		}
		for key, value in direction_map.items():
			self.actions[key] = ("act_to_dir", (value, ), no_kwds)

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
	target_coord = add_vector(creature.coord, direction)
	if game.creature_move(level, creature, direction):
		return True
	elif level.has_creature(target_coord):
		game.creature_attack(level, creature, direction)
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
	coord = creature.coord
	drawline_flag = False
	direction = DIR.STOP
	while True:
		new_coord = add_vector(coord, direction)
		if level.legal_coord(new_coord):
			coord = new_coord
		io.msg(level.look_information(coord))
		if drawline_flag:
			io.drawline(creature.coord, coord, Char("*", COLOR.YELLOW))
			io.drawline(coord, creature.coord, Char("*", COLOR.YELLOW))
			io.msg("LoS: {}".format(level.check_los(creature.coord, coord)))
		if coord != creature.coord:
			char = level._get_visible_char(coord)
			char = char[0], (COLOR.BASE_BLACK, COLOR.BASE_GREEN)
			io.draw_char(coord, char)
			io.draw_reverse_char(creature.coord, level._get_visible_char(creature.coord))
		c = io.getch()
		game.redraw()
		direction = DIR.STOP
		if c in direction_map:
			direction = direction_map[c]
		elif c == 'd':
			drawline_flag = not drawline_flag
		elif c == 'b':
			from generic_algorithms import bresenham
			for coord in bresenham(level.get_coord(creature.coord), coord):
				io.msg(coord)
		elif c == 's':
			if level.has_creature(coord):
				game.register_status_texts(level.get_creature(coord))
		elif c in "QqzZ ":
			break

def endgame(game, level, creature, *a, **k):
	game.endgame(*a, **k)

def savegame(game, level, creature, *a, **k):
	game.savegame(*a, **k)

def attack(game, level, creature):
	c = io.ask("Specify attack direction:", KEY.GROUP_DEFAULT | set(direction_map.iterkeys()))
	if c in direction_map:
		game.creature_attack(level, creature, direction_map[c])
		return True

def redraw_view(game, level, creature):
	game.redraw()

def enter(game, level, creature, passage):
	coord = game.player.coord
	if level.is_exit(coord) and level.get_exit(coord) == passage:
		try:
			game.enter_passage(level.world_loc, level.get_exit(coord))
		except GAME.PyrlException:
			io.msg("This passage doesn't seem to lead anywhere.")
	else:
		try:
			new_coord = level.get_passage_coord(passage)
		except KeyError:
			io.msg("This level doesn't seem to have a corresponding passage.")
		else:
			if not level.is_passable(new_coord):
				level.remove_creature(level.get_creature(new_coord))
			level.move_creature(game.player, new_coord)
	return True

def sight_change(game, level, creature, amount):
	from const.slots import BODY
	from const.stats import SIGHT
	creature.slots[BODY].stats[SIGHT] += amount

def debug(game, level, creature):
	c = io.getch_print("Avail cmds: vclbdhkpors+-")
	if c == 'v':
		game.flags.show_map = not game.flags.show_map
		game.redraw()
		io.msg("Show map set to {}".format(game.flags.show_map))
	elif c == 'c':
		DEBUG.CROSS = not DEBUG.CROSS
		io.msg("Path heuristic cross set to {}".format(DEBUG.CROSS))
	elif c == 'l':
		GAME.LEVEL_TYPE = LEVEL_TYPE.ARENA if GAME.LEVEL_TYPE == LEVEL_TYPE.DUNGEON else LEVEL_TYPE.DUNGEON
		io.msg("Level type set to {}".format(GAME.LEVEL_TYPE))
	elif c == 'b':
		io.draw_block((4,4))
	elif c == 'd':
		if not DEBUG.PATH:
			DEBUG.PATH = True
			io.msg("Path debug set")
		elif not DEBUG.PATH_STEP:
			DEBUG.PATH_STEP = True
			io.msg("Path debug and stepping set")
		else:
			DEBUG.PATH = False
			DEBUG.PATH_STEP = False
			io.msg("Path debug unset")
	elif c == 'h':
		game.flags.reverse = not game.flags.reverse
		game.redraw()
		io.msg("Reverse set to {}".format(game.flags.reverse))
	elif c == 'k':
		creature_list = level.creatures.values()
		creature_list.remove(creature)
		for i in creature_list:
			level.remove_creature(i)
		io.msg("Abrakadabra.")
	elif c == 'o':
		passage_down = level.get_passage_coord(GAME.PASSAGE_DOWN)
		io.draw_path(level.path(creature.coord, passage_down))
		game.redraw()
	elif c == 'p':
		passage_up = level.get_passage_coord(GAME.PASSAGE_UP)
		passage_down = level.get_passage_coord(GAME.PASSAGE_DOWN)
		io.draw_path(level.path(passage_up, passage_down))
		game.redraw()
	elif c == 's':
		import code
		code.interact(local=locals())
	elif c == 'e':
		import curses
		io.msg(curses.COLORS, curses.COLOR_PAIRS, curses.can_change_color())
		io.msg(curses.A_ALTCHARSET, curses.A_BLINK, curses.A_BOLD, curses.A_DIM, curses.A_NORMAL,
				curses.A_REVERSE, curses.A_STANDOUT, curses.A_UNDERLINE)
	elif c == 'r':
		pass
	elif c == '+':
		from const.slots import BODY
		from const.stats import SIGHT
		creature.slots[BODY].stats[SIGHT] += 1
		while True:
			c2 = io.getch_print("[+-]")
			if c2 == "+":
				creature.slots[BODY].stats[SIGHT] += 1
			elif c2 == "-":
				creature.slots[BODY].stats[SIGHT] -= 1
			else:
				break
	elif c == '-':
		from const.slots import BODY
		from const.stats import SIGHT
		creature.slots[BODY].stats[SIGHT] -= 1
		while True:
			c2 = io.getch_print("[+-]")
			if c2 == "+":
				creature.slots[BODY].stats[SIGHT] += 1
			elif c2 == "-":
				creature.slots[BODY].stats[SIGHT] -= 1
			else:
				break
	elif c == 'm':
		io.msg("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam varius massa enim, id fermentum erat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. In et enim ut nibh rutrum suscipit. Aenean a lacus eget justo dignissim tempus. Nunc venenatis congue erat vel adipiscing. Nam nulla felis, accumsan eu sagittis aliquet, fermentum at tortor. Suspendisse tortor risus, dapibus quis porta vel, mattis sit amet libero. Morbi vel metus eget metus ultricies ultrices placerat ac sapien. Lorem ipsum dolor sit amet, consectetur adipiscing elit.  Nulla urna erat, lacinia vitae pellentesque et, accumsan eget ante. Sed commodo molestie ipsum, a mattis sapien malesuada at. Integer et lorem magna. Sed nec erat orci. Donec id elementum elit. In hac habitasse platea dictumst. Duis id nisi ut felis convallis blandit id sit amet magna. Nam feugiat erat eget velit ullamcorper varius. Nunc tellus massa, fermentum eu aliquet non, fermentum a quam.  Pellentesque turpis erat, aliquam at feugiat in, congue nec urna. Nulla ut turpis dapibus metus blandit faucibus.  Suspendisse potenti. Proin facilisis massa vitae purus dignissim quis dapibus eros gravida. Vivamus ac sapien ante, ut euismod nunc. Pellentesque faucibus neque at tortor malesuada eu commodo nisl vehicula. Vivamus eu odio ut est egestas luctus. Duis orci magna, tincidunt id suscipit id, consectetur sodales nisl. Etiam justo lorem, molestie sit amet rutrum eget, consequat mattis magna.  Fusce eros est, tincidunt id consequat id, scelerisque ac sapien.  Donec lacus leo, adipiscing et vulputate in, pulvinar vitae sem. Suspendisse sem augue, adipiscing vitae tempor sit amet, egestas a neque. Donec nibh mauris, rutrum vitae dictum in, adipiscing in magna. Duis fringilla sem vel nisl tempus dignissim. Fusce vel felis ipsum. Sed risus ipsum, iaculis a mollis vel, viverra in nisi. Suspendisse est tellus, aliquet et vulputate vel, iaculis egestas nulla.  Praesent sed tortor sed neque varius consequat. Quisque interdum facilisis convallis. Aliquam eu nisi arcu. Proin convallis sagittis nisi id molestie. Aenean rutrum elementum mauris, vitae venenatis tellus semper et. Proin eu nisl ligula. Maecenas dui mi, varius eget adipiscing quis, commodo et libero.")

	else:
		io.msg("Undefined debug key: {}".format(chr(c) if 0 < c < 128 else c))
