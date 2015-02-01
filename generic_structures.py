

class TwoDimensionalList(list):

    """
    Dynamic two dimensional list with a bounded width.

    Uses coordinates in _list[y, x] fashion.
    """

    def __init__(self, iterable, width):
        list.__init__(self, iterable)
        self._width = width

    def _get_index(self, coord):
        y, x = coord
        if x < self._width:
            return y * self._width + x
        else:
            raise IndexError("list x-component out of range.")

    def __getitem__(self, coord):
        return list.__getitem__(self, self._get_index(coord))

    def __setitem__(self, coord, value):
        return list.__setitem__(self, self._get_index(coord), value)

    def __delitem__(self, coord):
        return list.__delitem__(self, self._get_index(coord))
