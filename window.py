import curses
import menu

from char import Char
from colors import color
from constants import YES, NO, DEFAULT

class Window(object):
	def __init__(self, window):
		self.w = window
		self.w.keypad(1)

	def clear(self):
		self.w.erase()
		self.w.move(0,0)

	def update(self):
		self.w.noutrefresh()

	def getch(self, y=None, x=None, str=None):
		if str:
			self.clear_and_print(str)
		if y is None and x is None:
			return self.w.getch()
		else:
			return self.w.getch(y, x)

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
				return color["normal"]
			elif input in color:
				return color[input]

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

	def addstr(self, str):
		self.w.addstr(str)

	def _getch(self):
		return self.w.getch()

	def draw_menu(self, lines, returns, keys=(), i=0):
		return menu.draw(self, lines, returns, keys, i)
