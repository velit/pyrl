import curses
import pickle

def main(w):
	from map import Map
	from io import IO

	l = []
	l.append(Map(20, 80))
	IO().drawMap(l[0].map)
	IO().getch()

curses.wrapper(main)
