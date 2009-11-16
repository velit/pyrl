from curses import A_NORMAL

class Char:
	"""Character object that holds both the visible character as well as the color that is used with ncurses."""
	def __init__(self, symbol=' ', color=A_NORMAL):
		self.symbol = symbol
		self.color = color
