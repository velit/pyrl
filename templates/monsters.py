from __future__ import absolute_import, division, print_function, unicode_literals

from enums.colors import Pair
from monster_template import MonsterTemplate


monster_templates = (
    MonsterTemplate("zombie", ('z', Pair.Cyan), -3, 0),
    MonsterTemplate("kobold", ('k', Pair.Light_Green), -3, 0),
    MonsterTemplate("goblin", ('g', Pair.Green), -2, 0),
    MonsterTemplate("giant bat", ('B', Pair.Brown), -3, 0),
    MonsterTemplate("orc", ('o', Pair.Green), -1, 0),
    MonsterTemplate("giant worm", ('w', Pair.Brown), 0, 0),
    MonsterTemplate("fire imp", ('I', Pair.Red), 3, 0),
    MonsterTemplate("moloch", ('&', Pair.Yellow), 18, 0),
    MonsterTemplate("blue drake", ('D', Pair.Blue), 0, 0),
    MonsterTemplate("blue baby drake", ('D', Pair.Light_Blue), 0, 0),
    MonsterTemplate("red baby dragon", ("d", Pair.Light_Red), 0, 0),
    MonsterTemplate("lightning lizard", ("l", Pair.Yellow), 0, 0),
    MonsterTemplate("giant slug", ("F", Pair.Light_Purple), 0, 0),
    MonsterTemplate("ratling warrior", ("r", Pair.Light_Cyan), 0, 0),
)
