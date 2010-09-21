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

	def getch_from_list(self, list=YES | NO | DEFAULT, str=None):
		if str:
			self.clear_and_print(str)
		c = self.w.getch()
		while c not in list:
			c = self.w.getch()
		return c

	def clear_and_print(self, str):
		self.clear()
		self.w.addstr(str)

	def _getstr(self, print_str=None):
		self.clear_and_print(print_str)
		curses.echo()
		str = self.w.getstr()
		curses.noecho()
		return str

	def getbool(self, print_str=None):
		while True:
			input = self._getstr(print_str + " [1/0]: ")
			if input == "" or input == "0":
				return False
			elif input == "1":
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

	def getstr(self, str=None):
		return self._getstr(str + " [str]: ")

	def getmaxyx(self):
		return self.w.getmaxyx()

	def move(self, y, x):
		self.w.move(y, x)

	def refresh(self):
		self.update()
		curses.doupdate()

	def addstr(self, *args, **keys):
		self.w.addstr(*args, **keys)

	def draw_menu(self, lines, returns, keys=(), i=0):
		return menu.draw(self, lines, returns, keys, i)

	def draw_h_menu(self, words, returns):
		return menu_h.draw(self, words, returns)
