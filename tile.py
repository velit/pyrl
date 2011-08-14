import const.game as CG
from char import Char


class Tile:
	"""The actual floor of a square."""

	def __init__(self, name="floor", visible=Char(), mem=Char(), is_passable=True,
				is_see_through=True, movement_cost=CG.MOVEMENT_COST, exit_point=None):
		self.name = name
		self.visible_char = visible
		self.memory_char = mem
		self.is_passable = is_passable
		self.is_see_through = is_see_through
		self.movement_cost = movement_cost
		self.exit_point = exit_point
