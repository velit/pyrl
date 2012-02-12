from const.colors import NORMAL

def Char(symbol=" ", color=NORMAL):
	if len(symbol) == 1:
		return (symbol, color)
	else:
		raise ValueError("Must be one character long: {}".format(symbol))
