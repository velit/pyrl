import curses

from creature import Creature
from char import Char
from fov import doFov
from tile import tiles
from io import io
from colors import color

UP = map(ord, ('7', '8', '9')); UP.append(curses.KEY_UP)
DOWN = map(ord, ('1', '2', '3')); DOWN.append(curses.KEY_DOWN)
LEFT = map(ord, ('1', '4', '7')); LEFT.append(curses.KEY_LEFT)
RIGHT = map(ord, ('3', '6', '9')); RIGHT.append(curses.KEY_RIGHT)
STOP = (ord('5'), ord('.'))

class Player(Creature):
	def __init__(self, level, game):
		Creature.__init__(self, level)
		self.game = game
		self.name = "tappi"
		self.n = "god"
		self.ch = Char('@', color["white"])

		self.register_status_texts()
		self.def_actions()

	def register_status_texts(self):
		io.s.register("hp", "HP: ", lambda: self.hp)

	def def_actions(self):
		a = {}

		a[ord('>')] = self.descend
		a[ord('<')] = self.ascend
		a[curses.KEY_DOWN] = self.move
		a[curses.KEY_LEFT] = self.move
		a[curses.KEY_RIGHT] = self.move
		a[curses.KEY_UP] = self.move
		a[ord('1')] = self.move
		a[ord('2')] = self.move
		a[ord('3')] = self.move
		a[ord('4')] = self.move
		a[ord('5')] = self.move
		a[ord('6')] = self.move
		a[ord('7')] = self.move
		a[ord('8')] = self.move
		a[ord('9')] = self.move

		a[ord('Q')] = self.endgame
		a[ord('S')] = self.savegame

		self.actions = a

	def move(self, d):
		y,x = self.l.squares[self].y, self.l.squares[self].x
		ny = y
		nx = x

		if d in UP:
			ny -= 1
		if d in DOWN:
			ny += 1 
		if d in LEFT:
			nx -= 1
		if d in RIGHT:
			nx += 1
		if d == STOP:
			return True
		
		target_square = self.l.getSquare(ny,nx)

		if target_square.passable():
			self.l.moveCreature(self, target_square)
			return True
		elif target_square.creature is not None:
			self.hit(target_square.creature)
			return True
		else:
			io.queueMsg("You can't move there.")
			return False

	def hit(self, creature):
		creature.hp -= 25
		if creature.hp > 0:
			io.queueMsg("You hit the "+creature.name+" and wound "+creature.n+".")
		else:
			creature.die()
			io.queueMsg("You hit the "+creature.name+" and kill "+creature.n+".")

	def descend(self, char):
		self.game.descend()
		return True

	def ascend(self, char):
		self.game.ascend()
		return True

	def endgame(self, char):
		self.game.endGame()

	def savegame(self, char):
		self.game.saveGame()

	def act(self):
		self.hp -= 1
		self.updateLos()
		while True:
			c = io.getch(self.l.squares[self].y, self.l.squares[self].x)
			if c in self.actions:
				if self.actions[c](c):
					break
			else:
				if 0 < c < 256:
					c = chr(c)
					io.queueMsg("Undefined command: '"+c+"'")
				else:
					io.queueMsg("Undefined command key: "+str(c))
