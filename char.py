from const.colors import NORMAL

def Char(symbol=u" ", color=NORMAL):
	if len(symbol) == 1:
		return (symbol, color)
	else:
		raise ValueError(u"Must be one character long: {}".format(symbol))
