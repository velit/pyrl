def Char(symbol=" ", color="normal"):
	if len(symbol) == 1:
		return (symbol, color)
	else:
		raise ValueError("Must be one character long: {}".format(symbol))
