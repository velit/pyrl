import curses
import colors
from char import Char
from window import Window
from generic_algorithms import bresenham
from tiles import gettile


class LevelWindow(Window):
	"""Handles the level display"""

	def __init__(self, window):
		super().__init__(window)

	def draw(self, char_payload_iterator, reverse=False):
		reverse_str = "r" if reverse else ""
		for y, x, (symbol, color) in char_payload_iterator:
			self.addch(y, x, (symbol, color + reverse_str))

	def draw_char(self, coord, char):
		y, x = coord
		self.addch(y, x, char)

	def draw_star(self, coord, col="green"):
		y, x = coord
		char = Char("*", col)
		self.addch(y, x, char)

	def draw_block(self, coord, col="blue"):
		y, x = coord
		char = Char(" ", col + "r")
		self.addch(y, x, char)

	def draw_line(self, coordA, coordB, char=Char('*', "yellow")):
		yA, xA = coordA
		yB, xB = coordB
		for y, x in bresenham(yA, xA, yB, xB):
			self.addch(y, x, char)
