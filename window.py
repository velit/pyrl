import curses
import menu
import menu_h
import colors

from textwrap import wrap
from char import Char
from constants import YES, NO, DEFAULT

class Window(object):
	def __init__(self, window):
		self.w = window
		self.w.keypad(1)
		self.rows, self.cols = self.w.getmaxyx()

	def clear(self):
		self.w.erase()
		self.w.move(0, 0)

	def update(self):
		self.w.noutrefresh()

	def addch(self, *args):
		if len(args) == 4 or len(args) == 2:
			self.w.addch(*(args[:-1] + (colors.d[args[-1]],)))
		else:
			self.w.addch(*args)

	def getch(self, *args):
		return self.w.getch(*args)
	
	def gety(self):
		return self.w.getyx()[0]

	def getx(self):
		return self.w.getyx()[1]

	def getyx(self):
		return self.w.getyx()

	def sel_getch(self, print_str=None, char_list=YES | NO | DEFAULT):
		if print_str:
			self.clear_and_print(print_str)
		c = self.w.getch()
		while c not in char_list:
			c = self.w.getch()
		return c

	def clear_and_print(self, print_str):
		self.clear()
		self.w.addstr(print_str)

	def _getstr(self, print_str=None):
		self.clear_and_print(print_str)
		curses.echo()
		print_str = self.w.getstr()
		curses.noecho()
		return print_str

	def getbool(self, print_str=None):
		while True:
			input = self.sel_getch(print_str + " [T/F]: ",
					map(ord, "01fFtT\n"))
			if input in map(ord, "0fF\n"):
				return False
			elif input in map(ord, "1tT"):
				return True

	def getchar(self, print_str=None):
		while True:
			input = self._getstr(print_str + " [char]: ")
			if input == "":
				return " "
			elif len(input) == 1:
				return input

	def getcolor(self, print_str=None):
		while True:
			input = self._getstr(print_str + "[white/normal/black/red/green/"
										"yellow/blue/purple/cyan/light_*]: ")
			if input == "":
				return "normal"
			elif input in colors.d:
				return input

	def getint(self, print_str=None):
		while True:
			input = self._getstr(print_str + " [int]: ")
			if input == "":
				return 0
			try:
				return int(input)
			except ValueError:
				pass

	def getstr(self, print_str=None):
		return self._getstr(print_str + " [str]: ")

	def getmaxyx(self):
		return self.w.getmaxyx()

	def move(self, y, x):
		self.w.move(y, x)

	def refresh(self):
		self.update()
		curses.doupdate()

	def addstr(self, *args, **keys):
		self.w.addstr(*args, **keys)

	def draw_menu(self, *args, **keys):
		return menu.draw(self, *args, **keys)

	def draw_h_menu(self, *args, **keys):
		return menu_h.draw(self, *args, **keys)
