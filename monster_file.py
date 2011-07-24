from char import Char

class MonsterFile:
	def __init__(self, name="kobold", char=Char('k', "green"),
			speciation_lvl=0, extinction_lvl=0):
		self.name = name
		self.char = char
		self.speciation_lvl = speciation_lvl
		self.extinction_lvl = extinction_lvl


monster_files = (
	MonsterFile("kobold", Char('k', "green"), -3, 0),
	MonsterFile("goblin", Char('g', "green"), -2, 0),
	MonsterFile("giant bat", Char('B', "brown"), -3, 0),
	MonsterFile("orc", Char('o', "green"), -1, 0),
	MonsterFile("giant worm", Char('w', "brown"), 0, 0),
	MonsterFile("fire imp", Char('I', "red"), 3, 0),
	MonsterFile("greater moloch", Char('&', "light_yellow"), 18, 0),
)
