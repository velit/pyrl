from char import Char
from const.colors import GREEN, BROWN, RED, YELLOW
from monster_file import MonsterFile

monster_files = (
	MonsterFile("kobold", Char('k', GREEN), -3, 0),
	MonsterFile("goblin", Char('g', GREEN), -2, 0),
	MonsterFile("giant bat", Char('B', BROWN), -3, 0),
	MonsterFile("orc", Char('o', GREEN), -1, 0),
	MonsterFile("giant worm", Char('w', BROWN), 0, 0),
	MonsterFile("fire imp", Char('I', RED), 3, 0),
	MonsterFile("moloch", Char('&', YELLOW), 18, 0),
)
