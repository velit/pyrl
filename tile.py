from char import Char
from const.game import OPTIMIZATION


class Tile:
	"""The actual floor of a square."""

	def __init__(self, name="floor", visible=Char(), mem=Char(), passable=True,
				see_through=True, movement_cost=1000, exit_point=None):
		self.name = name
		self.visible_char = visible
		self.memory_char = mem
		self.passable = passable
		self.see_through = see_through
		self.movement_cost = movement_cost
		self.exit_point = exit_point
