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
	io.msg(game.player.turn_visibility)

def path(game):
	io.msg("Shhhhhhh. Everything will be all right.")

def redraw_view(game):
	game.redraw()

def los_highlight(game):
	if game.player.reverse == "":
		game.player.reverse = "r"
	elif game.player.reverse == "r":
		game.player.reverse = ""
	game.redraw()

def descend(game):
	s = game.player.getsquare()
	if s.isexit() and s.getexit() == PASSAGE_DOWN:
		try:
			game.enter_passage(game.cur_level, s)
		except KeyError:
			io.msg("This passage doesn't seem to lead anywhere.")
	else:
		try:
			s = game.cur_level.getsquare(entrance=PASSAGE_DOWN)
		except KeyError:
			io.msg("This level doesn't seem to have a downward passage.")
		else:
			game.cur_level.movecreature(game.player, *s.getcoord())
	return True

def ascend(game):
	s = game.player.getsquare()
	if s.isexit() and s.getexit() == PASSAGE_UP:
		try:
			game.enter_passage(game.cur_level, s)
		except KeyError:
			io.msg("This passage doesn't seem to lead anywhere.")
	else:
		try:
			s = game.cur_level.getsquare(entrance=PASSAGE_UP)
		except KeyError:
			io.msg("This level doesn't seem to have an upward passage.")
		else:
			game.cur_level.movecreature(game.player, *s.getcoord())
	return True
