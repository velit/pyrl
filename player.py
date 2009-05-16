import curses

from creature import Creature
from io import IO
from char import Char
from fov import doFov
from tile import tiles

class Player(Creature):

	def __init__(self):
		Creature.__init__(self)
		self.ch = Char('@', IO().colors["white"])

	def move(self, direction, level):
		d = direction
		y,x = level.squares[self].loc
		ny = y
		nx = x

		if d in (7,8,9,curses.KEY_UP) : #up
			ny -= 1
		if d in (1,2,3,curses.KEY_DOWN): #down
			ny += 1 
		if d in (1,4,7,curses.KEY_LEFT): #left
			nx -= 1
		if d in (3,6,9,curses.KEY_RIGHT): #right
			nx += 1
		if d == 5:
			return True
		
		target_square = level.getSquare(ny,nx)

		if target_square.passable():
			level.moveCreature(self, target_square)
			return True
		elif target_square.creature is not None:
			self.hit(target_square.creature, level)
			return True
		return False

	def hit(self, creature, level):
		IO().printMsg("Poof.")
		level.removeCreature(creature)

	def act(self, game):
		while True:
			doFov(self, game.cur_level)
			IO().moveCursor(game.cur_level.squares[self])
			c = IO().getch()
			if 0 <= c < 256:
				c = chr(c)
				if c.isdigit():
					if self.move(int(c), game.cur_level):
						break
					else:
						IO().printMsg("You can't move there.")
				elif c.isalpha():
					if c == 'Q':
						game.endGame()
					elif c == 'S':
						game.saveGame()
					elif c == 'p':
						IO().drawLine(game.cur_level.squares[self], \
								game.cur_level.squares["ds"])
					elif c == 'b':
						IO().printMsg(str(game.dimensions[0])+" "+str(game.dimensions[1]))
					elif c == 'l':
						cre = game.cur_level.getClosestCreature(self)
						if cre:
							IO().drawLine(game.cur_level.squares[self], game.cur_level.squares[cre])
					elif c == 'f':
						game.cur_level.draw()
					elif c == 'H':
						IO().reverse = not IO().reverse
					else:
						IO().printMsg("Unknown command: '"+c+"'")
				else:
					if c == '>':
						if True:#game.cur_level.squares[self].tile == tiles["ds"]:
							game.descend()
							break
						else:
							IO().printMsg("You don't see a staircase going down.")
					elif c == '<':
						if True:#game.cur_level.squares[self].tile == tiles["us"]:
							game.ascend()
							break
						else:
							IO().printMsg("You don't see a staircase going up.")
					elif c == '+':
						self.sight += 1
						break
					elif c == '-':
						if self.sight > 0:
							self.sight -= 1
						break
					else:
						IO().printMsg("Unknown command: '"+c+"'")
			else:
				if c in (curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN):
					if self.move(c, game.cur_level):
						break
					else:
						IO().printMsg("You can't move there.")
				else:
					IO().printMsg("Unknown command: '"+str(c)+"'")
