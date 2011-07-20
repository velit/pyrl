from pio import io
from const.game import PASSAGE_UP, PASSAGE_DOWN

def act_to_dir(game, direction):
	if game.cur_level.move_creature_to_dir(game.player, direction):
		return True
	else:
		io.msg("You can't move there.")
		return False

def z_command(game):
	c = io.getch()
	if c == ord('Q'):
		game.endgame(ask=False)
	elif c == ord('Z'):
		game.savegame(ask=False)

def killall(game):
	io.msg("Abrakadabra.")
	game.cur_level.killall()
	return True

def endgame(game, *a, **k):
	game.endgame(*a, **k)

def savegame(game, *a, **k):
	game.savegame(*a, **k)

def loadgame(game, *a, **k):
	game.loadgame(*a, **k)

def debug(game):
	io.msg((game.player.loc, game.cur_level.passable(game.player.loc)))

def path(game):
	io.msg("Shhhhhhh. Everything will be all right.")

def redraw_view(game):
	game.redraw()
	game.cur_level.draw()

def los_highlight(game):
	if game.player.reverse == "":
		game.player.reverse = "r"
	elif game.player.reverse == "r":
		game.player.reverse = ""
	game.redraw()

def descend(game):
	loc = game.player.loc
	l = game.cur_level
	if l.isexit(loc) and l.getexit(loc) == PASSAGE_DOWN:
		game.enter_passage(game.cur_level.world_loc, l.getexit(loc))
		#try:
		#	game.enter_passage(game.cur_level.world_loc, l.getexit(loc))
		#except KeyError:
		#	io.msg("This passage doesn't seem to lead anywhere.")
	else:
		try:
			new_loc = game.cur_level.get_passage_loc(PASSAGE_DOWN)
		except KeyError:
			io.msg("This level doesn't seem to have a downward passage.")
		else:
			game.cur_level.movecreature(game.player, new_loc)
	return True

def ascend(game):
	loc = game.player.loc
	l = game.cur_level
	if l.isexit(loc) and l.getexit(loc) == PASSAGE_UP:
		try:
			game.enter_passage(game.cur_level.world_loc, l.getexit(loc))
		except KeyError:
			io.msg("This passage doesn't seem to lead anywhere.")
	else:
		try:
			new_loc = game.cur_level.get_passage_loc(PASSAGE_UP)
		except KeyError:
			io.msg("This level doesn't seem to have a downward passage.")
		else:
			game.cur_level.movecreature(game.player, new_loc)
	return True
