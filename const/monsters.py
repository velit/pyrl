import const.colors as COLOR
from char import Char
from monster_file import MonsterFile

monster_files = (
	MonsterFile("zombie", Char('z', COLOR.CYAN), -3, 0),
	MonsterFile("kobold", Char('k', COLOR.LIGHT_GREEN), -3, 0),
	MonsterFile("goblin", Char('g', COLOR.GREEN), -2, 0),
	MonsterFile("giant bat", Char('B', COLOR.BROWN), -3, 0),
	MonsterFile("orc", Char('o', COLOR.GREEN), -1, 0),
	MonsterFile("giant worm", Char('w', COLOR.BROWN), 0, 0),
	MonsterFile("fire imp", Char('I', COLOR.RED), 3, 0),
	MonsterFile("moloch", Char('&', COLOR.YELLOW), 18, 0),
	MonsterFile("blue drake", Char('D', COLOR.BLUE), 0, 0),
	MonsterFile("blue baby drake", Char('D', COLOR.LIGHT_BLUE), 0, 0),
	MonsterFile("red baby dragon", Char("d", COLOR.LIGHT_RED), 0, 0),
	MonsterFile("lightning lizard", Char("l", COLOR.YELLOW), 0, 0),
	MonsterFile("giant slug", Char("F", COLOR.LIGHT_PURPLE), 0, 0),
	MonsterFile("ratling warrior", Char("r", COLOR.LIGHT_CYAN), 0, 0),
)
