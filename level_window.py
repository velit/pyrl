import curses
from char import Char
from window import Window
from bresenham import bresenham
from tiles import gettile


class LevelWindow(Window):
	"""Handles the level display"""

	def __init__(self, window):
		super().__init__(window)

	def drawmap(self, map_obj):
		self.w.move(0, 0)
		for s in map_obj.squares:
			try:
				self.addch(s.y, s.x, *s.get_visible_char_data())
			except curses.error:
				pass
			# Writing to the last cell of a window raises an exception because
			# the automatic cursor move to the next cell is illegal, this is
			# the only way to write to the last cell in the current wrapper

	def drawmemory(self, map_obj):
		self.w.move(0, 0)
		for s in map_obj.squares:
			try:
				self.addch(s.y, s.x, *s.get_memory_char_data())
			except curses.error:
				pass

	# drawlos and clearlos draw based on coordinates, they need to fetch
	# printing data with the getsquare function

	def drawlos(self, coord_set, l, color_shift=""):
		for s in (l.getsquare(coord) for coord in coord_set):
			try:
				self.addch(s.y, s.x, *s.get_visible_char_data(color_shift))
			except curses.error:
				pass

	def clearlos(self, coord_set, l):
		for s in (l.getsquare(coord) for coord in coord_set):
			try:
				self.addch(s.y, s.x, *s.get_memory_char_data())
			except curses.error:
				pass

	def drawtilemap(self, map_file):
		self.w.move(0, 0)
		c = map_file.cols
		for i in range(len(map_file.tilemap)):
			try:
				t = map_file.gettile(i // c, i % c)
				self.addch(i // c, i % c, t.ch_memory.symbol, t.ch_memory.color)
			except curses.error:
				pass

	def drawsquare(self, s):
		try:
			self.addch(s.get_visible_data())
		except curses.error:
			pass

	def drawstar(self, square, col="green"):
		try:
			self.addch(square.y, square.x, "*", col)
		except curses.error:
			pass

	def drawblock(self, square, col="blue"):
		try:
			self.addch(square.y, square.x, " ", col)
		except curses.error:
			pass

	def drawline(self, s0, s1, char=Char('*', "yellow")):
		y0, x0 = s0.getcoord()
		y1, x1 = s1.getcoord()
		for y, x in bresenham(y0, x0, y1, x1):
			self.addch(y, x, char.symbol, char.color)
		self.getch(y1, x1)
