class Char(object):
	"""Printable ncurses char. Contains both color and symbol."""
	def __init__(self, symbol='.', color="normal"):
		self.symbol = symbol
		self.color = color
