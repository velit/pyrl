class Char(object):
	"""Printable ncurses char. Contains both color and symbol."""
	def __init__(self, symbol='.', color="normal"):
		if len(symbol) == 1:
			self.symbol = symbol
		else:
			raise ValueError("Must be one character long: "+str(symbol))
		self.color = color

	def __len__(self):
		return 1
