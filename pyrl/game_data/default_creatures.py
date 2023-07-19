from __future__ import annotations

from pyrl.engine.creature.basic_creature import CreatureTemplate
from pyrl.engine.types.glyphs import Colors

default_creatures = (
    #                name                   glyph         creature_level   spawn_weight_class
    CreatureTemplate("bat",                ('b', Colors.Brown),        0,  10),
    CreatureTemplate("giant bat",          ('B', Colors.Brown),        1,  1000),
    CreatureTemplate("giant worm",         ('w', Colors.Brown),        1,  1000),
    CreatureTemplate("goblin",             ('g', Colors.Green),        5,  1000),
    CreatureTemplate("kobold",             ('k', Colors.Light_Green),  7,  1000),
    CreatureTemplate("zombie",             ('z', Colors.Cyan),         10, 1000),
    CreatureTemplate("orc",                ('o', Colors.Green),        10, 1000),
    CreatureTemplate("fire imp",           ('I', Colors.Red),          12, 1000),
    CreatureTemplate("blue baby drake",    ('d', Colors.Light_Blue),   15, 1000),
    CreatureTemplate("giant slug",         ("F", Colors.Light_Purple), 15, 1000),
    CreatureTemplate("blue drake",         ('D', Colors.Light_Blue),   18, 1000),
    CreatureTemplate("ratling warrior",    ("r", Colors.Light_Cyan),   20, 1000),
    CreatureTemplate("lightning lizard",   ("l", Colors.Yellow),       25, 1000),
    CreatureTemplate("red baby dragon",    ("d", Colors.Light_Red),    25, 1000),
    CreatureTemplate("red dragon",         ("D", Colors.Red),          35, 1000),
    CreatureTemplate("ancient red dragon", ("D", Colors.Red),          45, 1000),
    CreatureTemplate("moloch",             ('&', Colors.Yellow),       55, 1000),
    CreatureTemplate("angry moloch",       ('&', Colors.Light_Red),    75, 1000),
    CreatureTemplate("angrier moloch",     ('&', Colors.Red),          95, 1000),
    CreatureTemplate("angriest moloch",    ('&', Colors.Darker),       95, 100),
)
