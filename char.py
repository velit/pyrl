def Char(symbol=u" ", color=u"normal"):
	if len(symbol) == 1:
		return (symbol, color)
	else:
		raise ValueError(u"Must be one character long: {}".format(symbol))
