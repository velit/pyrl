from __future__ import annotations

from pyrl.creature.creature import Creature
from pyrl.types.color import ColorPairs

default_creatures = (
    #        name                   char                    creature_level   spawn_weight_class
    Creature("bat",                ('b', ColorPairs.Brown),          0,            10),
    Creature("giant bat",          ('B', ColorPairs.Brown),          1,            1000),
    Creature("giant worm",         ('w', ColorPairs.Brown),          1,            1000),
    Creature("goblin",             ('g', ColorPairs.Green),          5,            1000),
    Creature("kobold",             ('k', ColorPairs.Light_Green),    7,            1000),
    Creature("zombie",             ('z', ColorPairs.Cyan),          10,            1000),
    Creature("orc",                ('o', ColorPairs.Green),         10,            1000),
    Creature("fire imp",           ('I', ColorPairs.Red),           12,            1000),
    Creature("blue baby drake",    ('d', ColorPairs.Light_Blue),    15,            1000),
    Creature("giant slug",         ("F", ColorPairs.Light_Purple),  15,            1000),
    Creature("blue drake",         ('D', ColorPairs.Light_Blue),    18,            1000),
    Creature("ratling warrior",    ("r", ColorPairs.Light_Cyan),    20,            1000),
    Creature("lightning lizard",   ("l", ColorPairs.Yellow),        25,            1000),
    Creature("red baby dragon",    ("d", ColorPairs.Light_Red),     25,            1000),
    Creature("red dragon",         ("D", ColorPairs.Red),           35,            1000),
    Creature("ancient red dragon", ("D", ColorPairs.Red),           45,            1000),
    Creature("moloch",             ('&', ColorPairs.Yellow),        55,            1000),
    Creature("angry moloch",       ('&', ColorPairs.Light_Red),     75,            1000),
    Creature("angrier moloch",     ('&', ColorPairs.Red),           95,            1000),
    Creature("angriest moloch",    ('&', ColorPairs.Darker),        95,            100),
)
