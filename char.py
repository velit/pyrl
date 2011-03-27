from collections import namedtuple

_Char = namedtuple("Char", ['symbol', 'color'])


class Char(namedtuple("Char", "symbol color")):
	__slots__ = ()

	def __new__(cls, symbol='.', color="normal"):
		if len(symbol) != 1:
			raise ValueError("Symbol must be one character long: " + str(symbol))
		return super(Char, cls).__new__(cls, symbol, color)

#def Char(symbol='.', color="normal"):
#	"""Printable ncurses char. Contains both color and symbol."""
#	if len(symbol) != 1:
#		raise ValueError("Symbol must be one character long: "+str(symbol))

#	return _Char(symbol, color)

#class Char():
#	"""Printable ncurses char. Contains both color and symbol."""
#	def __init__(self, symbol='.', color="normal"):
#		if len(symbol) == 1:
#			self.symbol = symbol
#		else:
#			raise ValueError("Must be one character long: "+str(symbol))
#		self.color = color

#	def __len__(self):
#		return 1
