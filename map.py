import random

from square import Square
from io import IO

class Map:
	def __init__(self, dimensions, squares):
		f = IO().floors["f"]
		w = IO().floors["w"]
		r = IO().floors["r"]

		self.squares = squares

		y,x = dimensions
		self.map = [[Square(r,j,i) for i in range(x)] for j in range(y)]

		self.generateMap()
		#self.makeRoom(0,0,10,10)
		#self.addUpStairCase()
		#self.addDownStairCase()

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
			self.attemptCorridor()
		self.turnRockToWall()

	def makeInitialRoom(self):
		while True:
			height, width = random.randrange(5,11), random.randrange(7,14)
			if height*width <= 8*8:
				break
		while True: 
			y, x = random.randrange(1,len(self.map)-height-1), \
					random.randrange(1,len(self.map[0])-width-1)
			if self.rectIsDiggable(y, x, height, width):
				break
		
		self.makeRoom(y, x, height, width)

	def attemptCorridor(self):
		square, dir = self.getWallSquare()
		y,x = square.loc
		len = random.randrange(7,20)
		if dir == "up" and self.rectIsDiggable(y-len, x-1, len, 3) or \
				dir == "down" and self.rectIsDiggable(y+1, x-1, len, 3) or \
				dir == "left" and self.rectIsDiggable(y-1, x-len, 3, len) or \
				dir =="right" and self.rectIsDiggable(y-1, x+1, 3, len):
			self.makeCorridor(square, dir, len)
			return True

	def makeCorridor(self, square, dir, len):
		y0,x0 = square.loc

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

		self.digRect(wy, wx, IO().floors["w"], whei, wwid)
		self.digRect(fy, fx, IO().floors["f"], fhei, fwid)

	def getWallSquare(self):
		while True:
			tile = self.getRandomTile()
			dir = self.isWall(tile)
			if dir[0]:
				return tile, dir[1]

	def isWall(self, square):
		w = IO().floors["w"]
		f = IO().floors["f"]
		r = IO().floors["r"]
		y,x = square.loc
		if y in (0, len(self.map)-1) or x in (0, len(self.map[y])-1):
			return False, ""
		if self.getSquare(y-1,x).floor == w and self.getSquare(y+1,x).floor == w:
			if self.getSquare(y,x-1).floor == f and self.getSquare(y,x+1).floor == r:
				return True, "right"
			elif self.getSquare(y,x-1).floor == r and self.getSquare(y,x+1).floor == f:
				return True, "left"
		elif self.getSquare(y,x-1).floor == w and self.getSquare(y,x+1).floor == w:
			if self.getSquare(y-1,x).floor == f and self.getSquare(y+1,x).floor == r:
				return True, "down"
			elif self.getSquare(y-1,x).floor == r and self.getSquare(y+1,x).floor == f:
				return True, "up"
		return False, ""

	def rectIsDiggable(self, y0, x0, height, width):
		if y0 < 0 or x0 < 0 or y0+height >= len(self.map) \
				or x0+width >= len(self.map[y0]):
			return False
		for y in range(y0, y0+height):
			for x in range(x0, x0+width):
				if self.map[y][x].floor != IO().floors["r"]:
					return False
		return True	
	def digRect(self, y0, x0, floor, height=1, width=1):
		for y in range(y0, y0+height):
			for x in range(x0, x0+width):
				self.map[y][x].floor = floor

	def makeRoom(self, y0, x0, height, width):
		w = IO().floors["w"]
		f = IO().floors["f"]
		for y in range(y0, y0+height):
			for x in range(x0, x0+width):
				if y in (y0, y0+height-1) or x in (x0, x0+width-1):
					self.map[y][x].floor = w
				else:
					self.map[y][x].floor = f

	def turnRockToWall(self):
		for row in self.map:
			for col in row:
				if col.floor == IO().floors["r"]:
					col.floor = IO().floors["w"]

	def addUpStairCase(self):
		square = self.getFreeTile()
		square.floor = IO().floors["us"]
		self.squares["us"] = square
		square.draw()

	def addDownStairCase(self):
		square = self.getFreeTile()
		square.floor = IO().floors["ds"]
		self.squares["ds"] = square
		square.draw()
