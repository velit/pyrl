from __future__ import absolute_import, division, print_function, unicode_literals

from enums.colors import Pair
from creature.template import CreatureTemplate


creature_templates = (
    CreatureTemplate("zombie", ('z', Pair.Cyan), -3, 0),
    CreatureTemplate("kobold", ('k', Pair.Light_Green), -3, 0),
    CreatureTemplate("goblin", ('g', Pair.Green), -2, 0),
    CreatureTemplate("giant bat", ('B', Pair.Brown), -3, 0),
    CreatureTemplate("orc", ('o', Pair.Green), -1, 0),
    CreatureTemplate("giant worm", ('w', Pair.Brown), 0, 0),
    CreatureTemplate("fire imp", ('I', Pair.Red), 3, 0),
    CreatureTemplate("moloch", ('&', Pair.Yellow), 18, 0),
    CreatureTemplate("blue drake", ('D', Pair.Blue), 0, 0),
    CreatureTemplate("blue baby drake", ('D', Pair.Light_Blue), 0, 0),
    CreatureTemplate("red baby dragon", ("d", Pair.Light_Red), 0, 0),
    CreatureTemplate("lightning lizard", ("l", Pair.Yellow), 0, 0),
    CreatureTemplate("giant slug", ("F", Pair.Light_Purple), 0, 0),
    CreatureTemplate("ratling warrior", ("r", Pair.Light_Cyan), 0, 0),
)
