import curses
import colors
from char import Char
from window import Window
from bresenham import bresenham
from tile import tiles

import time

class LevelWindow(Window):
	"""Handles the level display"""
	def __init__(self, window):
		super(LevelWindow, self).__init__(window)

	def drawmap(self, map):
		self.w.move(0,0)
		for s in map:
			try:
				self.addch(*s.get_visible_data())
			except curses.error:
				pass
			# Writing to the last cell of a window raises an exception because
			# the automatic cursor move to the next cell is illegal, this is
			# the only way to write to the last cell in the current wrapper

	def drawmemory(self, map):
		self.w.move(0,0)
		for s in map:
			try:
				self.addch(*s.get_memory_data())
			except curses.error:
				pass

	def drawlos(self, visibility, l, color_shift="normal"):
		for s in visibility:
			try:
				self.addch(*l.getsquare(*s).get_visible_data(color_shift))
			except curses.error:
				pass

	def clearlos(self, old_visibility, l):
		for s in old_visibility:
			try:
				self.addch(*l.getsquare(*s).get_memory_data())
			except curses.error:
				pass

	def drawtilemap(self, tilemap):
		self.w.move(0,0)
		x = tilemap.cols
		for i, t in enumerate(tilemap):
			try:
				if t in tilemap.tiles:
					self.addch(i/x, i%x, tilemap.tiles[t].ch_memory.symbol,
							tilemap.tiles[t].ch_memory.color)
				else:
					self.addch(i/x, i%x, tiles[t].ch_memory.symbol,
							tiles[t].ch_memory.color)
			except curses.error:
				pass

	def drawsquare(self, s):
		try:
			self.addch(s.get_visible_data())
		except curses.error:
			pass

	def drawstar(self, square, col="green"):
		try:
			self.addch(square.y, square.x, "*", col)
		except curses.error:
			pass

	def drawblock(self, square, col="blue"):
		try:
			self.addch(square.y, square.x, " ", col)
		except curses.error:
			pass

	def drawline(self, s0, s1, char=Char('*', "yellow")):
		y0, x0 = s0.getloc()
		y1, x1 = s1.getloc()
		for y, x in bresenham(y0, x0, y1, x1):
			self.addch(y, x, char.symbol, char.color)
		self.getch(y1, x1)
