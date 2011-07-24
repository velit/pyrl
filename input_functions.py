from pio import io
from const.game import PASSAGE_UP, PASSAGE_DOWN, PyrlException

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
