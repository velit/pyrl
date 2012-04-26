import const.colors as COLOR
from monster_file import MonsterFile

monster_files = (
    MonsterFile("zombie", ('z', COLOR.CYAN), -3, 0),
    MonsterFile("kobold", ('k', COLOR.LIGHT_GREEN), -3, 0),
    MonsterFile("goblin", ('g', COLOR.GREEN), -2, 0),
    MonsterFile("giant bat", ('B', COLOR.BROWN), -3, 0),
    MonsterFile("orc", ('o', COLOR.GREEN), -1, 0),
    MonsterFile("giant worm", ('w', COLOR.BROWN), 0, 0),
    MonsterFile("fire imp", ('I', COLOR.RED), 3, 0),
    MonsterFile("moloch", ('&', COLOR.YELLOW), 18, 0),
    MonsterFile("blue drake", ('D', COLOR.BLUE), 0, 0),
    MonsterFile("blue baby drake", ('D', COLOR.LIGHT_BLUE), 0, 0),
    MonsterFile("red baby dragon", ("d", COLOR.LIGHT_RED), 0, 0),
    MonsterFile("lightning lizard", ("l", COLOR.YELLOW), 0, 0),
    MonsterFile("giant slug", ("F", COLOR.LIGHT_PURPLE), 0, 0),
    MonsterFile("ratling warrior", ("r", COLOR.LIGHT_CYAN), 0, 0),
)
