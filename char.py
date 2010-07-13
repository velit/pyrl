from curses import A_NORMAL

class Char(object):
	"""Printable ncurses char. Contains both color and symbol."""
	def __init__(self, symbol='.', color=A_NORMAL):
		self.symbol = symbol
		self.color = color
