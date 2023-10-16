from __future__ import annotations

from collections.abc import Iterable
from enum import Enum

from pyrl.engine.creature.enums.traits import Trait
from pyrl.engine.enums.mods import Mod
from pyrl.engine.creature.basic.basic_creature import BasicCreatureTemplate
from pyrl.engine.creature.enums.stats import Stat
from pyrl.engine.enums.glyphs import Colors

C = BasicCreatureTemplate

class PyrlCreature(Enum):
    #               name                   glyph        creature_level   spawn_weight_class trait mods
    GWORM     = C("giant worm",         ('w', Colors.Brown),        0,   200)
    GBAT      = C("giant bat",          ('b', Colors.Brown),        1,  1000)
    IMP       = C("imp",                ('i', Colors.Brown),        2,   400)
    GOBLIN    = C("goblin",             ('g', Colors.Green),        3,  1000)
    KOBOLD    = C("kobold",             ('k', Colors.Light_Green),  4,  1000)
    SKELETON  = C("skeleton",           ('z', Colors.White),        5,  1000, [Trait.UNDEAD])
    ZOMBIE    = C("zombie",             ('z', Colors.Gray),         5,   500, [Trait.UNDEAD])
    GNOLL     = C("gnoll",              ('g', Colors.Brown),        6,  1000)
    GSPIDER   = C("giant spider",       ('S', Colors.Purple),       7,  1000)
    ORC       = C("orc",                ('o', Colors.Green),        8,  1000)
    GHOST     = C("ghost",              ('g', Colors.White),        9,  1000, [Trait.UNDEAD, Trait.INCORPOREAL])
    FIMP      = C("fire imp",           ('I', Colors.Red),          10, 1000, [Trait.FIRE])
    TROLL     = C("troll",              ('T', Colors.Gray),         15, 1000)
    BBDRAKE   = C("blue baby drake",    ('D', Colors.Light_Blue),   15, 1000)
    GSLUG     = C("giant slug",         ("F", Colors.Light_Purple), 15, 1000)
    BDRAKE    = C("blue drake",         ('D', Colors.Light_Blue),   18, 1000)
    RWARRIOR  = C("ratling warrior",    ("R", Colors.Light_Cyan),   20, 1000)
    LLIZARD   = C("lightning lizard",   ("L", Colors.Yellow),       25, 1000)
    RBD       = C("red baby dragon",    ("d", Colors.Light_Red),    25, 1000, [Trait.FIRE])
    RD        = C("red dragon",         ("D", Colors.Red),          35, 1000, [Trait.FIRE])
    ARD       = C("ancient red dragon", ("D", Colors.Red),          45, 1000, [Trait.FIRE])
    QUICKLING = C("quickling",          ('q', Colors.Green),        65, 1000, mods={Stat.SPEED:  Mod.P9,
                                                                                    Stat.MAX_HP: Mod.N5})
    MOLOCH    = C("moloch",             ('&', Colors.Yellow),       55, 1000, mods={Stat.SPEED:  Mod.N3,
                                                                                    Stat.STR:    Mod.P4})
    AMOLOCH   = C("angry moloch",       ('&', Colors.Light_Red),    75, 1000, mods={Stat.SPEED:  Mod.N2,
                                                                                    Stat.STR:    Mod.P5})
    ARMOLOCH  = C("angrier moloch",     ('&', Colors.Red),          95, 1000, mods={Stat.SPEED:  Mod.N1,
                                                                                    Stat.STR:    Mod.P6})
    ATMOLOCH  = C("angriest moloch",    ('&', Colors.Darker),       95, 100,  mods={Stat.SPEED:  Mod.P0,
                                                                                    Stat.STR:    Mod.P7})

    @classmethod
    def templates(cls) -> Iterable[BasicCreatureTemplate]:
        return map(lambda creature_enum: creature_enum.value, cls)
