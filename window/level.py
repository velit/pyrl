from char import Char
from .pyrl_window import PyrlWindow
from generic_algorithms import bresenham


class LevelWindow(PyrlWindow):
	u"""Handles the level display"""

	def __init__(self, concrete_window):
		PyrlWindow.__init__(self, concrete_window)

	def draw(self, char_payload_iterator, reverse=False):
		reverse_str = u"r" if reverse else u""
		for (y, x), (symbol, color) in char_payload_iterator:
			self.addch(y, x, (symbol, color + reverse_str))

	def draw_char(self, coord, char):
		y, x = coord
		self.addch(y, x, char)

	def draw_star(self, coord, col=u"green"):
		y, x = coord
		char = Char(u"*", col)
		self.addch(y, x, char)

	def draw_block(self, coord, col=u"blue"):
		y, x = coord
		char = Char(u" ", col + u"r")
		self.addch(y, x, char)

	def draw_line(self, coordA, coordB, char=Char(u'*', u"yellow")):
		for y, x in bresenham(coordA, coordB):
			self.addch(y, x, char)
