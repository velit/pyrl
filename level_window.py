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

	def draw(self, char_payload_iterator, reverse=False):
		reverse_str = "r" if reverse else ""
		for y, x, (symbol, color) in char_payload_iterator:
			self.addch(y, x, (symbol, color + reverse_str))

	def drawstar(self, coord, col="green"):
		y, x = coord
		char = Char("*", col)
		self.addch(y, x, char)

	def drawblock(self, coord, col="blue"):
		y, x = coord
		char = Char(" ", col)
		self.addch(y, x, char)

	def drawline(self, coord_A, coord_B, char=Char('*', "yellow")):
		yA, xA = coord_A
		yB, xB = coord_B
		for y, x in bresenham(yA, xA, yB, xB):
			self.addch(y, x, char)
