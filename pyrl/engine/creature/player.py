from __future__ import annotations

from dataclasses import dataclass

from pyrl.engine.creature.mixins.hoarder import Hoarder
from pyrl.engine.creature.mixins.learner import Learner
from pyrl.engine.creature.mixins.skiller import Skiller
from pyrl.engine.creature.mixins.turner import Turner
from pyrl.engine.creature.mixins.visionary import Visionary

@dataclass(eq=False)
class Player(Hoarder, Visionary, Learner, Turner, Skiller):
    pass
