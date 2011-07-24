import curses
import colors
from char import Char
from window import Window
from bresenham import bresenham
from tiles import gettile


class LevelWindow(Window):
	"""Handles the level display"""

	def __init__(self, window):
		super().__init__(window)

	def addch(self, loc, cols, char):
		self.w.addch(loc // cols, loc % cols, char[0], colors.CURSES_COLOR[char[1]])

	def draw(self, seq, cols):
		for y, x, symbol, color in seq:
			self.addch(y, x, symbol, color)

	def drawlevel(self, level):
		self.w.move(0, 0)
		for loc in level.get_loc_iterator():
			try:
				self.addch(loc, level.cols, level.get_visible_char_data(loc))
			except curses.error:
				pass
			# Writing to the last cell of a window raises an exception because
			# the automatic cursor move to the next cell is illegal, this is
			# the only way to write to the last cell in the current wrapper

	def drawmemory(self, level):
		self.w.move(0, 0)
		for loc in level.get_loc_iterator():
			try:
				self.addch(loc, level.cols, level.get_memory_char_data(loc))
			except curses.error:
				pass

	# drawlos and clearlos draw based on coordinates, they need to fetch
	# printing data with the getsquare function

	def drawlos(self, loc_set, level, color_shift=""):
		for loc in loc_set:
			try:
				self.addch(loc, level.cols, level.get_visible_char_data(loc, color_shift))
			except curses.error:
				pass

	def clearlos(self, loc_set, level):
		for loc in loc_set:
			try:
				self.addch(loc, level.cols, level.get_memory_char_data(loc))
			except curses.error:
				pass

	def drawtilemap(self, level_file):
		self.w.move(0, 0)
		for loc in range(len(level_file.tilefile)):
			try:
				t = level_file.get_tile_from_loc(loc)
				self.addch(loc, level_file.cols, t.memory_ch)
			except curses.error:
				pass

	#def drawsquare(self, s):
	#	try:
	#		self.addch(s.get_visible_data())
	#	except curses.error:
	#		pass

	#def drawstar(self, square, col="green"):
	#	try:
	#		self.addch(square.y, square.x, "*", col)
	#	except curses.error:
	#		pass

	#def drawblock(self, square, col="blue"):
	#	try:
	#		self.addch(square.y, square.x, " ", col)
	#	except curses.error:
	#		pass

	#def drawline(self, s0, s1, char=Char('*', "yellow")):
	#	y0, x0 = s0.getcoord()
	#	y1, x1 = s1.getcoord()
	#	for y, x in bresenham(y0, x0, y1, x1):
	#		self.addch(y, x, char.symbol, char.color)
	#	self.getch(y1, x1)
