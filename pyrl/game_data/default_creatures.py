from __future__ import annotations

from pyrl.creature.creature import Creature
from pyrl.types.color import Colors

default_creatures = (
    #        name                   glyph         creature_level   spawn_weight_class
    Creature("bat",                ('b', Colors.Brown),        0,  10),
    Creature("giant bat",          ('B', Colors.Brown),        1,  1000),
    Creature("giant worm",         ('w', Colors.Brown),        1,  1000),
    Creature("goblin",             ('g', Colors.Green),        5,  1000),
    Creature("kobold",             ('k', Colors.Light_Green),  7,  1000),
    Creature("zombie",             ('z', Colors.Cyan),         10, 1000),
    Creature("orc",                ('o', Colors.Green),        10, 1000),
    Creature("fire imp",           ('I', Colors.Red),          12, 1000),
    Creature("blue baby drake",    ('d', Colors.Light_Blue),   15, 1000),
    Creature("giant slug",         ("F", Colors.Light_Purple), 15, 1000),
    Creature("blue drake",         ('D', Colors.Light_Blue),   18, 1000),
    Creature("ratling warrior",    ("r", Colors.Light_Cyan),   20, 1000),
    Creature("lightning lizard",   ("l", Colors.Yellow),       25, 1000),
    Creature("red baby dragon",    ("d", Colors.Light_Red),    25, 1000),
    Creature("red dragon",         ("D", Colors.Red),          35, 1000),
    Creature("ancient red dragon", ("D", Colors.Red),          45, 1000),
    Creature("moloch",             ('&', Colors.Yellow),       55, 1000),
    Creature("angry moloch",       ('&', Colors.Light_Red),    75, 1000),
    Creature("angrier moloch",     ('&', Colors.Red),          95, 1000),
    Creature("angriest moloch",    ('&', Colors.Darker),       95, 100),
)
