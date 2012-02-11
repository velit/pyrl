from char import Char
from const.colors import GREEN, BROWN, RED, YELLOW

class MonsterFile(object):
	def __init__(self, name=u"kobold", char=Char(u'k', GREEN),
			speciation_lvl=0, extinction_lvl=0):
		self.name = name
		self.char = char
		self.speciation_lvl = speciation_lvl
		self.extinction_lvl = extinction_lvl


monster_files = (
	MonsterFile(u"kobold", Char(u'k', GREEN), -3, 0),
	MonsterFile(u"goblin", Char(u'g', GREEN), -2, 0),
	MonsterFile(u"giant bat", Char(u'B', BROWN), -3, 0),
	MonsterFile(u"orc", Char(u'o', GREEN), -1, 0),
	MonsterFile(u"giant worm", Char(u'w', BROWN), 0, 0),
	MonsterFile(u"fire imp", Char(u'I', RED), 3, 0),
	MonsterFile(u"moloch", Char(u'&', YELLOW), 18, 0),
)
