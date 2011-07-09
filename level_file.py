from const.game import PASSAGE_UP, PASSAGE_DOWN, UP, DOWN

class LevelFile:

	def __init__(self, danger_level=0, map_file=None, map_not_rdg=True):
		self.danger_level = danger_level
		self.passages = {}
		self.map_not_rdg = map_not_rdg #true: map, false: rdg
		self.map_file = map_file
		self.monster_files = []

		if map_not_rdg:
			for key in self.map_file.entrance_locs:
				if key == PASSAGE_UP:
					self.passages[key] = UP
				elif key == PASSAGE_DOWN:
					self.passages[key] = DOWN
				else:
					raise NotImplementedError
		else:
			self.passages = {PASSAGE_UP: UP, PASSAGE_DOWN: DOWN}

	def addmonster(self, monster):
		self.monster_files.append(monster)
