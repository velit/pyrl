import curses
from window import Window
from colors import color

class LevelWindow(Window):
	"""Handles the level display"""
	def __init__(self, window, io):
		Window.__init__(self, window)
		self.io = io

	def drawMap(self, level):
		self.w.move(0,0)
		for s in level.map:
			try:
				self.w.addch(s.y, s.x, s.getVisibleChar().symbol,
								s.getVisibleChar().color)
			except curses.error:
				pass
			# Writing to the last cell of a window raises an exception because
			# the automatic cursor move to the next cell is illegal, this is
			# the only way to the last cell with the current curses wrapper

	def drawMemoryMap(self, level):
		self.w.move(0,0)
		for s in level.map:
			try:
				self.w.addch(s.y, s.x, s.getMemoryChar().symbol,
								s.getMemoryChar().color)
			except curses.error:
				pass

	def drawChar(self, y, x, ch):
		self.w.addch(y,x, ch.symbol, ch.color)

	def drawLos(self, visibility, l, reverse=False):
		if reverse:
			for y,x in visibility:
				try:
					self.w.addch(y,x,l.getSquare(y,x).getVisibleChar().symbol,\
							l.getSquare(y,x).getVisibleChar().color \
							| color["reverse"])
				except curses.error:
					pass
		else:
			for y,x in visibility:
				try:
					self.w.addch(y,x,l.getSquare(y,x).getVisibleChar().symbol,\
							l.getSquare(y,x).getVisibleChar().color)
				except curses.error:
					pass

	def clearLos(self, visibility, l):
		while True:
			try:
				y, x = visibility.pop()
			except IndexError:
				break
			try:
				self.w.addch(y, x, l.getSquare(y,x).getMemoryChar().symbol, \
								l.getSquare(y,x).getMemoryChar().color)
			except curses.error:
				pass

	def drawStar(self, square, col):
		self.w.addch(square.y, square.x, "*", col)

	def drawBlock(self, square, col):
		self.w.addch(square.y, square.x, " ", col | color["reverse"])

	def drawLine(self, startSquare, targetSquare, char=None):
		if char is None:
			symbol = '*'
			color = color["yellow"]
		else:
			symbol = char.symbol
			color = char.color
		x0, y0 = startSquare.y, startSquare.x
		x1, y1 = targetSquare.y, targetSquare.x
		steep = abs(y1 - y0) > abs(x1 - x0)
		if steep:
			x0, y0 = y0, x0
			x1, y1 = y1, x1
		if x0 > x1:
			x0, x1 = x1, x0
			y0, y1 = y1, y0
		deltax = x1 - x0
		deltay = abs(y1 - y0)
		error = deltax / 2
		ystep = None
		y = y0
		if y0 < y1:
			ystep = 1
		else:
			ystep = -1
		for x in range(x0, x1):
			if steep:
				self.w.addch(y, x, symbol, color)
			else:
				self.w.addch(x, y, symbol, color)
			error -= deltay
			if error < 0:
				y += ystep
				error += deltax
		self.w.getch()
