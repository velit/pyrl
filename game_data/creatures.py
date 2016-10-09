from creature import Creature
from enums.colors import Pair


creatures = (
    Creature("zombie", ('z', Pair.Cyan), -3, 0),
    Creature("kobold", ('k', Pair.Light_Green), -3, 0),
    Creature("goblin", ('g', Pair.Green), -2, 0),
    Creature("giant bat", ('B', Pair.Brown), -3, 0),
    Creature("orc", ('o', Pair.Green), -1, 0),
    Creature("giant worm", ('w', Pair.Brown), 0, 0),
    Creature("fire imp", ('I', Pair.Red), 3, 0),
    Creature("moloch", ('&', Pair.Yellow), 18, 0),
    Creature("blue drake", ('D', Pair.Blue), 0, 0),
    Creature("blue baby drake", ('D', Pair.Light_Blue), 0, 0),
    Creature("red baby dragon", ("d", Pair.Light_Red), 0, 0),
    Creature("lightning lizard", ("l", Pair.Yellow), 0, 0),
    Creature("giant slug", ("F", Pair.Light_Purple), 0, 0),
    Creature("ratling warrior", ("r", Pair.Light_Cyan), 0, 0),
)
