from __future__ import absolute_import, division, print_function, unicode_literals

import const.colors as COL
from monster_template import MonsterTemplate

monster_templates = (
    MonsterTemplate("zombie", ('z', COL.CYAN), -3, 0),
    MonsterTemplate("kobold", ('k', COL.LIGHT_GREEN), -3, 0),
    MonsterTemplate("goblin", ('g', COL.GREEN), -2, 0),
    MonsterTemplate("giant bat", ('B', COL.BROWN), -3, 0),
    MonsterTemplate("orc", ('o', COL.GREEN), -1, 0),
    MonsterTemplate("giant worm", ('w', COL.BROWN), 0, 0),
    MonsterTemplate("fire imp", ('I', COL.RED), 3, 0),
    MonsterTemplate("moloch", ('&', COL.YELLOW), 18, 0),
    MonsterTemplate("blue drake", ('D', COL.BLUE), 0, 0),
    MonsterTemplate("blue baby drake", ('D', COL.LIGHT_BLUE), 0, 0),
    MonsterTemplate("red baby dragon", ("d", COL.LIGHT_RED), 0, 0),
    MonsterTemplate("lightning lizard", ("l", COL.YELLOW), 0, 0),
    MonsterTemplate("giant slug", ("F", COL.LIGHT_PURPLE), 0, 0),
    MonsterTemplate("ratling warrior", ("r", COL.LIGHT_CYAN), 0, 0),
)
