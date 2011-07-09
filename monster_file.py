from char import Char

class MonsterFile:
	def __init__(self, name="kobold", base_hp=10, ch=Char('k', "green"),
			speciation_lvl=0, extinction_lvl=0):
		self.name = name
		self.base_hp = base_hp
		self.ch = ch
		self.speciation_lvl = speciation_lvl
		self.extinction_lvl = extinction_lvl


monster_files = (
	MonsterFile("kobold", 10, Char('k', "green"), -3, 0),
	MonsterFile("goblin", 10, Char('g', "green"), -2, 0),
	MonsterFile("giant bat", 10, Char('B', "brown"), -3, 0),
	MonsterFile("orc", 10, Char('o', "green"), -1, 0),
	MonsterFile("giant worm", 10, Char('w', "brown"), 0, 0),
	MonsterFile("fire imp", 10, Char('I', "red"), 3, 0),
	MonsterFile("greater moloch", 10, Char('&', "light_yellow"), 18, 0),
)
