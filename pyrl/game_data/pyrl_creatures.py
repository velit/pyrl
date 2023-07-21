from __future__ import annotations

from collections.abc import Iterator
from enum import Enum

from pyrl.engine.creature.basic_creature import CreatureTemplate
from pyrl.engine.types.glyphs import Colors, Glyph


class PyrlCreature(Enum):
    #           name                   glyph         creature_level   spawn_weight_class
    GWORM    = ("giant worm",         ('w', Colors.Brown),        0,   200)
    GBAT     = ("giant bat",          ('b', Colors.Brown),        1,  1000)
    IMP      = ("imp",                ('i', Colors.Brown),        2,   400)
    GOBLIN   = ("goblin",             ('g', Colors.Green),        3,  1000)
    KOBOLD   = ("kobold",             ('k', Colors.Light_Green),  4,  1000)
    SKELETON = ("skeleton",           ('z', Colors.White),        5,  1000)
    ZOMBIE   = ("zombie",             ('z', Colors.Gray),         5,   500)
    GNOLL    = ("gnoll",              ('g', Colors.Brown),        6,  1000)
    GSPIDER  = ("giant spider",       ('S', Colors.Purple),       7,  1000)
    ORC      = ("orc",                ('o', Colors.Green),        8,  1000)
    GHOST    = ("ghost",              ('g', Colors.White),        9,  1000)
    FIMP     = ("fire imp",           ('I', Colors.Red),          10, 1000)
    TROLL    = ("troll",              ('T', Colors.Gray),         15, 1000)
    BBDRAKE  = ("blue baby drake",    ('D', Colors.Light_Blue),   15, 1000)
    GSLUG    = ("giant slug",         ("F", Colors.Light_Purple), 15, 1000)
    BDRAKE   = ("blue drake",         ('D', Colors.Light_Blue),   18, 1000)
    RWARRIOR = ("ratling warrior",    ("R", Colors.Light_Cyan),   20, 1000)
    LLIZARD  = ("lightning lizard",   ("L", Colors.Yellow),       25, 1000)
    RBD      = ("red baby dragon",    ("d", Colors.Light_Red),    25, 1000)
    RD       = ("red dragon",         ("D", Colors.Red),          35, 1000)
    ARD      = ("ancient red dragon", ("D", Colors.Red),          45, 1000)
    MOLOCH   = ("moloch",             ('&', Colors.Yellow),       55, 1000)
    AMOLOCH  = ("angry moloch",       ('&', Colors.Light_Red),    75, 1000)
    ARMOLOCH = ("angrier moloch",     ('&', Colors.Red),          95, 1000)
    ATMOLOCH = ("angriest moloch",    ('&', Colors.Darker),       95, 100)

    def __init__(self, name: str, glyph: Glyph, creature_level: int, spawn_weight_class: int) -> None:
        self.template = CreatureTemplate(name, glyph, creature_level, spawn_weight_class)

    @classmethod
    def templates(cls) -> Iterator[CreatureTemplate]:
        return map(lambda c: c.template, cls)
