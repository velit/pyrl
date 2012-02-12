from char import Char
from const.colors import GREEN, BROWN, RED, YELLOW

class MonsterFile(object):
	def __init__(self, name="kobold", char=Char('k', GREEN),
			speciation_lvl=0, extinction_lvl=0):
		self.name = name
		self.char = char
		self.speciation_lvl = speciation_lvl
		self.extinction_lvl = extinction_lvl


monster_files = (
	MonsterFile("kobold", Char('k', GREEN), -3, 0),
	MonsterFile("goblin", Char('g', GREEN), -2, 0),
	MonsterFile("giant bat", Char('B', BROWN), -3, 0),
	MonsterFile("orc", Char('o', GREEN), -1, 0),
	MonsterFile("giant worm", Char('w', BROWN), 0, 0),
	MonsterFile("fire imp", Char('I', RED), 3, 0),
	MonsterFile("moloch", Char('&', YELLOW), 18, 0),
)
