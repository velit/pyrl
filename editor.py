import curses
import cPickle
import sys
from io import io

class Cursor():
	def __init__(self, y, x):
		self.y = y
		self.x = x

class Editor():
	def __init__(self):
		self.data = None

	def save(self):
		f = open("data", "w")
		cPickle.dump(self.data, f)
		f.close()

	def load(self):
		f = open("data", "r")
		self.data = cPickle.load(f)

	def ui(self):
		options = [("Tama menu uudestaan\n", self.ui), ("exit\n", exit)]
		io.getSelection(options)()

#	from map import Map
#	from tile import tiles
#
#	l = Map(20,80, False)
#	io.drawMap(l.map)
#
#	t = tiles["f"]
#	c = Cursor(0,0)
#	while True:
#		ch = io.getch(c.y, c.x)	
#		if ch == curses.KEY_LEFT:
#			c.x -= 1
#		elif ch == curses.KEY_RIGHT:
#			c.x += 1
#		elif ch == curses.KEY_UP:
#			c.y -= 1
#		elif ch == curses.KEY_DOWN:
#			c.y += 1
#		elif ch == ord('Q'):
#			sys.exit(0)
#		elif ch == ord('\n'):
#			a = l.getSquare(c.y, c.x)
#			a.tile = t
#			io.drawChar(c.y, c.x, a.getVisibleChar())
#		elif ch == ord('f'):
#			t = tiles["f"]
#		elif ch == <F2><F2>
#
#
#curses.wrapper(main)
