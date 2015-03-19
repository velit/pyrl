

class List2D(list):

    """
    Sub-class of list which overrides accessor methods with 2D ones.

    The second dimension is bounded by constructor parameter, first dimension is
    bounded by the amount of items given to the list divided by the second
    dimension bound.

    Iterating the flat list gives items that increase quicker in the second
    dimension. In other words the first four items in a list with the second
    dimension bounded to two are: (0, 0), (0, 1), (1, 0), (1, 1).
    """

    def __init__(self, iterable, second_dimension_bound):
        super(List2D, self).__init__(iterable)
        self._second_dim_bound = second_dimension_bound

    def _get_index(self, coord):
        first_dim, second_dim = coord
        if second_dim < self._second_dim_bound:
            return first_dim * self._second_dim_bound + second_dim
        else:
            raise IndexError("second dimension index out of range.")

    def __getitem__(self, coord):
        return super(List2D, self).__getitem__(self._get_index(coord))

    def __setitem__(self, coord, value):
        return super(List2D, self).__setitem__(self._get_index(coord), value)

    def __delitem__(self, coord):
        return super(List2D, self).__delitem__(self._get_index(coord))
