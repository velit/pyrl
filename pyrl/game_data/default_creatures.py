from __future__ import annotations

from pyrl.creature.creature import Creature
from pyrl.constants.colors import ColorPair

default_creatures = (
    #        name                 char                      danger_level   spawn_weight_class
    Creature("giant bat",        ('B', ColorPair.Brown),        -10,            1),
    Creature("giant worm",       ('w', ColorPair.Brown),         -5,            1),
    Creature("kobold",           ('k', ColorPair.Light_Green),    0,            1),
    Creature("goblin",           ('g', ColorPair.Green),          0,            1),
    Creature("zombie",           ('z', ColorPair.Cyan),           5,            1),
    Creature("orc",              ('o', ColorPair.Green),          5,            1),
    Creature("fire imp",         ('I', ColorPair.Red),           15,            1),
    Creature("blue baby drake",  ('D', ColorPair.Light_Blue),    15,            1),
    Creature("blue drake",       ('D', ColorPair.Blue),          15,            1),
    Creature("giant slug",       ("F", ColorPair.Light_Purple),  15,            1),
    Creature("ratling warrior",  ("r", ColorPair.Light_Cyan),    20,            1),
    Creature("lightning lizard", ("l", ColorPair.Yellow),        25,            1),
    Creature("red baby dragon",  ("d", ColorPair.Light_Red),     35,            1),
    Creature("moloch",           ('&', ColorPair.Yellow),        45,            1),
    Creature("angry moloch",     ('&', ColorPair.Light_Red),     65,            1),
    Creature("angrier moloch",   ('&', ColorPair.Red),           85,            1),
    Creature("angriest moloch",  ('&', ColorPair.Darker),        95,            1),
)
