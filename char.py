#from collections import namedtuple

#_Char = namedtuple("Char", ['symbol', 'color'])


#class Char(namedtuple("Char", "symbol color")):
#	__slots__ = ()

#	def __new__(cls, symbol='.', color="normal"):
#		if len(symbol) != 1:
#			raise ValueError("Symbol must be one character long: " + str(symbol))
#		return super().__new__(cls, symbol, color)

#def Char(symbol='.', color="normal"):
#	"""Printable ncurses char. Contains both color and symbol."""
#	if len(symbol) != 1:
#		raise ValueError("Symbol must be one character long: "+str(symbol))

#	return _Char(symbol, color)

#class Char:
#	"""Printable ncurses char. Contains both color and symbol."""
#	#__slots__ = ("symbol", "color")

#	def __init__(self, symbol='.', color="normal"):
#		if len(symbol) == 1:
#			self.symbol = symbol
#		else:
#			raise ValueError("Must be one character long: "+str(symbol))
#		self.color = color

	#def __getstate__(self):
	#	return self.symbol, self.color

	#def __setstate__(self, state):
	#	self.symbol, self.color = state

	#def __len__(self):
	#	return 1

def Char(symbol=" ", color="normal"):
	if len(symbol) == 1:
		return (symbol, color)
	else:
		raise ValueError("Must be one character long: {}".format(symbol))
