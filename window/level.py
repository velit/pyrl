import const.colors as COLOR
from char import Char
from .pyrl_window import PyrlWindow
from generic_algorithms import bresenham


class LevelWindow(PyrlWindow):
	"""Handles the level display"""

	def __init__(self, *a, **k):
		PyrlWindow.__init__(self, *a, **k)

	def draw_char(self, coord, char):
		y, x = coord
		self.addch(y, x, char)

	def draw_reverse_char(self, coord, char):
		y, x = coord
		symbol, color = char
		self.addch(y, x, (symbol, color[::-1]))

	def draw_star(self, coord, col=COLOR.GREEN):
		y, x = coord
		char = Char("*", col)
		self.addch(y, x, char)

	def draw_block(self, coord, col=COLOR.BASE_BLUE):
		y, x = coord

		char = (" ", (COLOR.BASE_BLACK, col))
		self.addch(y, x, char)

	def draw_line(self, coordA, coordB, char=Char('*', COLOR.YELLOW), includeFirst=False):
		if includeFirst:
			for y, x in bresenham(coordA, coordB):
				self.addch(y, x, char)
		else:
			for y, x in bresenham(coordA, coordB):
				if (y, x) != coordA:
					self.addch(y, x, char)
