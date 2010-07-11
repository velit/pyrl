import curses
from window import Window
from colors import color
from bresenham import bresenham

class LevelWindow(Window):
	"""Handles the level display"""
	def __init__(self, window, io):
		Window.__init__(self, window)
		self.io = io

	def drawmap(self, level):
		self.w.move(0,0)
		for s in level.map:
			try:
				self.w.addch(s.y, s.x, s.get_visible_char().symbol,
							s.get_visible_char().color)
			except curses.error:
				pass
			# Writing to the last cell of a window raises an exception because
			# the automatic cursor move to the next cell is illegal, this is
			# the only way to the last cell with the current curses wrapper

	def drawmemory(self, level):
		self.w.move(0,0)
		for s in level.map:
			try:
				self.w.addch(s.y, s.x, s.get_memory_char().symbol,
							s.get_memory_char().color)
			except curses.error:
				pass

	def drawsquare(self, s):
		try:
			self.w.addch(s.y, s.x, s.tile.visible_ch.symbol,
						s.tile.visible_ch.color)
		except curses.error:
			pass

	def drawlos(self, visibility, l, reverse=None):
		if reverse:
			reverse = color["reverse"]
		for s in visibility:
			try:
				self.w.addch(s.y, s.x, s.get_visible_char().symbol,
						s.get_visible_char().color | reverse)
			except curses.error:
				pass

	def clearlos(self, old_visibility, l):
		for s in old_visibility:
			try:
				self.w.addch(s.y, s.x,
							l.getsquare(s.y, s.x).get_memory_char().symbol,
							l.getsquare(s.y, s.x).get_memory_char().color)
			except curses.error:
				pass

	def drawstar(self, square, col):
		try:
			self.w.addch(square.y, square.x, "*", col)
		except curses.error:
			pass

	def drawblock(self, square, col):
		try:
			self.w.addch(square.y, square.x, " ", col | color["reverse"])
		except curses.error:
			pass

	def drawline(self, s0, s1, char=None):
		y0, x0 = s0.getloc()
		y1, x1 = s1.getloc()
		if char is None:
			symbol = '*'
			color_ = color["yellow"]
		else:
			symbol = char.symbol
			color_ = char.color
		for y, x in bresenham(y0, x0, y1, x1):
			self.w.addch(y, x, symbol, color_)
		self.io.getch(y1, x1)
