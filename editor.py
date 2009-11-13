import curses
import pickle
import sys

class Cursor():
	def __init__(self, y, x):
		self.y = y
		self.x = x

def main(w):
	from map import Map
	from io import IO
	from tile import tiles

	l = Map(20,80, False)
	IO().drawMap(l.map)

	t = tiles["f"]
	c = Cursor(0,0)
	while True:
		ch = IO().getch(c.y, c.x)	
		if ch == curses.KEY_LEFT:
			c.x -= 1
		elif ch == curses.KEY_RIGHT:
			c.x += 1
		elif ch == curses.KEY_UP:
			c.y -= 1
		elif ch == curses.KEY_DOWN:
			c.y += 1
		elif ch == ord('Q'):
			sys.exit(0)
		elif ch == ord('\n'):
			a = l.getSquare(c.y, c.x)
			a.tile = t
			IO().drawChar(c.y, c.x, a.getVisibleChar())


curses.wrapper(main)
