from __future__ import annotations

from pyrl.creature.creature import Creature
from pyrl.types.color import ColorPairs

default_creatures = (
    #        name                 char                      danger_level   spawn_weight_class
    Creature("giant bat",        ('B', ColorPairs.Brown),        -10,            1),
    Creature("giant worm",       ('w', ColorPairs.Brown),         -5,            1),
    Creature("kobold",           ('k', ColorPairs.Light_Green),    0,            1),
    Creature("goblin",           ('g', ColorPairs.Green),          0,            1),
    Creature("zombie",           ('z', ColorPairs.Cyan),           5,            1),
    Creature("orc",              ('o', ColorPairs.Green),          5,            1),
    Creature("fire imp",         ('I', ColorPairs.Red),           15,            1),
    Creature("blue baby drake",  ('D', ColorPairs.Light_Blue),    15,            1),
    Creature("blue drake",       ('D', ColorPairs.Blue),          15,            1),
    Creature("giant slug",       ("F", ColorPairs.Light_Purple),  15,            1),
    Creature("ratling warrior",  ("r", ColorPairs.Light_Cyan),    20,            1),
    Creature("lightning lizard", ("l", ColorPairs.Yellow),        25,            1),
    Creature("red baby dragon",  ("d", ColorPairs.Light_Red),     35,            1),
    Creature("moloch",           ('&', ColorPairs.Yellow),        45,            1),
    Creature("angry moloch",     ('&', ColorPairs.Light_Red),     65,            1),
    Creature("angrier moloch",   ('&', ColorPairs.Red),           85,            1),
    Creature("angriest moloch",  ('&', ColorPairs.Darker),        95,            1),
)
