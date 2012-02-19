import const.colors as COLOR
from char import Char
from .pyrl_window import PyrlWindow
from generic_algorithms import bresenham


class LevelWindow(PyrlWindow):
	"""Handles the level display"""

	def __init__(self, *a, **k):
		PyrlWindow.__init__(self, *a, **k)

	def draw(self, char_payload_sequence):
		for payload in char_payload_sequence:
			self.addch(*payload)

	def draw_reverse(self, char_payload_sequence):
		for y, x, (symbol, color) in char_payload_sequence:
			self.addch(y, x, (symbol, color[::-1]))

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

	def draw_block(self, coord, col=COLOR.BLUE):
		y, x = coord

		char = (chr(176), col)
		self.addch(y, x, char)

	def draw_line(self, coordA, coordB, char=Char('*', COLOR.YELLOW), includeFirst=False):
		if includeFirst:
			for y, x in bresenham(coordA, coordB):
				self.addch(y, x, char)
		else:
			for y, x in bresenham(coordA, coordB):
				if (y, x) != coordA:
					self.addch(y, x, char)
