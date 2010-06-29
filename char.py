from curses import A_NORMAL

class Char(object):
	"""Printable ncurses char. Contains both color and symbol."""

	#__slots__ = ("symbol", "color")

	def __init__(self, symbol=' ', color=A_NORMAL):
		self.symbol = symbol
		self.color = color

	#def __getstate__(self):
	#	return self.symbol, self.color

	#def __setstate__(self, state):
	#	self.symbol, self.color = state
