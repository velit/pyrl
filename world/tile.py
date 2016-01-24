from __future__ import absolute_import, division, print_function, unicode_literals


class Tile(object):

    """Permanent portion of a square. Eg. walls or floor."""

    def __init__(self, name, visible_char, mem_char, passable=True, see_through=True, move_mult=1):
        self.name = name
        self.visible_char = visible_char
        self.memory_char = mem_char
        self.is_passable = passable
        self.is_see_through = see_through
        self.movement_multiplier = move_mult

    @property
    def defense_rating(self):
        return 0

    @property
    def armor(self):
        return 100 if self.is_passable else 40

    def __repr__(self):
        return "Tile({0.name}: {0.visible_char[0]})".format(self)
