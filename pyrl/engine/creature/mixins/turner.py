from dataclasses import dataclass, field

from pyrl.engine.creature.creature import Creature


@dataclass(eq=False)
class Turner(Creature):

    turns: int = field(init=False, repr=False, default=0)

    def apply_turn_effects(self, tick_delta: int) -> None:
        super().apply_turn_effects(tick_delta)
        self.turns += 1
