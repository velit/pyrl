import curses
from char import Char
from window import Window
from bresenham import bresenham
from tiles import gettile


class LevelWindow(Window):
	"""Handles the level display"""

	def __init__(self, window):
		super(LevelWindow, self).__init__(window)

	def drawmap(self, map_obj):
		self.w.move(0, 0)
		for s in map_obj:
			try:
				self.addch(s.y, s.x, *s.get_visible_char_data())
			except curses.error:
				pass
			# Writing to the last cell of a window raises an exception because
			# the automatic cursor move to the next cell is illegal, this is
			# the only way to write to the last cell in the current wrapper

	def drawmemory(self, map_obj):
		self.w.move(0, 0)
		for s in map_obj:
			try:
				self.addch(s.y, s.x, *s.get_memory_char_data())
			except curses.error:
				pass

	# drawlos and clearlos draw based on coordinates, they need to fetch
	# printing data with the getsquare function

	def drawlos(self, visibility, l, color_shift=""):
		for s in map(lambda coord: l.getsquare(*coord), visibility):
			try:
				self.addch(s.y, s.x, *s.get_visible_char_data(color_shift))
			except curses.error:
				pass

	def clearlos(self, old_visibility, l):
		for s in map(lambda coord: l.getsquare(*coord), old_visibility):
			try:
				self.addch(s.y, s.x, *s.get_memory_char_data())
			except curses.error:
				pass

	def drawtilemap(self, tm):
		self.w.move(0, 0)
		x = tm.cols
		for i, t in enumerate(map(lambda th: gettile(th, tm.tile_dict), tm)):
			try:
				self.addch(i // x, i % x, t.ch_memory.symbol, t.ch_memory.color)

				#if t in tilemap.tile_dict:
				#	self.addch(i//x, i%x, tilemap.tile_dict[t].ch_memory.symbol,
				#			tilemap.tile_dict[t].ch_memory.color)
				#else:
				#	self.addch(i//x, i%x, tiles[t].ch_memory.symbol,
				#			tiles[t].ch_memory.color)
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
		y0, x0 = s0.getloc()
		y1, x1 = s1.getloc()
		for y, x in bresenham(y0, x0, y1, x1):
			self.addch(y, x, char.symbol, char.color)
		self.getch(y1, x1)
