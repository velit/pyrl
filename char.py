import curses

class Char:
	"Character object that holds both the visible character as well as the color that is used with ncurses."
	def __init__(self, symbol=' ', color=curses.A_NORMAL):
		self.symbol = symbol
		self.color = color
