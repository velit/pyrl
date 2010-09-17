import curses
import colors
from char import Char
from window import Window
from bresenham import bresenham

class LevelWindow(Window):
	"""Handles the level display"""
	def __init__(self, window):
		super(LevelWindow, self).__init__(window)

	def drawmap(self, map):
		self.w.move(0,0)
		for s in map:
			try:
				self.w.addch(s.y, s.x, s.get_visible_char().symbol,
							s.get_visible_char().color)
			except curses.error:
				pass
			# Writing to the last cell of a window raises an exception because
			# the automatic cursor move to the next cell is illegal, this is
			# the only way to write to the last cell in the current wrapper

	def drawmemory(self, map):
		self.w.move(0,0)
		for s in map:
			try:
				self.w.addch(s.y, s.x, s.get_memory_char().symbol,
							s.get_memory_char().color)
			except curses.error:
				pass

	def drawsquare(self, s):
		try:
			self.w.addch(s.y, s.x, s.tile.ch_visible.symbol,
						s.tile.ch_visible.color)
		except curses.error:
			pass

	def drawlos(self, visibility, reverse=False):
		color = colors.normal if not reverse else colors.reverse
		for s in visibility:
			try:
				self.w.addch(s.y, s.x, s.get_visible_char().symbol,
						s.get_visible_char().color | color)
			except curses.error:
				pass

	def clearlos(self, old_visibility, l):
		for s in old_visibility:
			try:
			# The square we have in the container is the square we saw, but
			# because we're updating what we whould be remembering, we need
			# to update it to the current level square, thuse the seemingly
			# redundant use of l.getsquare with the already on hand square
				self.w.addch(s.y, s.x,
							l.getsquare(s.y, s.x).get_memory_char().symbol,
							l.getsquare(s.y, s.x).get_memory_char().color)
			except curses.error:
				pass

	def drawstar(self, square, col=colors.green):
		try:
			self.w.addch(square.y, square.x, "*", col)
		except curses.error:
			pass

	def drawblock(self, square, col=colors.blue):
		try:
			self.w.addch(square.y, square.x, " ", col)
		except curses.error:
			pass

	def drawline(self, s0, s1, char=Char('*', colors.yellow)):
		y0, x0 = s0.getloc()
		y1, x1 = s1.getloc()
		for y, x in bresenham(y0, x0, y1, x1):
			self.w.addch(y, x, char.symbol, char.color)
		self.getch(y1, x1)
