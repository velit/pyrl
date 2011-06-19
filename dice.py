from random import randrange

def dice(num, sides):
	return sum(randrange(sides) + 1 for die in range(num))
