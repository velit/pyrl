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
		or_int = curses.A_REVERSE if reverse else curses.A_NORMAL
		for y, x, (symbol, color) in char_payload_iterator:
			try:
				self.w.addch(y, x, symbol, colors.CURSES_COLOR[color] | or_int)
			except curses.error:
				pass
			# Writing to the last cell of a window raises an exception because
			# the automatic cursor move to the next cell is illegal, this is
			# the only way to write to the last cell in the current wrapper

	def drawstar(self, coord, col="green"):
		y, x = coord
		self.addch(y, x, "*", col)

	def drawblock(self, coord, col="blue"):
		y, x = coord
		self.addch(y, x, " ", col)

	def drawline(self, coord_A, coord_B, char=Char('*', "yellow")):
		yA, xA = coord_A
		yB, xB = coord_B
		symbol, color = char
		for y, x in bresenham(yA, xA, yB, xB):
			self.addch(y, x, symbol, color)
		self.getch(yB, xB)
