from char import Char

class MonsterFile(object):
	def __init__(self, name=u"kobold", char=Char(u'k', u"green"),
			speciation_lvl=0, extinction_lvl=0):
		self.name = name
		self.char = char
		self.speciation_lvl = speciation_lvl
		self.extinction_lvl = extinction_lvl


monster_files = (
	MonsterFile(u"kobold", Char(u'k', u"green"), -3, 0),
	MonsterFile(u"goblin", Char(u'g', u"green"), -2, 0),
	MonsterFile(u"giant bat", Char(u'B', u"brown"), -3, 0),
	MonsterFile(u"orc", Char(u'o', u"green"), -1, 0),
	MonsterFile(u"giant worm", Char(u'w', u"brown"), 0, 0),
	MonsterFile(u"fire imp", Char(u'I', u"red"), 3, 0),
	MonsterFile(u"moloch", Char(u'&', u"yellow"), 18, 0),
)
