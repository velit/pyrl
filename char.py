import curses

class Char:
	def __init__(self, symbol=' ', color=curses.A_NORMAL):
		self.symbol = symbol
		self.color = color
