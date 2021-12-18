import typing
from collections import defaultdict

from pyrl.creature.creature import Creature

if typing.TYPE_CHECKING:
    CreatureHint = Creature
else:
    CreatureHint = object

class RemembersVision:

    """Creatures with this mixin class remember the level squares they've seen."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.visited_locations = defaultdict(set)
        self.vision = set()

    def get_visited_locations(self):
        return self.visited_locations[self.level]

    @property
    def vision(self):
        return self._vision

    @vision.setter
    def vision(self, coordinates):
        self.visited_locations[self.level] |= coordinates
        self._vision = coordinates

    @vision.deleter
    def vision(self):
        del self._vision
