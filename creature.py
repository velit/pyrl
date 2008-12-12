class Creature:
	def act(self, game):
		self.move(game.cur_level.squares[game.player], game.cur_level)
	
	def move(self, directionsquare, level):
		dy, dx = directionsquare.loc
		sy, sx = level.squares[self].loc #self loc
		ny, nx = None, None #newy
		if dy-sy > 0:
			ny = sy+1
		elif dy-sy < 0:
			ny = sy-1
		else:
			ny = sy

		if dx-sx > 0:
			nx = sx+1
		elif dx-sx < 0:
			nx = sx-1
		else:
			nx = sx

		target_square = level.getSquare(ny,nx)

		if target_square.passable():
			level.moveCreature(self, target_square)
