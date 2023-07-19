from __future__ import annotations

from dataclasses import dataclass

from pyrl.engine.creature.mixins.hoarder import Hoarder
from pyrl.engine.creature.mixins.learner import Learner
from pyrl.engine.creature.mixins.skiller import Skiller
from pyrl.engine.creature.mixins.turner import Turner
from pyrl.engine.creature.mixins.visionary import Visionary
from pyrl.engine.types.glyphs import Glyph, Color

@dataclass(eq=False)
class Player(Hoarder, Visionary, Learner, Turner, Skiller):

    name_: str

    @property
    def name(self) -> str:
        return self.name_

    @property
    def glyph(self) -> Glyph:
        return '@', (Color.Green, Color.Black)
