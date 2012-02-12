from char import Char
from .pyrl_window import PyrlWindow
from generic_algorithms import bresenham
from const.colors import GREEN, BLUE, YELLOW, MAKE_REVERSE


class LevelWindow(PyrlWindow):
	"""Handles the level display"""

	def __init__(self, *a, **k):
		PyrlWindow.__init__(self, *a, **k)

	def draw(self, char_payload_iterator, reverse=False):
		reverse_str = MAKE_REVERSE if reverse else ""
		for (y, x), (symbol, color) in char_payload_iterator:
			self.addch(y, x, (symbol, color + reverse_str))

	def draw_char(self, coord, char):
		y, x = coord
		self.addch(y, x, char)

	def draw_star(self, coord, col=GREEN):
		y, x = coord
		char = Char("*", col)
		self.addch(y, x, char)

	def draw_block(self, coord, col=BLUE):
		y, x = coord

		char = (chr(176), col)
		self.addch(y, x, char)

	def draw_line(self, coordA, coordB, char=Char('*', YELLOW)):
		for y, x in bresenham(coordA, coordB):
			self.addch(y, x, char)
