import const.game as GAME


class Tile(object):
    """The actual floor of a square."""

    def __init__(self, name, visible_char, mem_char, is_passable=True,
                 is_see_through=True, exit_point=None, movement_cost=GAME.MOVEMENT_COST):
        self.name = name
        self.visible_char = visible_char
        self.memory_char = mem_char
        self.is_passable = is_passable
        self.is_see_through = is_see_through
        self.movement_cost = movement_cost
        self.exit_point = exit_point

    @property
    def dr(self):
        return 0

    @property
    def pv(self):
        return 100 if self.is_passable else 40
