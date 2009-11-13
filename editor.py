import curses
import pickle

def main(w):
	from map import Map
	from io import IO
	from square import Square
	from tile import tiles

	r = tiles["r"]
	m = [[Square(r,j,i) for i in range(80)] for j in range(20)]
	IO().drawMap(m)
	IO().getch()

curses.wrapper(main)
