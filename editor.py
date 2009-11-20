import curses
import cPickle
import sys
from io import io

def save(data, name="data"):
	f = open(name, "w")
	cPickle.dump(data, f)
	f.close()

def load(name="data"):
	f = open(name, "r")
	a = cPickle.load(f)
	f.close()
	return a

class Cursor:
	def __init__(self, y, x):
		self.y = y
		self.x = x

class Data:
	def __init__(self):
		self.tiles = {}

class Editor:
	def __init__(self):
		self.data = Data()

	def save(self):
		f = open("data", "w")
		cPickle.dump(self.data, f)
		f.close()

	def load(self):
		f = open("data", "r")
		self.data = cPickle.load(f)

	def ui(self):
		options = (("Tile editor", self.ui), ("Level editor", self.ui), ("exit", exit))
		io.getSelection(options)()

	def tile_editor(self):
		


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
