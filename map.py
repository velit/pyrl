import random

from square import Square
from tile import tiles

f = tiles["f"]
w = tiles["w"]
r = tiles["r"]

class Map(object):
	"""This object holds the data of a Level object, and methods for manipulating the data."""
	def __init__(self, y, x, generate=True):

		self.squares = {}

		self.map = [[Square(r,j,i) for i in range(x)] for j in range(y)]

		if generate:
			self.generateMap()

	def getSquare(self, y, x):
		return self.map[y][x]

	def getFreeTile(self):
		#TODO Write a new one that doesn't loop indefinitely if the map is full
		while True:
			tile = self.getRandomTile()
			if tile.passable():
				return tile

	def getRandomTile(self):
		return random.choice(random.choice(self.map))

	def generateMap(self):
		self.makeInitialRoom()
		for x in range(200):
			if random.random() < 0.50:
				self.attemptCorridor()
			else:
				self.attemptRoom()
		self.addUpStairCase()
		self.addDownStairCase()

	def makeInitialRoom(self):
		while True:
			height, width = random.randrange(5,11), random.randrange(7,14)
			if height*width <= 8*8:
				break
		while True: 
			y, x = random.randrange(1,len(self.map)-height-1), \
					random.randrange(1,len(self.map[0])-width-1)
			if self.rectDiggable(y, x, height, width):
				break
		
		self.makeRoom(y, x, height, width)

	def getWallSquare(self):
		while True:
			tile = self.getRandomTile()
			dir = self.isWall(tile)
			if dir[0]:
				return tile, dir[1]

	def isWall(self, square):
		y,x = square.y, square.x
		if y in (0, len(self.map)-1) or x in (0, len(self.map[y])-1):
			return False, ""
		if self.getSquare(y-1,x).tile == w and self.getSquare(y+1,x).tile == w:
			if self.getSquare(y,x-1).tile == f and self.getSquare(y,x+1).tile == r:
				return True, "right"
			elif self.getSquare(y,x-1).tile == r and self.getSquare(y,x+1).tile == f:
				return True, "left"
		elif self.getSquare(y,x-1).tile == w and self.getSquare(y,x+1).tile == w:
			if self.getSquare(y-1,x).tile == f and self.getSquare(y+1,x).tile == r:
				return True, "down"
			elif self.getSquare(y-1,x).tile == r and self.getSquare(y+1,x).tile == f:
				return True, "up"
		return False, ""

	def rectDiggable(self, y0, x0, height, width):
		if y0 < 0 or x0 < 0 or y0+height >= len(self.map) \
				or x0+width >= len(self.map[y0]):
			return False
		for y in range(y0, y0+height):
			for x in range(x0, x0+width):
				if self.map[y][x].tile != tiles["r"] and self.map[y][x].tile != tiles["w"]:
					return False
		return True	

	def attemptRoom(self):
		square, dir = self.getWallSquare()
		y0,x0 = square.y, square.x
		height, width = random.randrange(5,11), random.randrange(7,14)
		ypos, xpos = random.choice(range(height-2)), random.choice(range(width-2))

		if dir == "left":
			y = y0 - 1 - ypos
			x = x0 - width + 1
		elif dir == "right":
			y = y0 - 1 - ypos
			x = x0
		elif dir == "up":
			y = y0 - height + 1
			x = x0 - 1 - xpos
		elif dir == "down":
			y = y0
			x = x0 - 1 - xpos

		if self.rectDiggable(y, x, height, width):
			self.makeRoom(y, x, height, width)
			self.map[y0][x0].tile = tiles["f"]

	def makeRoom(self, y0, x0, height, width):
		for y in range(y0, y0+height):
			for x in range(x0, x0+width):
				if y in (y0, y0+height-1) or x in (x0, x0+width-1):
					self.map[y][x].tile = w
				else:
					self.map[y][x].tile = f

	def digRect(self, y0, x0, tile, height=1, width=1):
		for y in range(y0, y0+height):
			for x in range(x0, x0+width):
				self.map[y][x].tile = tile

	def turnRockToWall(self):
		for row in self.map:
			for col in row:
				if col.tile == tiles["r"]:
					col.tile = tiles["w"]

	def attemptCorridor(self):
		square, dir = self.getWallSquare()
		y,x = square.y, square.x
		len = random.randrange(7,20)
		if dir == "up" and self.rectDiggable(y-len, x-1, len, 3) or \
				dir == "down" and self.rectDiggable(y+1, x-1, len, 3) or \
				dir == "left" and self.rectDiggable(y-1, x-len, 3, len) or \
				dir =="right" and self.rectDiggable(y-1, x+1, 3, len):
			self.makeCorridor(square, dir, len)
			return True

	def makeCorridor(self, square, dir, len):
		y0,x0 = square.y, square.x

		if dir in ("up", "down"):
			fhei = whei = len
			fwid = 1
			wwid = 3
			fx = x0
			wx = x0-1
			if dir == "up":
				fy = y0-len+1
				wy = fy-1
			else:
				fy = y0
				wy = fy+1

		elif dir in ("left", "right"):
			fwid = wwid = len
			fhei = 1
			whei = 3
			fy = y0
			wy = y0-1
			if dir == "left":
				fx = x0-len+1
				wx = fx-1
			else:
				fx = x0
				wx = fx+1

		self.digRect(wy, wx, tiles["w"], whei, wwid)
		self.digRect(fy, fx, tiles["f"], fhei, fwid)

	def addUpStairCase(self):
		while True:
			square = self.getFreeTile()
			y,x = square.y, square.x
			m = self.map
			f = tiles["f"]
			if m[y-1][x].tile == f and m[y+1][x].tile == f and m[y][x-1].tile == f and m[y][x+1].tile == f:
				break

		square.tile = tiles["us"]
		self.squares["us"] = square

	def addDownStairCase(self):
		while True:
			square = self.getFreeTile()
			y,x = square.y, square.x
			m = self.map
			f = tiles["f"]
			if m[y-1][x].tile == f and m[y+1][x].tile == f and m[y][x-1].tile == f and m[y][x+1].tile == f:
				break

		square.tile = tiles["ds"]
		self.squares["ds"] = square
