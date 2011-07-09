from pio import io
from const.game import PASSAGE_UP, PASSAGE_DOWN

def act_to_dir(game, direction):
	if game.p.l.move_creature_to_dir(game.p, direction):
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
	game.p.l.killall()
	return True

def endgame(game, *a, **k):
	game.endgame(*a, **k)

def savegame(game, *a, **k):
	game.savegame(*a, **k)

def loadgame(game, *a, **k):
	game.loadgame(*a, **k)

def debug(game):
	io.msg((io.level_rows, io.level_cols))
	io.msg(game.p.getloc())

def path(game):
	io.msg("Shhhhhhh. Everything will be all right.")

def los_highlight(game):
	if game.p.reverse == "":
		game.p.reverse = "r"
	elif game.p.reverse == "r":
		game.p.reverse = ""
	game.redraw()

def _kill(square):
	if square.creature is not None:
		io.msg(msg.format(square.creature.name))
		square.creature.die()

def ascend(game):
	s = game.p.getsquare()
	if s.isexit() and s.tile.exit_point == PASSAGE_UP:
		try:
			game.p.exit_level()
			return True
		except KeyError:
			io.msg("This passage doesn't seem to lead anywhere.")
	else:
		try:
			s = game.p.l.getsquare(entrance=PASSAGE_UP)
			_kill(s)
			game.p.l.movecreature(game.p, *s.getloc())
			return True
		except KeyError:
			io.msg("This level doesn't seem to have an upward passage.")

def descend(game):
	s = game.p.getsquare()
	if s.isexit() and s.tile.exit_point == PASSAGE_DOWN:
		try:
			game.p.exit_level()
			return True
		except KeyError:
			io.msg("This passage doesn't seem to lead anywhere.")
	else:
		try:
			s = game.p.l.getsquare(entrance=PASSAGE_DOWN)
			_kill(s)
			game.p.l.movecreature(game.p, *s.getloc())
			return True
		except KeyError:
			io.msg("This level doesn't seem to have a downward passage.")
