from pyrl.creature import Creature
from pyrl.enums.colors import Pair

default_creatures = (#name       char                      danger_level    spawn_weight_class
    Creature("giant bat",        ('B', Pair.Brown),        -10,            1),
    Creature("giant worm",       ('w', Pair.Brown),         -5,            1),
    Creature("kobold",           ('k', Pair.Light_Green),    0,            1),
    Creature("goblin",           ('g', Pair.Green),          0,            1),
    Creature("zombie",           ('z', Pair.Cyan),           5,            1),
    Creature("orc",              ('o', Pair.Green),          5,            1),
    Creature("fire imp",         ('I', Pair.Red),           15,            1),
    Creature("blue baby drake",  ('D', Pair.Light_Blue),    15,            1),
    Creature("blue drake",       ('D', Pair.Blue),          15,            1),
    Creature("giant slug",       ("F", Pair.Light_Purple),  15,            1),
    Creature("ratling warrior",  ("r", Pair.Light_Cyan),    20,            1),
    Creature("lightning lizard", ("l", Pair.Yellow),        25,            1),
    Creature("red baby dragon",  ("d", Pair.Light_Red),     35,            1),
    Creature("moloch",           ('&', Pair.Yellow),        45,            1),
    Creature("angry moloch",     ('&', Pair.Light_Red),     65,            1),
    Creature("angrier moloch",   ('&', Pair.Red),           85,            1),
    Creature("angriest moloch",  ('&', Pair.Darker),        95,            1),
)
